# Usar a imagem oficial do Python
FROM python:3.9

# Definir diretório de trabalho
WORKDIR /app

COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do diretório local para o contêiner
COPY . .

EXPOSE 8091

CMD ["streamlit", "run", "app.py", "--server.port=8091", "--server.enableCORS=false"]
