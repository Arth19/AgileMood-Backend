# FastAPI + SQLite

Este repositório contém um projeto baseado em **FastAPI** que se comunica com um banco de dados **SQLite**.

## 📌 Requisitos

Certifique-se de ter os seguintes requisitos instalados antes de executar o projeto:

- Python 3.9+
- Virtualenv (opcional, mas recomendado)

## 🚀 Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Executando a API

Para iniciar o servidor, execute o seguinte comando:

```bash
fastapi dev main.py
```

A API estará disponível em `http://127.0.0.1:8000`.

### 📜 Documentação Interativa

Após iniciar a API, você pode acessar a documentação interativa gerada automaticamente pelo FastAPI:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🗄️ Banco de Dados

Este projeto utiliza **SQLite** como banco de dados. O arquivo do banco de dados será gerado automaticamente ao rodar a API.

Caso queira gerenciar o banco, você pode utilizar ferramentas como:

- [DB Browser for SQLite](https://sqlitebrowser.org/)
- `sqlite3` via terminal:
  ```bash
  sqlite3 database.db
  ```

## 📂 Estrutura do Projeto

```
📁 seu-repositorio/
│── 📄 main.py             # Arquivo principal da API
│── 📄 models.py           # Modelos do banco de dados
│── 📄 routes.py           # Definição das rotas da API
│── 📄 database.py         # Configuração da conexão SQLite
│── 📄 requirements.txt    # Dependências do projeto
```

## 🤝 Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorar este projeto.

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

# MA-24.2-Backend
