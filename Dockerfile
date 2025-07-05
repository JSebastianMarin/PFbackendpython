FROM python:3.11-slim

# Argumentos de build-time
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG SECRET_KEY
ARG DEBUG


# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /movimientos_financieros

# Copiar requirements primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Convertir el archivo entrypoint.sh a formato Unix y hacerlo ejecutable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Establecer variables de entorno desde los argumentos
ENV DB_NAME
    DB_USER
    DB_PASSWORD
    DB_HOST
    SECRET_KEY
    DEBUG

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]