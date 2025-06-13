import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()
APP_DIR = "/app"

@app.get("/read")
async def read_file(page: str):
    """Read file endpoint"""
    try:
        with open(os.path.join(APP_DIR, page), "r") as f:
            return PlainTextResponse(f.read())
    except FileNotFoundError:
        return PlainTextResponse("File not found", status_code=404)
    except Exception as e:
        return PlainTextResponse(f"Error reading file: {str(e)}", status_code=500)

@app.get("/api/files")
async def list_files():
    """List all files in the app directory"""
    try:
        files = []
        for root, dirs, filenames in os.walk(APP_DIR):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), APP_DIR)
                files.append(rel_path)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "app_dir": APP_DIR,
        "files_exist": os.path.exists(os.path.join(APP_DIR, "app.py"))
    }
