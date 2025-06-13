from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()
APP_DIR = os.getcwd()

@app.get("/read")
async def read_file(page: str):
    try:
        with open(os.path.join(APP_DIR, page), "r") as f:
            return PlainTextResponse(f.read())
    except FileNotFoundError:
        return PlainTextResponse("File not found", status_code=404)

@app.post("/write")
async def write_file(request: Request):
    page = request.query_params.get("page")
    content = await request.body()
    with open(os.path.join(APP_DIR, page), "wb") as f:
        f.write(content)
    os.system(f"touch {os.path.join(APP_DIR, 'app.py')}") 
    return {"status": "success"}
