import asyncio
from app.core.celery_app import celery_app
from app.utils.email import send_email_async
from pydantic import EmailStr

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def send_email_task(self, to_email: str, subject: str, body: str):
    # Ejecutar la función async dentro del worker de Celery
    asyncio.run(send_email_async([to_email], subject, body))