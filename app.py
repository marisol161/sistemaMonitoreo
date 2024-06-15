from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Lista de APIs con su respectiva información
apis = [
    {"title": "1.- Observar lo que hace la otra PC", "description": "Observar PC", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "2.- Transferencia de información", "description": "Transferencia de información de modo bidireccional", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "3.- Exhibir un PC", "description": "Observar lo que hace las pc's de modo remoto", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "4.- Mostrar lo que hace la máquina principal", "description": "El equipo principal visualizara lo que hace la maquina conectada", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "5.- Bloquear teclado y mouse", "description": "Bloquear y desbloquear la entra del teclado y el mouse", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "6.- Apagar PC remoto", "description": "Apagar el pc de manera remota", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "7.- Control de Ping Remoto", "description": "Permitir o denegar ping remoto a una IP específica.", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "8.- Chat", "description": "Chat bidireccional de modo remoto entre dos equipos", "endpoint": "http://127.0.0.1:5000/"},
    {"title": "9.- Denegar acceso a páginas web", "description": "Permitir y denegar acceso a páginas web a una IP especifica", "endpoint": "http://127.0.0.1:5000/"},
    # Añadir más APIs aquí
]

@app.route('/')
def index():
    return render_template('index.html', apis=apis)

@app.route('/api/cards', methods=['GET'])
def get_cards():
    return jsonify({"cards": apis})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
