### 1. **Rota Principal (Página de Upload)**
- **Método**: GET
- **Endpoint**: `/`
- **Descrição**: Retorna a página HTML principal para o upload de arquivos.
- **Resposta**: HTML da página `index.html`.

**Uso**: Acesse o endereço base do servidor (ex.: `http://localhost:8000/`) no navegador para visualizar a página de upload de arquivos.

### 2. **Upload de Arquivo**
- **Método**: POST
- **Endpoint**: `/uploadfile/`
- **Descrição**: Permite o upload de um arquivo.
- **Parâmetros**: `file` (UploadFile) - O arquivo a ser carregado.
- **Resposta**: JSON com o nome do arquivo e status de sucesso ou erro.

**Uso**: Faça uma solicitação POST para `http://localhost:8000/uploadfile/` com o arquivo como dado do formulário.

### 3. **Criar Diretório**
- **Método**: POST
- **Endpoint**: `/createdir/`
- **Descrição**: Cria um novo diretório.
- **Parâmetros**: `directory_name` (str) - O nome do diretório a ser criado.
- **Resposta**: JSON com o caminho do diretório e status de sucesso ou erro.

**Uso**: Faça uma solicitação POST para `http://localhost:8000/createdir/` com um JSON no corpo contendo o nome do diretório:
```json
{
    "directory_name": "novo_diretorio"
}
```

### 4. **Pesquisar Arquivos e Diretórios**
- **Método**: GET
- **Endpoint**: `/search/`
- **Descrição**: Pesquisa arquivos e diretórios com base em um termo de pesquisa.
- **Parâmetros**: `search_term` (str) - O termo de pesquisa.
- **Resposta**: JSON com uma lista de correspondências.

**Uso**: Faça uma solicitação GET para `http://localhost:8000/search/?search_term=termo`.

### 5. **Renomear Arquivo ou Diretório**
- **Método**: PUT
- **Endpoint**: `/rename/`
- **Descrição**: Renomeia um arquivo ou diretório.
- **Parâmetros**: `old_name` (str) - O nome atual do arquivo ou diretório.
              `new_name` (str) - O novo nome.
- **Resposta**: JSON com os nomes antigo e novo e status de sucesso ou erro.

**Uso**: Faça uma solicitação PUT para `http://localhost:8000/rename/` com um JSON no corpo contendo os nomes antigo e novo:
```json
{
    "old_name": "nome_antigo.txt",
    "new_name": "nome_novo.txt"
}
```

### 6. **Apagar Arquivo ou Diretório**
- **Método**: DELETE
- **Endpoint**: `/delete/`
- **Descrição**: Apaga um arquivo ou diretório.
- **Parâmetros**: `item_name` (str) - O nome do arquivo ou diretório a ser apagado.
- **Resposta**: JSON com o nome do item e status de sucesso ou erro.

**Uso**: Faça uma solicitação DELETE para `http://localhost:8000/delete/` com um JSON no corpo contendo o nome do item:
```json
{
    "item_name": "nome_do_arquivo.txt"
}
```

### 7. **Mover Arquivo ou Diretório**
- **Método**: POST
- **Endpoint**: `/move/`
- **Descrição**: Move um arquivo ou diretório para outro diretório.
- **Parâmetros**: `item_name` (str) - O nome do arquivo ou diretório a ser movido.
              `target_directory` (str) - O diretório de destino.
- **Resposta**: JSON com o nome do item, diretório de destino e status de sucesso ou erro.

**Uso**: Faça uma solicitação POST para `http://localhost:8000/move/` com um JSON no corpo contendo o nome do item e o diretório de destino:
```json
{
    "item_name": "nome_do_arquivo.txt",
    "target_directory": "diretorio_destino"
}
```

### 8. **Árvore de Arquivos e Diretórios**
- **Método**: GET
- **Endpoint**: `/filetree/`
- **Descrição**: Retorna uma estrutura hierárquica de todos os arquivos e diretórios.
- **Resposta**: JSON representando a árvore de diretórios.

**Uso**: Faça uma solicitação GET para `http://localhost:8000/filetree/`.

### 9. **Lista de Arquivos (HTML)**
- **Método**: GET
- **Endpoint**: `/files/`
- **Descrição**: Retorna uma página HTML listando todos os arquivos.
- **Resposta**: HTML da página `files.html`.

**Uso**: Acesse `http://localhost:8000/files/` no navegador para visualizar a lista de arquivos.

### 10. **Monitoramento de Arquivos**
- **Método**: GET
- **Endpoint**: `/monitor/`
- **Descrição**: Retorna informações sobre os arquivos no diretório.
- **Resposta**: JSON com as seguintes informações:
  - `total_files`: Número total de arquivos.
  - `total_size`: Tamanho total do diretório em bytes.
  - `image_files`: Quantidade de arquivos de imagem.
  - `video_files`: Quantidade de arquivos de vídeo.
  - `pdf_files`: Quantidade de arquivos PDF.
  - `excel_files`: Quantidade de arquivos de planilha (Excel).
  - `word_files`: Quantidade de arquivos de texto (Word).
  - `powerpoint_files`: Quantidade de arquivos de apresentação (PowerPoint).

**Uso**: Faça uma solicitação GET para `http://localhost:8000/monitor/`.

Essas rotas cobrem diversas funcionalidades para gerenciar e monitorar arquivos e diretórios em um servidor utilizando FastAPI.
