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

@app.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    data = request.get_json()
    venta_enc = data.get('venta_enc')
    venta_det = data.get('venta_det')
    db.venta_enc.insert_one(venta_enc)
    db.venta_det.insert_many(venta_det)
    return 'Venta guardada correctamente.'
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
    <h2>Menú principal v 1</h2>
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

@app.route('/ventas')
def ventas():
        html = '''
        <style>
        body { font-family: Arial, sans-serif; background: #f8f8f8; }
        .venta-container { max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 0 10px #ccc; padding: 30px; }
        .venta-form input, .venta-form select { font-size: 1.2em; margin: 5px; }
        .venta-list { margin-top: 20px; }
        .venta-list th, .venta-list td { font-size: 1.2em; padding: 5px 10px; }
        .venta-total { font-size: 2.5em; color: #007bff; text-align: right; margin-top: 20px; }
        .venta-cambio { font-size: 2em; color: #28a745; text-align: right; margin-top: 10px; }
        </style>
        <div class="venta-container">
            <h2>Captura de Venta</h2>
            <form class="venta-form" id="form-agregar">
                <input type="number" min="1" value="1" id="cantidad" placeholder="Cantidad" required>
                <input type="text" id="codigo_barras" placeholder="Código de Barras" autofocus>
                <input type="text" id="descripcion" placeholder="Descripción">
                <button type="submit">Agregar</button>
            </form>
            <table class="venta-list" id="tabla-productos" style="width:100%">
                <thead><tr><th>Cant</th><th>Código</th><th>Descripción</th><th>Precio</th><th>Importe</th></tr></thead>
                <tbody></tbody>
            </table>
            <div class="venta-total" id="total">$0.00</div>
            <div class="venta-cambio" id="cambio" style="display:none"></div>
            <button id="guardar" style="margin-top:20px;font-size:1.2em;">Guardar venta</button>
            <a href="/">Volver al menú principal</a>
        </div>
        <script>
        let productos = [];
        let total = 0;
        let ticketId = Date.now();
        function actualizarTabla() {
            const tbody = document.querySelector('#tabla-productos tbody');
            tbody.innerHTML = '';
            total = 0;
            productos.forEach((p, i) => {
                const importe = p.precio * p.cantidad;
                total += importe;
                tbody.innerHTML += `<tr><td><input type='number' min='1' value='${p.cantidad}' data-idx='${i}' class='cantidad-input' style='width:50px'></td><td>${p.codigo_barras}</td><td>${p.descripcion}</td><td>$${p.precio.toFixed(2)}</td><td>$${importe.toFixed(2)}</td></tr>`;
            });
            document.getElementById('total').textContent = '$' + total.toFixed(2);
        }
        document.getElementById('form-agregar').onsubmit = async function(e) {
            e.preventDefault();
            let cantidad = parseInt(document.getElementById('cantidad').value);
            let codigo = document.getElementById('codigo_barras').value.trim();
            let desc = document.getElementById('descripcion').value.trim();
            if (!codigo && !desc) return alert('Ingresa código o descripción');
            let producto = null;
            if (codigo) {
                let res = await fetch(`/buscar_producto?codigo_barras=${codigo}`);
                let data = await res.text();
                let match = data.match(/'descripcion': '([^']+)'/);
                let precioMatch = data.match(/'precio': ([0-9.]+)/);
                if (match && precioMatch) {
                    producto = {codigo_barras: codigo, descripcion: match[1], precio: parseFloat(precioMatch[1])};
                } else {
                    return alert('Producto no encontrado');
                }
            } else if (desc) {
                let res = await fetch(`/productos`);
                let html = await res.text();
                let regex = new RegExp(`<li class='producto-item'>.*'descripcion': '${desc}'.*?</li>`, 'i');
                let item = html.match(regex);
                if (item) {
                    let codMatch = item[0].match(/'codigo_barras': '([^']+)'/);
                    let precioMatch = item[0].match(/'precio': ([0-9.]+)/);
                    if (codMatch && precioMatch) {
                        producto = {codigo_barras: codMatch[1], descripcion: desc, precio: parseFloat(precioMatch[1])};
                    }
                }
                if (!producto) return alert('Producto no encontrado por descripción');
            }
            productos.push({cantidad, ...producto});
            actualizarTabla();
            document.getElementById('form-agregar').reset();
            document.getElementById('codigo_barras').focus();
        };
        document.getElementById('tabla-productos').addEventListener('input', function(e) {
            if (e.target.classList.contains('cantidad-input')) {
                let idx = e.target.getAttribute('data-idx');
                productos[idx].cantidad = parseInt(e.target.value);
                actualizarTabla();
            }
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                let efectivo = prompt('Efectivo recibido:');
                if (efectivo !== null) {
                    let cambio = parseFloat(efectivo) - total;
                    document.getElementById('cambio').style.display = '';
                    document.getElementById('cambio').textContent = 'Cambio: $' + cambio.toFixed(2);
                    setTimeout(() => {
                        productos = [];
                        actualizarTabla();
                        document.getElementById('cambio').style.display = 'none';
                    }, 4000);
                }
            }
        });
        document.getElementById('guardar').onclick = async function() {
            if (productos.length === 0) return alert('Agrega productos');
            let venta_enc = {ticket_id: ticketId, fecha: new Date().toISOString(), cliente: 1, total};
            let venta_det = productos.map(p => ({ticket_id: ticketId, id_producto: p.codigo_barras, cantidad: p.cantidad, precio: p.precio}));
            let res = await fetch('/guardar_venta', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({venta_enc, venta_det})
            });
            let msg = await res.text();
            alert(msg);
            productos = [];
            actualizarTabla();
            ticketId = Date.now();
        };
        </script>
        '''
        return html

@app.route('/compras')
def compras():
    return "<h2>Compras</h2><a href='/'>Volver al menú principal</a>"

@app.route('/buscar_producto', methods=['GET', 'POST'])
def buscar_producto():
    html = '''
    <h2>Buscar Producto</h2>
    <form action='/buscar_producto' method='post'>
      <input type='text' name='codigo_barras' placeholder='Código de Barras (ID)' required>
      <button type='submit'>Buscar</button>
    </form>
    '''
    if request.method == 'POST':
        codigo_barras = request.form.get('codigo_barras')
        producto = db.productos.find_one({'codigo_barras': codigo_barras}, {'_id': 0})
        if producto:
            html += f"<h3>Resultado:</h3><pre>{producto}</pre>"
        else:
            html += "<h3>No se encontró el producto.</h3>"
    html += "<a href='/productos'>Volver a Productos</a>"
    return html

@app.route('/cargar_productos', methods=['POST'])
def cargar_productos():
    import pandas as pd
    from werkzeug.utils import secure_filename
    file = request.files.get('archivo')
    if not file:
        return "<h2>Error: No se recibió archivo.</h2><a href='/productos'>Volver a Productos</a>"
    filename = secure_filename(file.filename)
    filepath = f"./{filename}"
    file.save(filepath)
    import traceback
    try:
        df = pd.read_excel(filepath)
        required_cols = ['codigo_barras', 'descripcion', 'unidad', 'precio', 'costo', 'existencia']
        for col in required_cols:
            if col not in df.columns:
                print(f"Error: Falta la columna '{col}' en el archivo.")
                return f"<h2>Error: Falta la columna '{col}' en el archivo.</h2><a href='/productos'>Volver a Productos</a>"
        for i, row in df.iterrows():
            try:
                if db.productos.find_one({'codigo_barras': str(row['codigo_barras'])}):
                    continue  # No duplicar
                db.productos.insert_one({
                    'codigo_barras': str(row['codigo_barras']),
                    'descripcion': str(row['descripcion']),
                    'unidad': str(row['unidad']),
                    'precio': float(row['precio']),
                    'costo': float(row['costo']),
                    'existencia': float(row['existencia'])
                })
            except Exception as e:
                print(f"Error en la fila {i+2}: {e}")
                traceback.print_exc()
                return f"<h2>Error en la fila {i+2}: {e}</h2><a href='/productos'>Volver a Productos</a>"
        print("Catálogo cargado correctamente.")
        return "<h2>Catálogo cargado correctamente.</h2><a href='/productos'>Volver a Productos</a>"
    except Exception as e:
        print(f"Error al procesar archivo: {e}")
        traceback.print_exc()
        return f"<h2>Error al procesar archivo: {e}</h2><a href='/productos'>Volver a Productos</a>"

# Agrega el formulario en la página de productos
@app.route('/productos', methods=['GET'])
def productos():
    html = '''
    <h2>Gestión de Productos</h2>
    <form action='/agregar_producto' method='post'>
      <input type='text' name='codigo_barras' placeholder='Código de Barras (ID)' required>
      <input type='text' name='descripcion' placeholder='Descripción' required>
      <input type='text' name='unidad' placeholder='Unidad' required>
      <input type='number' step='0.01' name='precio' placeholder='Precio' required>
      <input type='number' step='0.01' name='costo' placeholder='Costo' required>
      <input type='number' step='0.01' name='existencia' placeholder='Existencia' required>
      <button type='submit'>Agregar producto</button>
    </form>
    <form action='/modificar_producto' method='post' style='margin-top:10px;'>
      <input type='text' name='codigo_barras' placeholder='Código de Barras (ID) a modificar' required>
      <input type='text' name='descripcion' placeholder='Nueva Descripción'>
      <input type='text' name='unidad' placeholder='Nueva Unidad'>
      <input type='number' step='0.01' name='precio' placeholder='Nuevo Precio'>
      <input type='number' step='0.01' name='costo' placeholder='Nuevo Costo'>
      <input type='number' step='0.01' name='existencia' placeholder='Nueva Existencia'>
      <button type='submit'>Modificar producto</button>
    </form>
    <form action='/eliminar_producto' method='post' style='margin-top:10px;'>
      <input type='text' name='codigo_barras' placeholder='Código de Barras (ID) a eliminar' required>
      <button type='submit'>Eliminar producto</button>
    </form>
    <form action='/buscar_producto' method='get' style='margin-top:10px;'>
      <button type='submit'>Buscar producto</button>
    </form>
    <form action='/cargar_productos' method='post' enctype='multipart/form-data' style='margin-top:10px;'>
      <input type='file' name='archivo' accept='.xlsx' required>
      <button type='submit'>Cargar catálogo desde Excel</button>
    </form>
    <hr>
    <h3>Filtrar productos:</h3>
    <input type='text' id='filtro' placeholder='Escribe para filtrar...'>
    <ul id='lista-productos'>
    '''
    productos = list(db.productos.find({}, {'_id': 0}))
    for p in productos:
        html += f"<li class='producto-item'>{p}</li>"
    html += """</ul><a href='/'>Volver al menú principal</a>
    <script>
    const filtro = document.getElementById('filtro');
    const items = document.querySelectorAll('.producto-item');
    filtro.addEventListener('input', function() {
      const texto = filtro.value.toLowerCase();
      items.forEach(function(item) {
        if (item.textContent.toLowerCase().includes(texto)) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
    </script>
    """
    return html

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    codigo_barras = request.form.get('codigo_barras')
    descripcion = request.form.get('descripcion')
    unidad = request.form.get('unidad')
    precio = float(request.form.get('precio'))
    costo = float(request.form.get('costo'))
    existencia = float(request.form.get('existencia'))
    # Verificar que el código de barras no exista
    if db.productos.find_one({'codigo_barras': codigo_barras}):
        html = """
        <h2>Error: El código de barras ya existe en el catálogo.</h2>
        <a href='/productos'>Volver a Productos</a>
        """
        return html
    db.productos.insert_one({
        'codigo_barras': codigo_barras,
        'descripcion': descripcion,
        'unidad': unidad,
        'precio': precio,
        'costo': costo,
        'existencia': existencia
    })
    return redirect('/productos')

@app.route('/modificar_producto', methods=['POST'])
def modificar_producto():
    codigo_barras = request.form.get('codigo_barras')
    descripcion = request.form.get('descripcion')
    unidad = request.form.get('unidad')
    precio = request.form.get('precio')
    costo = request.form.get('costo')
    existencia = request.form.get('existencia')
    update = {}
    if descripcion:
        update['descripcion'] = descripcion
    if unidad:
        update['unidad'] = unidad
    if precio:
        update['precio'] = float(precio)
    if costo:
        update['costo'] = float(costo)
    if existencia:
        update['existencia'] = float(existencia)
    if update:
        db.productos.update_one({'codigo_barras': codigo_barras}, {'$set': update})
    return redirect('/productos')

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    codigo_barras = request.form.get('codigo_barras')
    db.productos.delete_one({'codigo_barras': codigo_barras})
    return redirect('/productos')

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