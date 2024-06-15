from flask import Flask, render_template, request, abort

app = Flask(__name__)

# Diccionario para almacenar las URLs con sus respectivas listas de IPs permitidas y denegadas
url_access_control = {
    "/protected": {
        "allowed_ips": [],
        "denied_ips": []
    }
}

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    requested_path = request.path

    # Verificar si la URL solicitada está en el control de acceso
    if requested_path in url_access_control:
        access_rules = url_access_control[requested_path]
        allowed_ips = access_rules["allowed_ips"]
        denied_ips = access_rules["denied_ips"]

        # Denegar acceso si la IP está en la lista de denegadas o no está en la lista de permitidas (si la lista no está vacía)
        if client_ip in denied_ips or (allowed_ips and client_ip not in allowed_ips):
            abort(403)  # Acceso denegado

@app.route('/')
def index():
    return render_template('denegar_acceso.html')

@app.route('/protected')
def protected():
    return "Esta es una página protegida."

@app.route('/control_acceso', methods=['POST'])
def control_acceso():
    url_destino = request.form['url_destino']
    ip_destino = request.form['ip_destino']
    accion = request.form['accion']
    
    if url_destino not in url_access_control:
        url_access_control[url_destino] = {"allowed_ips": [], "denied_ips": []}
    
    access_rules = url_access_control[url_destino]

    if accion == "permitir":
        if ip_destino not in access_rules["allowed_ips"]:
            access_rules["allowed_ips"].append(ip_destino)
        if ip_destino in access_rules["denied_ips"]:
            access_rules["denied_ips"].remove(ip_destino)
        mensaje = f"Se ha permitido el acceso a la dirección IP: {ip_destino} para la URL: {url_destino}."
    elif accion == "denegar":
        if ip_destino not in access_rules["denied_ips"]:
            access_rules["denied_ips"].append(ip_destino)
        if ip_destino in access_rules["allowed_ips"]:
            access_rules["allowed_ips"].remove(ip_destino)
        mensaje = f"Se ha denegado el acceso a la dirección IP: {ip_destino} para la URL: {url_destino}."
    else:
        mensaje = "Entrada no válida. Por favor, ingresa 'permitir' o 'denegar'."
    
    return render_template('denegar_acceso.html', mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
