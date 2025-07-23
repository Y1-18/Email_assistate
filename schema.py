from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ----------- Email Generation Request -----------
class EmailRequest(BaseModel):
    user_input: str = Field(..., example="Schedule a meeting with the marketing team next Monday.")
    reply_to: Optional[str] = Field(None, example="Thanks for the update.")
    context: Optional[str] = Field(None, example="This is related to our Q3 campaign.")
    length: Optional[int] = Field(300, example=300, description="Max tokens for email")
    tone: Optional[str] = Field("professional", example="friendly")

# ----------- Email Generation Response -----------
class EmailResponse(BaseModel):
    generated_email: str = Field(..., example="Dear Team, I hope this email finds you well...")

# ----------- Email Log for Saving to DB -----------
class EmailLogCreate(BaseModel):
    user_input: str
    reply_to: Optional[str]
    context: Optional[str]
    length: Optional[int]
    tone: Optional[str]
    generated_email: str

# ----------- Email Log Response from DB -----------
class EmailLogRead(BaseModel):
    id: int
    user_input: str
    reply_to: Optional[str]
    context: Optional[str]
    length: Optional[int]
    tone: Optional[str]
    generated_email: str
    created_at: datetime

    class Config:
        from_attributes = True
