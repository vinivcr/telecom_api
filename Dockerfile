# Usar a imagem base oficial do Python
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos necessários para dentro do container
COPY . /app

# Instalar as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta em que a aplicação irá rodar
EXPOSE 8000

# Definir o comando que será executado para rodar a aplicação
CMD ["python", "app.py"]
