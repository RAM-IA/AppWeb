from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
# Habilitar CORS
CORS(app)

# Conexión a MongoDB Atlas
import os
mongo_uri = os.environ.get('MONGO_URI', "mongodb+srv://ramongo:LeoyDem01@cluster0.aemc3mn.mongodb.net/sample_mflix?retryWrites=true&w=majority&appName=Cluster0&connectTimeoutMS=10000&socketTimeoutMS=10000")
client = MongoClient(mongo_uri)
db = client.get_database('sample_mflix')  # Cambia 'test' por el nombre de tu base de datos si es diferente
usuarios_collection = db.users
@app.route('/')
def home():
    return "API Flask funcionando de nuevo2: User" + " " + str(usuarios_collection.count_documents({}))
@app.route('/users', methods=['GET'])
def get_users():
    users = list(usuarios_collection.find({}, {'_id': 0}))
    return jsonify(users)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
    
