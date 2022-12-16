import os
from typing import List
from datetime import timedelta
from dependencies import get_db
from sqlalchemy.orm import Session
#from models.usuario import Usuario
from .forms import LoginForm, SigninForm
from sqlalchemy.exc import IntegrityError
from fastapi_csrf_protect import CsrfProtect
from fastapi.templating import Jinja2Templates
from schemas import usuarios as usuarios_schemas
from fastapi.security import OAuth2PasswordRequestForm
from services.usuarios import main as usuarios_services
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi import responses, Depends, APIRouter, HTTPException, Request, status, Response

router = APIRouter(prefix="/usuario", tags=["usuario"])


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

@router.get("/usuarios/yo/", response_model=usuarios_schemas.Usuario)
async def leer_mi_usuario(current_user: usuarios_schemas.Usuario = Depends(usuarios_services.obtener_usuario_activo_actual)):
    return current_user

@router.get("/usuarios/{usuario_id}", response_model=usuarios_schemas.Usuario)
def leer_un_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = usuarios_services.obtener_usuario(db, usuario_id=usuario_id) 
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found") 
    return db_user
