FROM python:3.12-slim

# Instala PROJ y dependencias necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        proj-bin \
        proj-data \
        libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece la variable de entorno para PROJ
ENV PROJ_LIB=/usr/share/proj

# Verifica la instalación de Python y PROJ
RUN python --version && projinfo --version

# Directorio de trabajo
WORKDIR /app

# Copia tu código aquí si es necesario
# COPY . /app

CMD ["python3"]