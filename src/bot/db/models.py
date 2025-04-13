from datetime import datetime

from sqlalchemy import text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Feedback(Base):
    __tablename__ = 'feedbacks'
    id: Mapped[int] = mapped_column(primary_key=True)
    feedback: Mapped[str]
    written_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
