import os
from typing import List
from urllib import request
from dependencies import get_db
from sqlalchemy.orm import Session
#from fastapi_login import LoginManager
from sql_app.database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi_csrf_protect import CsrfProtect
from schemas import usuarios as usuarios_schemas
from routers.ventas import main as ventas_router
from routers.usuarios import login as login_router
from routers.usuarios import main as usuarios_router
from fastapi import FastAPI, Request, Depends,status
from routers.productos import main as productos_router
from routers.categorias import main as categorias_router
from fastapi_csrf_protect.exceptions import CsrfProtectError
from routers.templates_routes import router as templates_router
from routers.usuarios import crear_cuenta as crear_cuenta_router
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

#SECRET = os.environ.get("TOKEN_ALTOQ")

#manager = LoginManager(SECRET,"/login")

app.mount("/static", StaticFiles(directory="static/"), name="static")


@CsrfProtect.load_config
def get_csrf_config():
  return usuarios_schemas.CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    #return JSONResponse(status_code=exc.status_code, content={ 'detail':  exc.message })
	return RedirectResponse(
                "/?msg=Necesitas_autenticarte_para_acceder_a_este_endpoint", status_code=status.HTTP_302_FOUND
            )

app.include_router(login_router.router)
app.include_router(crear_cuenta_router.router)
app.include_router(usuarios_router.router)
app.include_router(productos_router.router)
app.include_router(categorias_router.router)
app.include_router(ventas_router.router)
app.include_router(templates_router)