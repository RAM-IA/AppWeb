from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# Habilitar CORS
CORS(app)

# Conexión a MongoDB Atlas
import os
mongo_uri = os.environ.get('MONGO_URI', "mongodb+srv://ramsj:LeoyDem01@cluster0.1fgzarl.mongodb.net/dbapp?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(mongo_uri)
db = client.get_database('dbapp')  # Cambia 'sample_mflix' por el nombre de tu base de datos
@app.route('/')
def home():
    # Obtener todas las colecciones
    colecciones = db.list_collection_names()
    # Generar HTML con links
    html = "<h2>Colecciones en la base de datos2:</h2><ul>"
    for col in colecciones:
        html += f'<li><a href="/coleccion/{col}" target="_blank">{col}</a></li>'
    html += "</ul>"
    return html
@app.route('/coleccion/<nombre>')
def mostrar_coleccion(nombre):
    coleccion = db[nombre]
    documentos = list(coleccion.find({}, {'_id': 0}))
    html = f"<h2>Colección: {nombre}</h2><pre>{documentos}</pre>"
    return html

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
