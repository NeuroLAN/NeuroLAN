from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "User"

    id: str | None = Field(default=None, primary_key=True)
    username: str
    display_name: Optional[str] = None
    mail: str
    password: str


class SessionID(SQLModel, table=True):
    __tablename__ = "SessionID"

    id: str | None = Field(default=None, primary_key=True)
    session_id: str
    created_at: int = Field(default=int(datetime.now().timestamp()))
    expires_at: int
