# API de Upload de Arquivos com FastAPI

Esta API permite o upload de arquivos, visualização de uma lista de arquivos enviados e acesso aos arquivos enviados. A interface do usuário é construída usando Bootstrap e renderizada com Jinja2.

## Endpoints

### `GET /`

Renderiza um formulário HTML para fazer o upload de arquivos.

#### Exemplo de Requisição

```http
GET /
```

#### Exemplo de Resposta

Um formulário HTML com um campo para selecionar um arquivo e um botão para enviar.

---

### `POST /uploadfile/`

Faz o upload de um arquivo para o servidor.

#### Parâmetros

- `file` (form-data): O arquivo a ser enviado.

#### Exemplo de Requisição

```http
POST /uploadfile/
Content-Type: multipart/form-data

file: <arquivo>
```

#### Exemplo de Resposta

```json
{
    "filename": "example.txt",
    "status": "uploaded successfully"
}
```

---

### `GET /files/`

Renderiza uma página HTML que lista todos os arquivos enviados com links para acessá-los.

#### Exemplo de Requisição

```http
GET /files/
```

#### Exemplo de Resposta

Uma página HTML com uma lista de arquivos enviados.

---

### `GET /uploads/{filename}`

Serve um arquivo específico enviado anteriormente.

#### Parâmetros

- `filename`: O nome do arquivo a ser visualizado.

#### Exemplo de Requisição

```http
GET /uploads/example.txt
```

#### Exemplo de Resposta

O conteúdo do arquivo solicitado.

---

## Estrutura do Projeto

```
project/
│
├── main.py
└── templates/
    ├── index.jinja
    └── files.jinja
```

---

## Dependências

- `fastapi`
- `uvicorn`
- `jinja2`
- `aiofiles`

Para instalar as dependências, execute:

```sh
pip install fastapi uvicorn jinja2 aiofiles
```

---

## Executando a Aplicação

Para iniciar a aplicação, execute o comando:

```sh
uvicorn main:app --reload
```

A aplicação estará disponível em `http://localhost:8000/`.

---

## Exemplos de Uso

### Upload de Arquivo

1. Acesse `http://localhost:8000/`.
2. Selecione um arquivo e clique no botão "Upload".

### Listar Arquivos Enviados

1. Acesse `http://localhost:8000/files/`.
2. Veja a lista de arquivos enviados. Cada arquivo possui um link para visualizá-lo.

---

## Templates

### index.jinja

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h2>Upload File</h2>
        <form action="/uploadfile/" enctype="multipart/form-data" method="post">
            <div class="form-group">
                <label for="file">Choose file</label>
                <input type="file" class="form-control" id="file" name="file" required>
            </div>
            <button type="submit" class="btn btn-primary">Upload</button>
        </form>
    </div>
</body>
</html>
```

---

### files.jinja

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uploaded Files</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h2>Uploaded Files</h2>
        <ul class="list-group">
            {% for file in files %}
                <li class="list-group-item">
                    <a href="/uploads/{{ file }}">{{ file }}</a>
                </li>
            {% endfor %}
        </ul>
        <a href="/" class="btn btn-primary mt-3">Upload another file</a>
    </div>
</body>
</html>
```

---

## Notas

- Certifique-se de que o diretório `uploads` existe no diretório do projeto. O FastAPI irá armazenar os arquivos enviados nesse diretório.
- A aplicação está configurada para rodar na porta 8000. Você pode alterar isso no comando `uvicorn` ou na configuração do próprio `main.py`.

---

 
