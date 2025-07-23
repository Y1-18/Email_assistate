from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    reply_to = Column(Text, nullable=True)
    context = Column(Text, nullable=True)
    length = Column(Integer, nullable=True)
    tone = Column(String(50), nullable=True)
    generated_email = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
