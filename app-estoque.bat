@echo off
REM 1. Mudar para o diretório do script
cd "C:\Users\User\Documents\Nova pasta\app-estoque"

REM 2. Ativar o ambiente virtual (Ajuste o caminho se necessário)
call venv\Scripts\activate.bat

REM 3. Rodar o Streamlit
start streamlit run app.py