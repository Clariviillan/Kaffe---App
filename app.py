
from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)

@app.route("/estado")
def estado():
    return jsonify({
        "mensaje": "La aplicación funciona correctamente"
    })

@app.route("/comentario", methods=["POST"])
def comentario():
    texto = request.form.get("texto", "").strip()

    # Validación de entrada
    if not texto or len(texto) > 500:
        abort(400)

    # Jinja escapa automáticamente el contenido
    return render_template(
        "index.html",
        title="Hello",
        comentario=texto
    )

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/buscar")
def buscar():
    nombre = request.args.get("nombre", "").strip()

    if not nombre or len(nombre) > 100:
        abort(400)

    # Consulta segura utilizando SQLAlchemy
    resultados = Usuario.query.filter_by(nombre=nombre).all()

    return jsonify({
        "resultados": [usuario.nombre for usuario in resultados]
    })

# Lista de productos con diccionarios
productos = [
    {
        "id": 1,
        "nombre": "Laptop",
        "precio": 15000,
        "categoria": "Tecnología"
    },
    {
        "id": 2,
        "nombre": "Audífonos",
        "precio": 850,
        "categoria": "Accesorios"
    },
    {
        "id": 3,
        "nombre": "Teclado",
        "precio": 1200,
        "categoria": "Tecnología"
    }
]

# Primera ruta: página principal
@app.route("/")
def inicio():
    return render_template("index.html", title="Mi tienda")

# Segunda ruta: mostrar productos
@app.route("/productos")
def mostrar_productos():
    return render_template(
        "productos.html",
        productos=productos
    )

if __name__ == "__main__":
    app.run(debug=True)
