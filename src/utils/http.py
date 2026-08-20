"""A polite, retrying, stdlib-only HTTP client — and the reason it exists.

Every fetcher in `src/cli_channel.py` and `src/classify/reference.py` used to
be shaped like this::

    try:
        return _json(url)
    except Exception:
        return {}

which cannot tell "this protein carries no Pfam domain" from "UniProt rate
limited us". The second one is common — a benchmark panel is ~70 proteins and
three requests each — and its consequences are silent and wrong, not loud and
absent:

* an empty `pfam_counts` makes a protein look like it "carries nothing a
  calcium channel carries", so a positive is scored as a miss;
* an empty anchor sequence makes `verify_anchor()` fail, which this project
  reads as *the anchor has drifted* — the TRPV6 D542/D582 finding says that is
  a real risk, so a network hiccup must never be able to imitate it;
* an empty exemplar sequence silently shrinks the reference panel, and the
  reference tier then scores against a panel nobody declared.

So: retry with backoff, distinguish a genuine 404 from a transient failure,
and **raise** when the retries are exhausted. A missing result is a missing
result and a note, never a silently weaker method (**D28**).

Stdlib only — `src/cli_channel.py` and the classifier must run in a bare
interpreter.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

#: Seconds to wait after attempt *i* fails. Four attempts total by default.
BACKOFFS = (1.0, 3.0, 8.0)

#: Sent on every request so the upstream services can identify the client.
USER_AGENT = "calcium-channel-census/0.1 (https://github.com/; research use)"

#: HTTP codes that mean "the record is genuinely not there", not "try again".
ABSENT_CODES = (204, 404)

#: HTTP codes that are always worth retrying, whatever the retry budget says.
TRANSIENT_CODES = (429, 500, 502, 503, 504)


class FetchFailed(RuntimeError):
    """A request failed after every retry.

    Raised rather than returned so no caller can mistake a network failure for
    an empty record. Carries the url and the last error seen.
    """

    def __init__(self, url: str, reason: str, attempts: int):
        self.url = url
        self.reason = reason
        self.attempts = attempts
        super().__init__(f"{reason} after {attempts} attempt(s): {url}")


@dataclass
class Fetcher:
    """A polite client that retries, then raises, and keeps a ledger.

    `n_requests` and `failures` make a run's network behaviour reportable:
    S0 quotes both in its report, and S1 now does the same.
    """

    sleep_s: float = 0.12
    timeout_s: int = 40
    max_retries: int = 3
    n_requests: int = 0
    n_absent: int = 0
    failures: list[tuple[str, str]] = field(default_factory=list)

    # -- the one place a request is actually made ------------------------
    def _fetch(self, url: str, accept: str, allow_absent: bool) -> str | None:
        last = "unknown"
        attempts = self.max_retries + 1
        for attempt in range(attempts):
            try:
                req = urllib.request.Request(
                    url, headers={"Accept": accept, "User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=self.timeout_s) as r:
                    payload = r.read().decode()
                self.n_requests += 1
                time.sleep(self.sleep_s)
                return payload
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code in ABSENT_CODES and allow_absent:
                    self.n_requests += 1
                    self.n_absent += 1
                    time.sleep(self.sleep_s)
                    return None
                # A 4xx that is not 429 will not fix itself; do not spend the
                # retry budget on it.
                if 400 <= e.code < 500 and e.code not in TRANSIENT_CODES:
                    break
            except Exception as e:                  # network, timeout, decode
                last = type(e).__name__
            if attempt < attempts - 1:
                time.sleep(BACKOFFS[min(attempt, len(BACKOFFS) - 1)])
        self.failures.append((url, last))
        raise FetchFailed(url, last, attempts)

    # -- the two shapes callers want -------------------------------------
    def json(self, url: str, allow_absent: bool = True):
        """Parsed JSON, or `None` if the record is genuinely absent.

        Raises `FetchFailed` if the request could not be completed.
        """
        text = self._fetch(url, "application/json", allow_absent)
        if text is None:
            return None
        try:
            return json.loads(text)
        except ValueError as e:
            self.failures.append((url, f"bad JSON: {e}"))
            raise FetchFailed(url, "bad JSON", 1) from e

    def text(self, url: str, allow_absent: bool = True) -> str | None:
        """Response body, or `None` if the record is genuinely absent."""
        return self._fetch(url, "text/plain", allow_absent)

    # -- reporting --------------------------------------------------------
    def ledger(self) -> dict:
        return {"requests": self.n_requests,
                "absent": self.n_absent,
                "failures": len(self.failures),
                "failed_urls": [u for u, _ in self.failures[:20]]}


#: The shared instance the module-level helpers use, so a whole process's
#: request count and failure ledger can be read back at the end of a run.
DEFAULT = Fetcher()


def get_json(url: str, allow_absent: bool = True):
    return DEFAULT.json(url, allow_absent)


def get_text(url: str, allow_absent: bool = True) -> str | None:
    return DEFAULT.text(url, allow_absent)


def ledger() -> dict:
    """The shared fetcher's request/failure counts, for a run's summary."""
    return DEFAULT.ledger()


def reset_ledger() -> None:
    DEFAULT.n_requests = 0
    DEFAULT.n_absent = 0
    DEFAULT.failures.clear()
