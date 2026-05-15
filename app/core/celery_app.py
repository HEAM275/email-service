import os
from celery import Celery

# Cargar variables desde .env si usas python-dotenv
from dotenv import load_dotenv
load_dotenv()

broker_url = os.getenv("CELERY_BROKER_URL")
backend_url = os.getenv("CELERY_RESULT_BACKEND")


celery_app = Celery(
    "email_sender",
    broker=broker_url,
    backend=backend_url,
    include=["app.tasks.email_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_queues={
        "email_tasks": {"exchange": "email_tasks", "routing_key": "email_tasks"},
    },
    task_default_queue="email_tasks",
    task_default_routing_key="email_tasks",
)