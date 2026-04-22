from sqlalchemy import Column, Integer, String, Boolean, text, DateTime
from sqlalchemy.sql import func
from .db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("true"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )