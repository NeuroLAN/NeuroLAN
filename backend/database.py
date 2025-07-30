from sqlmodel import Field, SQLModel, create_engine, Session, select
import uuid
from argon2 import PasswordHasher   
from datetime import datetime, timedelta

from backend.models import *

ph = PasswordHasher()

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


def create_user(username: str, display_name: str | None, mail: str, password: str):
    ph = PasswordHasher()
    user = User()

    with Session(engine) as session:
        while True:
            user.id = str(uuid.uuid4())
            result = session.exec(select(User).where(User.id == user.id)).first()
            if result is None:
                break

        user.username = username.lower()
        user.display_name = display_name or user.username
        user.mail = mail
        user.password = ph.hash(password)

        try:
            session.add(user)
            session.commit()
            return {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "email": user.mail
            }
        except Exception as e:
            print(f"Error: {e}")
            return None


def find_user(username: str = None, mail: str = None, id: str = None):
    parameters = [username, mail, id]

    with Session(engine) as session:
        if parameters.count(None) < 2:
            raise ValueError("Only one of username or mail or id should be provided.")

        if username is not None:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()

            return {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "email": user.mail
            }

        if mail is not None:
            statement = select(User).where(User.mail == mail)
            user = session.exec(statement).first()

            return {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "email": user.mail
            }

        if id is not None:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()

            return {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "email": user.mail
            }
    

def generate_session_id(user_id: str):
    session_id = SessionID()

    session_id.id = user_id
    session_id.session_id = str(uuid.uuid4())
    session_id.created_at = int(datetime.utcnow().timestamp())
    session_id.expires_at = int((datetime.utcnow() + timedelta(days=30)).timestamp())

    try:
        with Session(engine) as session:
            session.add(session_id)

            session.commit()

            return session_id.session_id
    except Exception as e:
        print(f"Error: {e}")
        return None


def is_session_id_active(client_session_id: str, user_id: str):
    if client_session_id is None or user_id is None:
            return False

    with Session(engine) as session:
        statement = select(SessionID).where(SessionID.id == user_id, SessionID.session_id == client_session_id)
        filtered_session_id = session.exec(statement).first()

        if filtered_session_id is None:
            return False

        if filtered_session_id.session_id == client_session_id:
            if int(datetime.utcnow().timestamp()) < filtered_session_id.expires_at:
                return True
            else:
                session.delete(filtered_session_id)
                session.commit()

                return False
        return False
        