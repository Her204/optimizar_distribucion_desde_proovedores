import os
from typing import List
from urllib import request
from dependencies import get_db
from sqlalchemy.orm import Session
#from fastapi_login import LoginManager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from routers.ventas import main as ventas_router
from schemas import productos as productos_schemas
from routers.usuarios import main as usuarios_router
from sql_app.database import SessionLocal,Base, engine
from routers.productos import main as productos_router
from routers.categorias import main as categorias_router
from routers.templates_routes import router as templates_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

#SECRET = os.environ.get("TOKEN_ALTOQ")

#manager = LoginManager(SECRET,"/login")

app.mount("/static", StaticFiles(directory="static/"), name="static")

app.include_router(productos_router.router)
app.include_router(categorias_router.router)
app.include_router(usuarios_router.router)
app.include_router(ventas_router.router)
app.include_router(templates_router)
