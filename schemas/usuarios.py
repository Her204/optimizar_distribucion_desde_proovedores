from pydantic import BaseModel, EmailStr
from typing import Union
import os

class CsrfSettings(BaseModel):
  secret_key:str = os.environ.get("TOKEN_ALTOQ")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UsuarioBase(BaseModel):
    nombre_de_usuario: str
    correo_de_usuario: EmailStr
    pais: str
    ciudad: str

class MostrarUsuario(BaseModel):
    nombre_de_usuario: str
    correo_de_usuario: EmailStr
    esta_activo: bool
    es_super_usuario: bool
    class Config:
        orm_mode = True

class UsuarioCreate(UsuarioBase):
    contrasenia_encriptada: str

class Usuario(UsuarioBase):
    usuario_id: int
    
    class Config:
        orm_mode = True
