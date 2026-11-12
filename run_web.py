"""Start the calcium-channel census dashboard on http://127.0.0.1:8177 (local only, read-only).

Run: python run_web.py   (needs: pip install -r requirements-web.txt)
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.web.app:app", host="127.0.0.1", port=8177)
