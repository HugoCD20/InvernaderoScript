# Invernadero Script

Este proyecto consiste en un script de Python diseñado para sincronizar datos de temperatura y humedad desde Firebase Realtime Database hacia Firestore, además de proporcionar un endpoint de verificación de estado (health check).

## ⚠️ IMPORTANTE: Credenciales

**Este proyecto requiere un archivo de credenciales de servicio de Firebase para funcionar.**

El archivo debe ubicarse en: `credentials/credenciales.json`

> **NOTA:** Las credenciales incluidas en este repositorio (si las hay) son de ejemplo o inválidas y **serán borradas**. Debes generar tus propias credenciales desde la consola de Firebase (Project Settings > Service Accounts > Generate New Private Key) y colocar el archivo JSON descargado en la ruta mencionada.

## Características

- **Sincronización de Datos**: Lee periódicamente (cada hora) los valores de `Temperatura` y `Humedad` desde Realtime Database y los guarda como un nuevo documento en la colección `Temperatura` de Firestore, añadiendo la fecha y hora actual.
- **Endpoint de Health Check**: Expone una ruta `/ping` que devuelve un estado 200 OK, útil para mantener el servicio activo en plataformas como Render.
- **Dockerizado**: Incluye un `Dockerfile` para facilitar su despliegue en contenedores.

## Requisitos Previos

- Python 3.10 o superior.
- Una cuenta de Google Cloud / Firebase con un proyecto activo.
- Realtime Database y Firestore habilitados en el proyecto de Firebase.

## Configuración y Uso

### Ejecución Local

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd InvernaderoScript
    ```

2.  **Configurar Credenciales:**
    Asegúrate de tener tu archivo `credenciales.json` en la carpeta `credentials/`.

3.  **Instalar dependencias:**
    Se recomienda usar un entorno virtual.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el script:**
    ```bash
    python script.py
    ```
    El servidor Flask iniciará (por defecto en el puerto 5000) y el hilo de sincronización comenzará a funcionar en segundo plano.

### Ejecución con Docker

1.  **Construir la imagen:**
    ```bash
    docker build -t invernadero-script .
    ```

2.  **Correr el contenedor:**
    ```bash
    docker run -p 5000:5000 invernadero-script
    ```

## Variables de Entorno

- `PORT`: Puerto en el que escuchará el servidor Flask (por defecto `5000`).
