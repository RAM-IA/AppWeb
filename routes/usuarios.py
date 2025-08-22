
from flask import Blueprint, request, redirect, jsonify
from db import db

usuarios_bp = Blueprint('usuarios', __name__)

# Endpoint para login
@usuarios_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    nombre = data.get('nombre')
    contrasena = data.get('contrasena')
    usuario = db.usuarios.find_one({'nombre': nombre, 'contrasena': contrasena}, {'_id': 0})
    if usuario:
        return jsonify({'success': True, 'usuario': usuario}), 200
    else:
        return jsonify({'success': False, 'msg': 'Usuario o contraseña incorrectos'}), 401

# API REST para gestión de usuarios
@usuarios_bp.route('/api/usuarios', methods=['GET'])
def api_get_usuarios():
    usuarios = list(db.usuarios.find({}, {'_id': 0}))
    return jsonify(usuarios)

@usuarios_bp.route('/api/usuarios', methods=['POST'])
def api_add_usuario():
    data = request.get_json()
    id = data.get('id')
    nombre = data.get('nombre')
    contrasena = data.get('contrasena')
    rol = data.get('rol', 'usuario')
    db.usuarios.insert_one({'id': id, 'nombre': nombre, 'contrasena': contrasena, 'rol': rol})
    return jsonify({'msg': 'Usuario agregado'}), 200

@usuarios_bp.route('/usuarios', methods=['GET'])
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

@usuarios_bp.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    direccion = request.form.get('direccion')
    db.usuarios.insert_one({'id': id, 'nombre': nombre, 'direccion': direccion})
    return redirect('/usuarios')

@usuarios_bp.route('/modificar_usuario', methods=['POST'])
def modificar_usuario():
    id = request.form.get('id')
    nombre = request.form.get('nombre')
    contrasena = request.form.get('contrasena')
    rol = request.form.get('rol')
    update = {}
    if nombre:
        update['nombre'] = nombre
    if contrasena:
        update['contrasena'] = contrasena
    if rol:
        update['rol'] = rol
    if update:
        db.usuarios.update_one({'id': id}, {'$set': update})
    return redirect('/usuarios')

@usuarios_bp.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    id = request.form.get('id')
    db.usuarios.delete_one({'id': id})
    return redirect('/usuarios')


