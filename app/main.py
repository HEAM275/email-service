from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.email import router as email_router

load_dotenv()

app = FastAPI(title="Email Service API")

app.include_router(email_router)

@app.get("/")
async def root():
    return{"service": "Email Sender API", "status": "running"}