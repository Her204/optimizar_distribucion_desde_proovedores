import os
from typing import List
from datetime import timedelta
from dependencies import get_db
from sqlalchemy.orm import Session
#from models.usuario import Usuario
from .forms import LoginForm, SigninForm
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from schemas import usuarios as usuarios_schemas
from fastapi.security import OAuth2PasswordRequestForm
from services.usuarios import main as usuarios_services
from fastapi import responses, Depends, APIRouter, HTTPException, Request, status, Response

router = APIRouter(prefix="/usuario", tags=["usuario"])

templates = Jinja2Templates(directory="templates")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token", response_model=usuarios_schemas.Token)
def login_para_acceder_token(response: Response,
                             db : Session = Depends(get_db),
                             form_data: OAuth2PasswordRequestForm = Depends()):
    
    print(form_data.username)
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
    print(access_token)
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/crear/", response_model=usuarios_schemas.Usuario)
def crear_usuario(usuario: usuarios_schemas.UsuarioCreate, db: Session = Depends(get_db)):
     db_user = usuarios_services.obtener_usuario_por_nombre(db, nombre_de_usuario=usuario.nombre_de_usuario)
     if db_user:
         raise HTTPException(status_code=400, detail="Email or Username already registered") 
     return usuarios_services.crear_usuario(db=db, user=usuario) 

@router.get("/todos_los_usuarios/", response_model=List[usuarios_schemas.Usuario]) 
def leer_usuarios(skip: int = 0, limite: int = 100, db: Session = Depends(get_db)):
    users = usuarios_services.obtener_varios_usuarios(db, skip=skip, limite=limite) 
    return users

@router.get("/usuarios/usuario_autenticado/", response_model=usuarios_schemas.Usuario)
async def leer_mi_usuario(current_user: usuarios_schemas.Usuario = Depends(usuarios_services.obtener_usuario_activo_actual)):
    return current_user

@router.get("/usuarios/{usuario_id}", response_model=usuarios_schemas.Usuario)
def leer_un_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = usuarios_services.obtener_usuario(db, usuario_id=usuario_id) 
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found") 
    return db_user

@router.get("/inicio_sesion/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/inicio_sesion/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Inicio de sesion satisfactoria :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_para_acceder_token(response=response,form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Correo o Password incorrecto")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)

@router.get("/crear_cuenta/")
def signin(request: Request):
    return templates.TemplateResponse("auth/signin.html", {"request": request})


@router.post("/crear_cuenta/")
async def signin(request: Request, db: Session = Depends(get_db)):
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