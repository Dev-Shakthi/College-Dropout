from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
import os
import uvicorn
import requests

app = FastAPI()
APP_DIR = os.getcwd()

@app.get("/health")
async def health_check():
    """Health check endpoint for nginx"""
    return {"status": "healthy"}
    
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

@app.get("/streamlit/{path:path}")
async def proxy_streamlit(path: str):
    try:
        # Forward request to internal Streamlit server
        streamlit_url = f"http://127.0.0.1:8501/{path}"
        response = requests.get(streamlit_url, timeout=10)
        
        # Return the response
        if response.headers.get('content-type', '').startswith('text/html'):
            return HTMLResponse(response.content, status_code=response.status_code)
        else:
            return PlainTextResponse(response.content, status_code=response.status_code)
            
    except requests.exceptions.RequestException as e:
        return PlainTextResponse(f"Streamlit proxy error: {str(e)}", status_code=503)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
