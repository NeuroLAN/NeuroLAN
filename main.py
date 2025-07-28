from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.models import *
from backend.database import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="home.html", request=request
    )

@app.get("/signin", response_class=HTMLResponse)
async def signin_get(request: Request):
    return templates.TemplateResponse(
        name="signin.html", request=request
    )

@app.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse(
        name="signup.html", request=request
    )

@app.post("/signup")
async def signup_post(
    request: Request,
    username: Annotated[str, Form()],
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

    if create_user(username, email, password):
        return templates.TemplateResponse(
            name="me.html",
            context={"request": request}
        )


@app.post("/signin")
async def signin_post(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    user = find_user(mail=email)

    if user.password == password:
        return templates.TemplateResponse(
            name="me.html",
            context={"request": request}
        )
    return templates.TemplateResponse(
        name="signin.html",
        context={
            "request": request,
            "error": True
        }
    )