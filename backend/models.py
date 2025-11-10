from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import uuid
from database import Base

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(String)
    bot_response = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    