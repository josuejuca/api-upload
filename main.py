from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import os
import mimetypes

app = FastAPI()

# Diretório de templates
templates = Jinja2Templates(directory="templates")

# Diretório onde os arquivos serão armazenados
UPLOAD_DIRECTORY = "uploads"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Monta a rota estática para servir os arquivos do diretório uploads
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

@app.get("/", response_class=HTMLResponse, tags=["Interface de Usuário"])
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploadfile/", tags=["Gerenciamento de Arquivos"])
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"filename": file.filename, "status": "uploaded successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/createdir/", tags=["Gerenciamento de Diretórios"])
async def create_directory(directory_name: str):
    try:
        dir_path = Path(UPLOAD_DIRECTORY) / directory_name
        dir_path.mkdir(parents=True, exist_ok=True)
        return JSONResponse(content={"directory": str(dir_path), "status": "created successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/search/", tags=["Pesquisa"])
async def search_files_and_directories(search_term: str):
    try:
        base_path = Path(UPLOAD_DIRECTORY)
        matches = []
        for path in base_path.rglob('*'):
            if search_term in path.name:
                matches.append(str(path))
        return JSONResponse(content={"matches": matches})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.put("/rename/", tags=["Gerenciamento de Arquivos"])
async def rename_item(old_name: str, new_name: str):
    try:
        old_path = Path(UPLOAD_DIRECTORY) / old_name
        new_path = Path(UPLOAD_DIRECTORY) / new_name
        if not old_path.exists():
            raise HTTPException(status_code=404, detail="Item not found")
        old_path.rename(new_path)
        return JSONResponse(content={"old_name": old_name, "new_name": new_name, "status": "renamed successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.delete("/delete/", tags=["Gerenciamento de Arquivos"])
async def delete_item(item_name: str):
    try:
        item_path = Path(UPLOAD_DIRECTORY) / item_name
        if not item_path.exists():
            raise HTTPException(status_code=404, detail="Item not found")
        if item_path.is_dir():
            shutil.rmtree(item_path)
        else:
            item_path.unlink()
        return JSONResponse(content={"item_name": item_name, "status": "deleted successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/move/", tags=["Gerenciamento de Arquivos"])
async def move_item(item_name: str, target_directory: str):
    try:
        item_path = Path(UPLOAD_DIRECTORY) / item_name
        target_path = Path(UPLOAD_DIRECTORY) / target_directory / item_name
        if not item_path.exists():
            raise HTTPException(status_code=404, detail="Item not found")
        if not (Path(UPLOAD_DIRECTORY) / target_directory).exists():
            raise HTTPException(status_code=404, detail="Target directory not found")
        shutil.move(str(item_path), str(target_path))
        return JSONResponse(content={"item_name": item_name, "target_directory": target_directory, "status": "moved successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/filetree/", tags=["Estrutura de Arquivos"])
async def get_file_tree():
    def build_tree(path):
        tree = {}
        for item in path.iterdir():
            if item.is_dir():
                tree[item.name] = build_tree(item)
            else:
                tree[item.name] = None
        return tree

    try:
        base_path = Path(UPLOAD_DIRECTORY)
        file_tree = build_tree(base_path)
        return JSONResponse(content=file_tree)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/files/", response_class=HTMLResponse, tags=["Interface de Usuário"])
async def list_files(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})

@app.get("/monitor/", tags=["Monitoramento"])
async def monitor_files():
    try:
        base_path = Path(UPLOAD_DIRECTORY)
        num_files = 0
        total_size = 0
        image_files = 0
        video_files = 0
        pdf_files = 0
        excel_files = 0
        word_files = 0
        powerpoint_files = 0

        for file_path in base_path.rglob('*'):
            if file_path.is_file():
                num_files += 1
                total_size += file_path.stat().st_size

                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type:
                    if mime_type.startswith('image/'):
                        image_files += 1
                    elif mime_type.startswith('video/'):
                        video_files += 1
                    elif mime_type == 'application/pdf':
                        pdf_files += 1
                    elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                        excel_files += 1
                    elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                        word_files += 1
                    elif mime_type in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
                        powerpoint_files += 1

        response = {
            "total_files": num_files,
            "total_size": total_size,
            "image_files": image_files,
            "video_files": video_files,
            "pdf_files": pdf_files,
            "excel_files": excel_files,
            "word_files": word_files,
            "powerpoint_files": powerpoint_files
        }
        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
