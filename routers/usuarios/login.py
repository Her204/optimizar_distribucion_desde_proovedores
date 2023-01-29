import os
import requests
from typing import List
from .forms import LoginForm
from datetime import timedelta
from dependencies import get_db
from sqlalchemy.orm import Session
#from models.usuario import Usuario
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi.templating import Jinja2Templates
from schemas import usuarios as usuarios_schemas
from fastapi.security import OAuth2PasswordRequestForm
from services.usuarios import main as usuarios_services
from fastapi import Depends, APIRouter, HTTPException, Request, status, Response

router = APIRouter(prefix="/login", tags=["login"])

templates = Jinja2Templates(directory="templates")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@CsrfProtect.load_config
def get_csrf_config():
  return usuarios_schemas.CsrfSettings()



@router.post("/token", response_model=usuarios_schemas.Token)
def login_para_acceder_token(response: Response,
                             db : Session = Depends(get_db),
                             form_data: OAuth2PasswordRequestForm = Depends()):

    user = usuarios_services.autentificar_usuario(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = usuarios_services.crear_acceso_al_token(
        data={"sub": user.nombre_de_usuario}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    response.set_cookie(
        key="nombre_de_usuario",value=user.nombre_de_usuario,httponly=True
    )
    return response#{"access_token": access_token, "token_type": "bearer"}


@router.get("/")
def login(request: Request):
       return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/csrftoken")
async def get_csrf_token(csrf_protect:CsrfProtect = Depends()):
    response = JSONResponse(status_code=200, content={'csrf_token':os.environ.get("TOKEN_ALTOQ")})
    csrf_protect.set_csrf_cookie(response)
    print(response)
    return response

@router.post("/")
async def login(request: Request, db: Session = Depends(get_db),
                ):
    form = LoginForm(request)

    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Inicio de sesion satisfactoria :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            
            response = login_para_acceder_token(response=response,form_data=form, db=db)
            print(response.headers)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Correo o Password incorrecto")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)