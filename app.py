from flask import Flask, request, redirect
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

@app.route('/')
def menu():
    html = '''
    <h2>Menú principal</h2>
    <form action="/ventas" method="get"><button type="submit">Ventas</button></form>
    <form action="/compras" method="get"><button type="submit">Compras</button></form>
    <form action="/productos" method="get"><button type="submit">Productos</button></form>
    <form action="/clientes" method="get"><button type="submit">Clientes</button></form>
    <form action="/proveedores" method="get"><button type="submit">Proveedores</button></form>
    <form action="/gastos" method="get"><button type="submit">Gastos</button></form>
    <form action="/cortes" method="get"><button type="submit">Cortes</button></form>
    <form action="/usuarios" method="get"><button type="submit">Usuarios</button></form>
    '''
    return html

@app.route('/usuarios', methods=['GET'])
def usuarios():
    html = '''
    <h2>Gestión de Usuarios</h2>
    <form action='/agregar_usuario' method='post'>
      <input type='text' name='id' placeholder='Id' required>
      <input type='text' name='nombre' placeholder='Nombre' required>
      <input type='text' name='direccion' placeholder='Dirección' required>
      <button type='submit'>Agregar usuario</button>
    </form>
    <form action='/modificar_usuario' method='post' style='margin-top:10px;'>
      <input type='text' name='id' placeholder='Id a modificar' required>
      <input type='text' name='nombre' placeholder='Nuevo nombre'>
      <input type='text' name='direccion' placeholder='Nueva dirección'>
      <button type='submit'>Modificar usuario</button>
    </form>
    <form action='/eliminar_usuario' method='post' style='margin-top:10px;'>
      <input type='text' name='id' placeholder='Id a eliminar' required>
      <button type='submit'>Eliminar usuario</button>
    </form>
    <hr>
    <h3>Usuarios actuales:</h3>
    <ul>
    '''
    usuarios = list(db.usuarios.find({}, {'_id': 0}))
    for u in usuarios:
        html += f"<li>{u}</li>"
    html += "</ul><a href='/'>Volver al menú principal</a>"
    return html

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    db.usuarios.insert_one({'id': id, 'nombre': nombre, 'direccion': direccion})
    return redirect('/usuarios')

@app.route('/modificar_usuario', methods=['POST'])
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
    return redirect('/usuarios')

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    id = request.form.get('id')
    db.usuarios.delete_one({'id': id})
    return redirect('/usuarios')

# Las demás opciones del menú solo muestran un mensaje por ahora
@app.route('/ventas')
def ventas():
    return "<h2>Ventas</h2><a href='/'>Volver al menú principal</a>"

@app.route('/compras')
def compras():
    return "<h2>Compras</h2><a href='/'>Volver al menú principal</a>"

@app.route('/productos')
def productos():
    return "<h2>Productos</h2><a href='/'>Volver al menú principal</a>"

@app.route('/clientes')
def clientes():
    return "<h2>Clientes</h2><a href='/'>Volver al menú principal</a>"

@app.route('/proveedores')
def proveedores():
    return "<h2>Proveedores</h2><a href='/'>Volver al menú principal</a>"

@app.route('/gastos')
def gastos():
    return "<h2>Gastos</h2><a href='/'>Volver al menú principal</a>"

@app.route('/cortes')
def cortes():
    return "<h2>Cortes</h2><a href='/'>Volver al menú principal</a>"