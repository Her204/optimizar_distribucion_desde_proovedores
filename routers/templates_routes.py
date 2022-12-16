from PIL import Image
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from fastapi_csrf_protect import CsrfProtect
from fastapi.templating import Jinja2Templates
from schemas import productos as productos_schemas
from fastapi import Request, APIRouter, File,UploadFile,Depends

router = APIRouter(prefix="", tags=["home"])

templates = Jinja2Templates(directory="templates")

# Pagina principal del sitio web
@router.get('/')
async def index(request: Request):
  context = {
    "request": request,
  }
  return templates.TemplateResponse("index.html", context)

# Genera las paginas que muestran los productos por categoria
@router.get('/explorando_por_categoria/{categoria_id}')
async def index(categoria_id:int,request: Request):
  context = {
    "request": request,
  }
  return templates.TemplateResponse("index.html", context)

# Genera la pagina que muestra los productos buscados por palabras
@router.get('/productos_buscados')
async def index(palabra_clave:str,request: Request):
  context = {
    "request": request,
  }
  return templates.TemplateResponse("index.html", context)

# Genera la planilla de crear producto
@router.get('/crear_producto')
async def index(request:Request,csrf_protect:CsrfProtect = Depends()):
    csrf_protect.validate_csrf_in_cookies(request)
    entradas = eval(productos_schemas.ProductoCreate.schema_json())["properties"].keys()

    tipos = ["text","number","number","file",
             "number","text","text","text"]

    context = {
      "request":request,
       "entradas": [a for a in zip(entradas,tipos)]
    }
    return templates.TemplateResponse("crear_productos_planilla.html", context)

@router.post("/guardar_imagen_productos")
async def UploadImage(file: UploadFile = File(...)):
    
    if not ".jpg" in file.filename.lower(): 
        raise ValueError("Error file its not an image")
    


    path = f'static/images/productos/{file.filename.split(".")[0]}.jpg'
    
    print(file.filename)

    with open(path,'wb') as image:
        image.write(await file.read())
        image.close()
    
    return path