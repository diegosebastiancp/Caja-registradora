from flask import Flask, render_template, request, jsonify, redirect, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from modelo import *

app = Flask(__name__)

engine = create_engine('sqlite:///Supermercado.db', connect_args={'check_same_thread':False})
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("carro.html")

@app.route("/lista")
def lista():
    
    lista = session.query(Productos).all()
    return render_template("lista.html", productos=lista)

@app.route("/add", methods=['POST'])
def add():

    if request.method == "POST":
        
        codigo = request.json.get("codigo", "")

        if codigo:
            try:
                existe = session.query(Productos).filter(Productos.codigo == codigo).first()

                if not existe:
                    return {'check': False,
                            'msg': 'No existe el producto'}
                else:
                    return {'check': True,
                            'msg': 'Producto agregado!',
                            'codigo': existe.codigo,
                            'producto': existe.producto,
                            'valor': existe.precio,
                            'cantidad': 1}
            
            except Exception as e:
                session.rollback()
                return {'check': False,
                        'msg': str(e)}, 500

@app.route("/addnew", methods=['POST'])
def nuevoProducto():

    codigo = request.form.get("codigo")
    descripcion = request.form.get("desc")
    precio = request.form.get("precio")

    if codigo and descripcion and precio:

        existe = session.query(Productos).filter(Productos.codigo == codigo).first()

        if existe:
            return {'check': False,
                    'msg': 'El producto ya existe'}

        try:
            nuevo_producto = Productos(codigo=codigo,
                                    producto=descripcion,
                                    precio=precio)
            session.add(nuevo_producto)

            session.commit()
            print(f"Nuevo producto añadido: {nuevo_producto}")

            return {'check': True,
                        'msg': 'Nuevo producto agregado!',
                        'codigo': nuevo_producto.codigo,
                        'producto': nuevo_producto.producto,
                        'valor': nuevo_producto.precio}

        except Exception as e:
            session.rollback() # Rollback in case of error
            print(f"Ocurrió un error: {e}")

@app.route("/producto/editar/<codigo>", methods=["POST"])
def editar_producto(codigo):

    producto = session.query(Productos).filter(
        Productos.codigo == codigo
    ).first()

    if not producto:
        return {
            "check": False,
            "msg": "Producto no encontrado"
        }

    try:
        datos = request.json

        producto.producto = datos.get("producto")
        producto.precio = datos.get("precio")

        session.commit()

        return {
            "check": True,
            "msg": "Producto actualizado"
        }

    except Exception as e:
        session.rollback()

        return {
            "check": False,
            "msg": str(e)
        }, 500

@app.route("/producto/eliminar/<codigo>")
def eliminar_producto(codigo):

    producto = session.query(Productos).filter(
        Productos.codigo == codigo
    ).first()

    if not producto:
        return "Producto no encontrado", 404

    try:
        session.delete(producto)
        session.commit()

    except Exception as e:
        session.rollback()
        return str(e), 500

    return redirect(url_for("lista"))

print(app.url_map)
if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False, threaded=False)