import os
import openai
from starlette.config import Config
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schema import EmailRequest, EmailResponse, EmailLogCreate, EmailLogRead
from database import get_session
from crud import crud_email_logs

# Load .env
current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, ".env")
config = Config(env_path)
OPENAI_API_KEY = config("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Routers
email_router = APIRouter()
log_router = APIRouter()

# ----------- Email Generator -----------
@email_router.post("/", response_model=EmailResponse, summary="Generate an email using OpenAI")
async def generate_email(
    request: EmailRequest,
    db: AsyncSession = Depends(get_session)
):
    try:
        system_prompt = (
            "You are a helpful email assistant. "
            "You get a prompt to write an email, "
            "you reply with the email and nothing else."
        )

        user_prompt = f"""
        Write an email based on the following input:
        - User Input: {request.user_input}
        - Reply To: {request.reply_to or 'N/A'}
        - Context: {request.context or 'N/A'}
        - Length: {request.length or 'N/A'} characters
        - Tone: {request.tone or 'N/A'}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=request.length or 300
        )

        generated_email = response.choices[0].message["content"].strip()

        # Save to DB
        log_entry = EmailLogCreate(
            user_input=request.user_input,
            reply_to=request.reply_to,
            context=request.context,
            length=request.length,
            tone=request.tone,
            generated_email=generated_email
        )
        await crud_email_logs.create(db, log_entry)

        return EmailResponse(generated_email=generated_email)

    except openai.error.OpenAIError as oe:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {oe}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ----------- Email Health Check -----------
@email_router.get("/health", summary="Check if email assistant is ready")
async def email_health_check():
    if OPENAI_API_KEY:
        return {"email": "ready"}
    else:
        return {"email": "not_ready"}


# ----------- Email Logs -----------
@log_router.get("/", summary="List all email logs")
async def read_logs(db: AsyncSession = Depends(get_session)):
    logs = await crud_email_logs.get_multi(db)
    return logs

@log_router.get("/{log_id}", response_model=EmailLogRead, summary="Get a specific log by ID")
async def read_log(log_id: int, db: AsyncSession = Depends(get_session)):
    log = await crud_email_logs.get(db, id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
