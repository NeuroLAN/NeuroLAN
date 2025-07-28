from sqlmodel import Field, SQLModel, create_engine, Session, select

class User(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    username: str
    mail: str
    password: str

