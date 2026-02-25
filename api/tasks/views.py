import json
import uuid
import redis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Conexión a Redis (usando el nombre del servicio docker)
redis_client = redis.StrictRedis(
    host="redis",
    port=6379,
    db=0,
    decode_responses=True
)


@csrf_exempt
def create_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        # Generar ID único
        task_id = str(uuid.uuid4())
        data["task_id"] = task_id

        # Guardar task como hash
        task_key = f"image_processing_v2:task:{task_id}"
        pipe = redis_client.pipeline()

        for key, value in data.items():
            pipe.hset(task_key, key, json.dumps(value))

        # Enviar a cola pending
        pipe.lpush("image_processing_v2:pending", task_id)
        pipe.execute()

        return JsonResponse({
            "message": "Task created successfully",
            "task_id": task_id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)