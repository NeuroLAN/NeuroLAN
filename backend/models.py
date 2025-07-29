from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime

class User(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    username: str
    mail: str
    password: str


class SessionID(SQLModel, table=True):
    __tablename__ = "SessionID"

    id: str | None = Field(default=None, primary_key=True)
    session_id: str
    created_at: int = Field(default=datetime.now().second)
    expires_at: int
