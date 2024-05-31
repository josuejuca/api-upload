from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI()

# Diretório de templates
templates = Jinja2Templates(directory="templates")

# Diretório onde os arquivos serão armazenados
UPLOAD_DIRECTORY = "uploads"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Monta a rota estática para servir os arquivos do diretório uploads
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request})

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"filename": file.filename, "status": "uploaded successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/files/", response_class=HTMLResponse)
async def list_files(request: Request):
    files = [f.name for f in Path(UPLOAD_DIRECTORY).iterdir() if f.is_file()]
    return templates.TemplateResponse("files.jinja", {"request": request, "files": files})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
