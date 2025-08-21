from flask import Blueprint, request, jsonify
from db import db

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas')
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
            let tr = e.target.closest('tr.resultado-item');
            if (!tr) return;
            let idx = Array.from(resultadosDiv.querySelectorAll('tr.resultado-item')).indexOf(tr);
            <h2>Captura de Venta</h2>
            <form class="venta-form" id="form-agregar" autocomplete="off">
                <input type="number" min="1" value="1" id="cantidad" placeholder="Cantidad" style="display:none">
                <input type="text" id="codigo_barras" placeholder="Código de Barras" autofocus>
                <input type="text" id="descripcion" placeholder="Descripción">
            </form>
            <div id="resultados" style="background:#fff;border:1px solid #ccc;max-height:200px;overflow-y:auto;display:none;position:absolute;z-index:10;width:90%"></div>
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
        const codigoInput = document.getElementById('codigo_barras');
        const descInput = document.getElementById('descripcion');
        const resultadosDiv = document.getElementById('resultados');
        let resultados = [];
        let seleccionIdx = 0;

        codigoInput.addEventListener('keydown', async function(e) {
            if (e.key === 'Enter' && codigoInput.value.trim()) {
                e.preventDefault();
                let codigo = codigoInput.value.trim();
                let res = await fetch(`/buscar_producto?codigo_barras=${codigo}`);
                if (res.ok) {
                    let producto = await res.json();
                    let idx = productos.findIndex(p => p.codigo_barras === producto.codigo_barras);
                    if (idx >= 0) {
                        productos[idx].cantidad += 1;
                    } else {
                        productos.push({cantidad: 1, ...producto});
                    }
                    actualizarTabla();
                    codigoInput.value = '';
                } else {
                    alert('Producto no encontrado');
                }
            }
        });

        descInput.addEventListener('keydown', async function(e) {
            if (e.key === 'Enter' && descInput.value.trim()) {
                e.preventDefault();
                let desc = descInput.value.trim();
                let res = await fetch(`/buscar_producto?descripcion=${encodeURIComponent(desc)}`);
                if (res.ok) {
                    resultados = await res.json();
                    if (resultados.length === 0) {
                        resultadosDiv.style.display = 'none';
                        alert('No hay coincidencias');
                        return;
                    }
                    mostrarResultados();
                }
            } else if (e.key === 'ArrowDown') {
                if (resultados.length > 0) {
                    seleccionIdx = Math.min(seleccionIdx + 1, resultados.length - 1);
                    resaltarSeleccion();
                }
            } else if (e.key === 'ArrowUp') {
                if (resultados.length > 0) {
                    seleccionIdx = Math.max(seleccionIdx - 1, 0);
                    resaltarSeleccion();
                }
            } else if (e.key === 'Escape') {
                resultadosDiv.style.display = 'none';
                descInput.focus();
            } else if (e.key === 'Enter' && resultados.length > 0) {
                e.preventDefault();
                agregarSeleccionado();
            }
        });

        function mostrarResultados() {
            resultadosDiv.innerHTML = resultados.map((p, i) => `<div class='resultado-item' style='padding:8px;cursor:pointer;background:${i===seleccionIdx?'#e0e0ff':'#fff'}'>${p.descripcion} ($${p.precio})</div>`).join('');
            resultadosDiv.style.display = '';
            resaltarSeleccion();
        }
        function resaltarSeleccion() {
            let items = resultadosDiv.querySelectorAll('.resultado-item');
            items.forEach((el, i) => {
                el.style.background = i === seleccionIdx ? '#e0e0ff' : '#fff';
            });
        }
        resultadosDiv.addEventListener('click', function(e) {
            let idx = Array.from(resultadosDiv.children).indexOf(e.target);
            seleccionIdx = idx;
            agregarSeleccionado();
        });
        function agregarSeleccionado() {
            let producto = resultados[seleccionIdx];
            if (!producto) return;
            let idx = productos.findIndex(p => p.codigo_barras === producto.codigo_barras);
            if (idx >= 0) {
                productos[idx].cantidad += 1;
            } else {
                productos.push({cantidad: 1, ...producto});
            }
            actualizarTabla();
            resultadosDiv.style.display = 'none';
            descInput.value = '';
            resultados = [];
            seleccionIdx = 0;
        }
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

@ventas_bp.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    data = request.get_json()
    venta_enc = data.get('venta_enc')
    venta_det = data.get('venta_det')
    db.venta_enc.insert_one(venta_enc)
    db.venta_det.insert_many(venta_det)
    return 'Venta guardada correctamente.'

