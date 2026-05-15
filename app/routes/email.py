from fastapi import APIRouter, BackgroundTasks
from app.schemas import EmailRequest
from app.tasks.email_tasks import send_email_task

router = APIRouter(prefix="/email", tags=["Email"])

@router.post("/send")
async def send_email(request: EmailRequest):
    # Enviar tarea a Celery (no esperamos respuesta)
    send_email_task.delay(
        to_email=request.to_email,
        subject=request.subject,
        body=request.body
    )
    return {"message": "Email task queued successfully"}