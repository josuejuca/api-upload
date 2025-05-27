from fastapi import FastAPI, File, UploadFile, Request, HTTPException, Form

from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from uuid import uuid4
import shutil
import sqlite3
import mimetypes

app = FastAPI()

# Diretórios
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIRECTORY = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "file_metadata.db"
TEMPLATES_DIR = BASE_DIR / "templates"

# Cria diretório de uploads se não existir
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Inicializa o banco se necessário
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name TEXT NOT NULL,
            stored_name TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Templates e arquivos estáticos
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")


@app.get("/", response_class=HTMLResponse, tags=["Interface de Usuário"])
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/uploaded-list/", tags=["Arquivos"])
async def get_uploaded_file_list():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT original_name, stored_name FROM files ORDER BY upload_time DESC")
        rows = cursor.fetchall()
        conn.close()
        return {stored: original for original, stored in rows}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.post("/uploadfile/", tags=["Gerenciamento de Arquivos"])
async def upload_file(file: UploadFile = File(...)):
    try:
        # Gera nome único
        ext = Path(file.filename).suffix
        stored_name = f"{uuid4().hex}{ext}"
        file_location = UPLOAD_DIRECTORY / stored_name

        # Salva arquivo
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Salva no banco
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO files (original_name, stored_name) VALUES (?, ?)",
            (file.filename, stored_name)
        )
        conn.commit()
        conn.close()

        # Redireciona com mensagem flash simulada (via query param)
        return RedirectResponse(url="/files?success=true", status_code=HTTP_303_SEE_OTHER)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/files/", response_class=HTMLResponse, tags=["Interface de Usuário"])
async def list_files(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


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
        return JSONResponse(content=build_tree(UPLOAD_DIRECTORY))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/createdir/", tags=["Gerenciamento de Diretórios"])
async def create_directory(directory_name: str):
    try:
        dir_path = UPLOAD_DIRECTORY / directory_name
        dir_path.mkdir(parents=True, exist_ok=True)
        return JSONResponse(content={"directory": str(dir_path), "status": "created successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/search/", tags=["Pesquisa"])
async def search_files_and_directories(search_term: str):
    try:
        matches = [str(p) for p in UPLOAD_DIRECTORY.rglob("*") if search_term in p.name]
        return JSONResponse(content={"matches": matches})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.put("/rename/", tags=["Gerenciamento de Arquivos"])
async def rename_item(old_name: str, new_name: str):
    try:
        old_path = UPLOAD_DIRECTORY / old_name
        new_path = UPLOAD_DIRECTORY / new_name
        if not old_path.exists():
            raise HTTPException(status_code=404, detail="Item not found")
        old_path.rename(new_path)
        return JSONResponse(content={"old_name": old_name, "new_name": new_name, "status": "renamed successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.delete("/delete/", tags=["Gerenciamento de Arquivos"])
async def delete_item(item_name: str):
    try:
        item_path = UPLOAD_DIRECTORY / item_name
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
        item_path = UPLOAD_DIRECTORY / item_name
        target_path = UPLOAD_DIRECTORY / target_directory / item_name
        if not item_path.exists():
            raise HTTPException(status_code=404, detail="Item not found")
        if not (UPLOAD_DIRECTORY / target_directory).exists():
            raise HTTPException(status_code=404, detail="Target directory not found")
        shutil.move(str(item_path), str(target_path))
        return JSONResponse(content={"item_name": item_name, "target_directory": target_directory, "status": "moved successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.get("/monitor/", tags=["Monitoramento"])
async def monitor_files():
    try:
        total_size = 0
        counts = {
            "total_files": 0,
            "image_files": 0,
            "video_files": 0,
            "pdf_files": 0,
            "excel_files": 0,
            "word_files": 0,
            "powerpoint_files": 0,
        }

        for file_path in UPLOAD_DIRECTORY.rglob('*'):
            if file_path.is_file():
                counts["total_files"] += 1
                total_size += file_path.stat().st_size

                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type:
                    if mime_type.startswith('image/'):
                        counts["image_files"] += 1
                    elif mime_type.startswith('video/'):
                        counts["video_files"] += 1
                    elif mime_type == 'application/pdf':
                        counts["pdf_files"] += 1
                    elif mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                        counts["excel_files"] += 1
                    elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                        counts["word_files"] += 1
                    elif mime_type in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
                        counts["powerpoint_files"] += 1

        counts["total_size"] = total_size
        return JSONResponse(content=counts)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
