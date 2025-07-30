from typing import Annotated

from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.models import *
from backend.database import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="frontend/templates")


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request
):
    return templates.TemplateResponse(
        name="home.html",
        context={
            "request": request
        }
    )


@app.get("/signin", response_class=HTMLResponse)
async def signin_get(
    request: Request
):
    client_session_id = request.cookies.get("session_id")
    client_user_id = request.cookies.get("user_id")

    _is_session_id_active = is_session_id_active(client_session_id, client_user_id)

    if _is_session_id_active:
        print("Session ID correct.")
        return templates.TemplateResponse(
            name="you.html",
            context={
                "request": request
            }
        )

    return templates.TemplateResponse(
        name="signin.html",
        context={
            "request": request
        }
    )


@app.get("/signup", response_class=HTMLResponse)
async def signup_get(
    request: Request
):
    client_session_id = request.cookies.get("session_id")
    client_user_id = request.cookies.get("user_id")

    _is_session_id_active = is_session_id_active(client_session_id, client_user_id)

    if _is_session_id_active:
        print("Session ID correct.")
        return templates.TemplateResponse(
            name="you.html",
            context={
                "request": request
            }
        )

    return templates.TemplateResponse(
        name="signup.html",
        context={
            "request": request
        }
    )


@app.post("/signup")
async def signup_post(
    response: Response,
    request: Request,
    username: Annotated[str, Form()],
    display_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    existing_items = is_user_exists(email, username)

    if True in existing_items.values():
        return templates.TemplateResponse(
            name="signup.html",
            context={
                "request": request,
                "username_exists": existing_items["username"],
                "mail_exists": existing_items["mail"]
            }
        )

    created_user = create_user(username, display_name, email, password)

    if created_user is not None:
        session_id = generate_session_id(created_user["id"])

        response = templates.TemplateResponse(
            name="you.html",
            context={"request": request}
        )

        response.set_cookie( # sets cookie for client.
            key="session_id", # cookie's key for accessing later
            value=session_id,  # cookie's value
            httponly=True, # no javascript
            samesite="Lax", 
            max_age=60*60*24*30 # expiring in 1 month (in seconds)
        )

        response.set_cookie(
            key="user_id",
            value=created_user["id"],
            httponly=True,
            samesite="Lax",
            max_age=86400000
        )

        return response


@app.post("/signin", response_class=RedirectResponse)
async def signin_post(
    response: Response,
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    user = find_user(mail=email)

    if user.password == password:
        session_id = generate_session_id(user.id)

        response = RedirectResponse("/you")

        response.set_cookie( # sets cookie for client.
            key="session_id", # cookie's key for accessing later
            value=session_id,  # cookie's value
            httponly=True, # no javascript
            samesite="Lax", 
            max_age=60*60*24*30 # expiring in 1 month (in seconds)
        )

        response.set_cookie(
            key="user_id",
            value=user.user_id,
            httponly=True,
            samesite="Lax",
            max_age=86400000
        )

        return response
    return templates.TemplateResponse(
        name="signin.html",
        context={
            "request": request,
            "error": True
        }
    )


@app.get("/you", response_class=HTMLResponse)
async def you_page(
    request: Request
):
    client_session_id = request.cookies.get("session_id")
    client_user_id = request.cookies.get("user_id")

    _is_session_id_active = is_session_id_active(client_session_id, client_user_id)

    if _is_session_id_active:
        print("Session ID correct.")
    else:
        return templates.TemplateResponse(
            name="signin.html",
            context={
                "request": request
            }
        )

    user_details: User = find_user(id=client_user_id)

    print(user_details["display_name"])

    return templates.TemplateResponse(
        name="you.html",
        context={
            "request": request,
            "user_id": user_details["id"],
            "username": user_details["username"],
            "display_name": user_details["display_name"]
        }
    )