from sqlalchemy import Boolean, Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sql_app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre_de_usuario = Column(String,unique=True)
    fecha_de_creacion = Column(DateTime)
    correo_de_usuario = Column(String, unique=True)
    contrasenia_encriptada = Column(String)
    pais = Column(String)
    esta_activo = Column(Boolean(), default=True)
    es_super_usuario = Column(Boolean(),default=False)
    ciudad = Column(String)
    productos = relationship(
        "VendedorProducto",
        #secondary="categorias_de_productos",
        back_populates="usuario"
        )
