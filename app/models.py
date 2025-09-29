import datetime
from typing import Any

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, String, func

from app.db import Model, engine


class Task(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
    title: Mapped[str] = mapped_column(String(255), nullable= False)
    description: Mapped[str|None] = mapped_column(String(4000), nullable= True, default=None)
    completed: Mapped[bool] = mapped_column(Boolean, nullable= False, default= False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    def __repr__(self) -> str:
        return f"Task[{self.id} - {self.title} - {self.created_at}]"
    

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    # email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(60), nullable=False) 
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),  server_default=func.now(), nullable= False
    )


    def __repr__(self) -> str:
        # return f"User[id:{self.id}, name: {self.username}, email: {self.email}, created_at: {self.created_at}]"
        return f"User[id:{self.id}, name: {self.username}, created_at: {self.created_at}]"
    

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            # 'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }