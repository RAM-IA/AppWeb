from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# Habilitar CORS
CORS(app)

# Conexión a MongoDB Atlas
import os
mongo_uri = os.environ.get('MONGO_URI', "mongodb+srv://ramsj:LeoyDem01@cluster0.1fgzarl.mongodb.net/")
client = MongoClient(mongo_uri)
db = client.get_database('dbapp')  # Cambia 'sample_mflix' por el nombre de tu base de datos
@app.route('/')
def home():
    # Obtener todas las colecciones
    colecciones = db.list_collection_names()
    html = """
<h2>Menú de opciones para la colección 'usuarios'</h2>
<form action='/agregar' method='post'>
  <input type='text' name='id' placeholder='Id' required>
  <input type='text' name='nombre' placeholder='Nombre' required>
  <input type='text' name='direccion' placeholder='Dirección' required>
  <button type='submit'>Agregar usuario</button>
</form>
<form action='/modificar' method='post' style='margin-top:10px;'>
  <input type='text' name='id' placeholder='Id a modificar' required>
  <input type='text' name='nombre' placeholder='Nuevo nombre'>
  <input type='text' name='direccion' placeholder='Nueva dirección'>
  <button type='submit'>Modificar usuario</button>
</form>
<form action='/eliminar' method='post' style='margin-top:10px;'>
  <input type='text' name='id' placeholder='Id a eliminar' required>
  <button type='submit'>Eliminar usuario</button>
</form>
<hr>
<h3>Usuarios actuales:</h3>
<ul>
"""
    usuarios = list(db.usuarios.find({}, {'_id': 0}))
    for u in usuarios:
        html += f"<li>{u}</li>"
    html += "</ul>"
    return html