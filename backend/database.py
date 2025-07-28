from sqlmodel import Field, SQLModel, create_engine, Session, select
import uuid

from backend.models import *

sqlite_file_name = ".db/NeuroLAN.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine) # Creates tables. But if table is there, doesn't re-create.

def is_user_exists(mail: str, username: str = None):
    with Session(engine) as session:
        existing_items: dict[str, bool] = {
            "username": False,
            "mail": False
        }

        statement_mail = select(User).where(User.mail == mail)
        result_mail = session.exec(statement_mail).first()

        if result_mail is not None:
            existing_items["mail"] = True

        if username is not None:
            statement_username = select(User).where(User.username == username)
            result_username = session.exec(statement_username).first()

            if result_username is not None:
                existing_items["username"] = True

        return existing_items


def create_user(username:str, mail: str, password: str):
    user: User = User()

    user.id = str(uuid.uuid4())
    user.username = username
    user.mail = mail
    user.password = password

    try:
        with Session(engine) as session:
            session.add(user)

            session.commit()
    except Exception as e:
        print(f"Hata: {e}")

    return True


def find_user(username: str = None, mail: str = None):
    with Session(engine) as session:
        if username is not None:
            statement = select(User).where(User.username == username)
            result = session.exec(statement)

            return result.first()

        if mail is not None:
            statement = select(User).where(User.mail == mail)
            result = session.exec(statement)

            return result.first()