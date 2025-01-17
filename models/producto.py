from .venta import Venta
from .categoria import Categoria
from sql_app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, DateTime

class Producto(Base):
    __tablename__ = "productos"

    producto_id = Column(Integer, primary_key=True, index=True)
    nombre_producto = Column(String,nullable=False)
    fecha_de_publicacion = Column(DateTime)
    numero_de_productos_subidos = Column(Integer)
    precio_unitario_de_producto = Column(Integer)
    stock = Column(Integer)
    link_de_imagen = Column(String,nullable=False)
    descripcion = Column(String)

    categorias = relationship(
            "CategoriaProducto",
            #secondary = "categorias_de_productos",
            back_populates = "producto"
    )
    usuarios = relationship(
            "VendedorProducto",
            #secondary = "categorias_de_productos",
            back_populates = "producto"
    )

class CategoriaProducto(Base):
    __tablename__ = "categorias_de_productos"

    #categoria_producto_id = Column(Integer,primary_key=True,index=True)

    
    categoria_id = Column(Integer,
                     ForeignKey("categorias.categoria_id"),
                     primary_key=True)
    categoria = relationship("Categoria",
                     back_populates="productos")

    producto_id = Column(Integer,
                     ForeignKey("productos.producto_id"),
                     primary_key=True)
    producto = relationship("Producto",
                     back_populates="categorias")

class VendedorProducto(Base):
    __tablename__ = "vendedores_de_productos"

    #categoria_producto_id = Column(Integer,primary_key=True,index=True)

    
    usuario_id = Column(Integer,
                    ForeignKey("usuarios.usuario_id"),
                    primary_key=True)
    usuario = relationship("Usuario",
                    back_populates="productos")

    producto_id = Column(Integer,
                    ForeignKey("productos.producto_id"),
                    primary_key=True)
    producto = relationship("Producto",
                    back_populates="usuarios")

