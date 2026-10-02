from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from datetime import date, datetime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Productos(Base):
    __tablename__ = 'Productos'

    codigo = Column(Integer, primary_key=True)
    producto = Column(String)
    precio = Column(Integer)

    def __str__(self):
        return f"{self.producto}"
    
class Compra(Base):
    __tablename__ = 'Compra'
    
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    valor_total = Column(Integer)

    def __str__(self):
        return f"{self.valor_total}"
    
# Crea el motor de la base de datos SQLite  
engine = create_engine('sqlite:///Supermercado.db', echo=True)

# Crea todas las tablas definidas en el modelo
Base.metadata.create_all(engine)