# Project 2 – Django API + Redis + Workers (Docker)

Este proyecto extiende el sistema distribuido de procesamiento de imágenes agregando una API en Django como intermediario HTTP REST <=> Redis.

## 🏗 Arquitectura

El flujo del sistema es:

Postman / Cliente HTTP  
        ↓  
Django API (REST)  
        ↓  
Redis (cola de tareas)  
        ↓  
Workers (procesamiento paralelo)  
        ↓  
Carpeta output (imagen procesada)

La API recibe una solicitud HTTP POST, crea una tarea en Redis y los workers la procesan de forma asíncrona.

---

## 📦 Servicios en Docker Compose

- redis → Cola distribuida
- worker-1
- worker-2
- worker-3 → Procesamiento paralelo
- api → Django (intermediario HTTP REST)

---

## 🚀 Cómo ejecutar el proyecto

Desde la raíz del proyecto:


docker-compose up --build

## Verificar que todos los contenedores estén activos:

docker ps

## 📡 Probar la API
Endpoint
POST http://localhost:8000/tasks/
Headers
Content-Type: application/json
Body (JSON)
{
  "input_path": "images/sample.jpg",
  "output_path": "output/test_api.jpg",
  "filters": [
    { "type": "grayscale" }
  ]
}
## ✅ Resultado esperado

La API responde con:

{
  "message": "Task created successfully",
  "task_id": "UUID_GENERADO"
}

En los logs se observa el worker procesando la tarea.

Se genera la imagen procesada en la carpeta:

output/test_api.jpg
## 📂 Estructura del Proyecto
.
├── api/                # Proyecto Django
├── workers/            # Workers de procesamiento
├── images/             # Imágenes de entrada
├── output/             # Imágenes procesadas
├── docker-compose.yml
└── Dockerfile

## 📸 Evidencias

### Contenedores activos

![Docker PS](docs/images/docker-ps.png)

### Respuesta en Postman

![Postman](docs/images/postman-response.png)

### Logs de procesamiento

![Logs](docs/images/worker-logs.png)

### Imagen procesada

![Output](docs/images/output-image.png)
```bash