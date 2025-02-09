# FastAPI + SQLite

Este repositório contém um projeto baseado em **FastAPI** que se comunica com um banco de dados **SQLite**.

## 📌 Requisitos

Certifique-se de ter os seguintes requisitos instalados antes de executar o projeto:

- Python 3.9+
- Virtualenv (opcional, mas recomendado)

## 🚀 Instalação

Clone este repositório:

   ```bash
   git clone https://github.com/Jurupoc/MA-24.2-Backend.git
   cd MA-24.2-Backend
   ```


## 🛠 Configurar o Ambiente Virtual
Existem dois scripts disponíveis para facilitar a configuração e execução do projeto, dependendo do seu sistema operacional.

1. 🚀 **Windows** (_setup.bat_ e _run.bat_): 
No Windows, você pode usar so scripts **.bat** para configurar o ambiente virtual, instalar as dependências e rodar o servidor.
Basta dar um duplo clique no arquivo _setup.bat_ e em seguida no _run.bat_ para iniciar tudo automaticamente. 
    A API estará disponível em `http://127.0.0.1:8000`.


2. 🚀 **Linux/macOS** (_setup.sh_ e _run.sh_): No Linux/macOS, você pode usar o script .sh. Para rodá-lo, siga os seguintes passos:  
   1. **Dar permissão de execução ao script (Caso necessário):** 
   ```bash 
   chmod +x <nome_do_scrit>.sh
   ```
   2. **Executar o script de setup:**
   ```bash 
   ./setup.sh
   ```
   3. **Executar o script que inicializa a API:**
   ```bash 
   ./run.sh
   ```
  
    
  
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
📁 MA-24.2-Backend/
│── app
    │── 📁 crud
         │── 📄 __init__.py
         │── 📄 emotion_crud.py
         │── 📄 user_crud.py
    │── 📁 data_structures
         │── 📄 __init__.py
         │── 📄 emotion_data_structure.py
         │── 📄 test_emotion_data_structure.py
    │── 📁 databases # Configuração da conexão SQLite
         │── 📄 __init__.py
         │── 📄 sqlite_database.py 
    │── 📁 models # Modelos do banco de dados
         │── 📄 __init__.py
         │── 📄 emotion_record_model.py
         │── 📄 user_model.py
    │── 📁 schemas # Objetos da API (response e request)
         │── 📄 __init__.py
         │── 📄 emotion_schema.py
         │── 📄 emotion_record_schema.py
         │── 📄 user_schema.py
    │── 📁 routers # Definição das rotas da API
         │── 📄 __init__.py
         │── 📄 emotion_router.py
         │── 📄 user_router.py
    │── 📁 utils # Arquivos utilitarios
         │── 📄 __init__.py
         │── 📄 constants.py
    │── 📄 main.py  # Arquivo principal da API
    │── 📄 __init__.py
│── 📄 requirements.txt # Dependências do projeto
│── 📄 setup.bat        
│── 📄 run.bat          
│── 📄 setup.sh         
│── 📄 run.sh           
```

## 🤝 Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorar este projeto.

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

# MA-24.2-Backend
