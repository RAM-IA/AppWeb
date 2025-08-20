from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# Habilitar CORS
CORS(app)

# Conexión a MongoDB Atlas
import os
mongo_uri = os.environ.get('MONGO_URI', "mongodb+srv://ramsj:LeoyDem01@cluster0.1fgzarl.mongodb.net/")
client = MongoClient(mongo_uri)
db = client.get_database('dbapp')  
usuarios = db['usuarios']
print(list(usuarios.find()))
print(client.list_database_names())
print(db.list_collection_names())

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

@app.route('/agregar', methods=['POST'])
def agregar_usuario():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    db.usuarios.insert_one({'id': id, 'nombre': nombre, 'direccion': direccion})
    return redirect('/')

@app.route('/modificar', methods=['POST'])
def modificar_usuario():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    update = {}
    if nombre:
        update['nombre'] = nombre
    if direccion:
        update['direccion'] = direccion
    if update:
        db.usuarios.update_one({'id': id}, {'$set': update})
    return redirect('/')

@app.route('/eliminar', methods=['POST'])
def eliminar_usuario():
    id = request.form.get('id')
    db.usuarios.delete_one({'id': id})
    return redirect('/')