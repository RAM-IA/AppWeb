from flask import Flask, request, redirect, jsonify, send_from_directory
from routes.usuarios import usuarios_bp
from flask_cors import CORS
import os


app = Flask(__name__)
# Habilitar CORS
CORS(app)

# Registrar blueprint de usuarios
app.register_blueprint(usuarios_bp)

# Servir Flutter Web desde build/web
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def flutter_app(path):
	web_dir = os.path.join(os.path.dirname(__file__), 'flutter_app', 'build', 'web')
	if path != "" and os.path.exists(os.path.join(web_dir, path)):
		return send_from_directory(web_dir, path)
	else:
		return send_from_directory(web_dir, 'index.html')
		
if __name__ == '__main__':
	app.run(debug=True)