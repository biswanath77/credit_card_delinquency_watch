"""
Main entry point for the backend application
Run with: uvicorn backend.main:app --reload
"""

from backend.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
