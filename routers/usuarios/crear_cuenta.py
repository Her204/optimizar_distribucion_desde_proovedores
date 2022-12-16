from typing import List
from .forms import SigninForm
from dependencies import get_db
from sqlalchemy.orm import Session
#from models.usuario import Usuario
from sqlalchemy.exc import IntegrityError
from fastapi_csrf_protect import CsrfProtect
from fastapi.templating import Jinja2Templates
from schemas import usuarios as usuarios_schemas
from services.usuarios import main as usuarios_services
from fastapi import responses, Depends, APIRouter, Request, status

router = APIRouter(prefix="/crear_cuenta", tags=["crear_cuenta"])

templates = Jinja2Templates(directory="templates")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/")
def crear_cuenta(request: Request):
    return templates.TemplateResponse("auth/signin.html", {"request": request})


@router.post("/")
async def crear_cuenta(request: Request, db: Session = Depends(get_db)):
    form = SigninForm(request)
    await form.load_data()
    if await form.is_valid():
        usuario = usuarios_schemas.UsuarioCreate(
                nombre_de_usuario=form.usuario,
                correo_de_usuario=form.correo,
                pais=form.pais,
                ciudad=form.ciudad,
                contrasenia_encriptada=form.password
            )
        try:
            usuario = usuarios_services.crear_usuario(db=db,user=usuario)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            form.__dict__.get("errors").append("Nombre de usuario o correo duplicado")
            return templates.TemplateResponse("users/signin.html", form.__dict__)
    return templates.TemplateResponse("auth/signin.html", form.__dict__)


