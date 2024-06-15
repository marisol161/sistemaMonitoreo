from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

def permitir_ping(ip_destino):
    comando = f"/sbin/iptables -D INPUT -p icmp --icmp-type echo-request -s {ip_destino} -j DROP"
    ejecutar_comando(comando)

def denegar_ping(ip_destino):
    comando = f"/sbin/iptables -A INPUT -p icmp --icmp-type echo-request -s {ip_destino} -j DROP"
    ejecutar_comando(comando)

def ejecutar_comando(comando):
    # Leer la contraseña desde el archivo
    with open('sudo_password.txt', 'r') as file:
        sudo_password = file.read().strip()
    
    # Construir el comando para pasar la contraseña a sudo
    comando_con_sudo = f"echo {sudo_password} | sudo -S {comando}"

    subprocess.run(comando_con_sudo, shell=True)

@app.route('/')
def index():
    return render_template('resultado.html')

@app.route('/control_ping', methods=['POST'])
def control_ping():
    ip_destino = request.form['ip_destino']
    accion = request.form['accion']
    
    if accion == "permitir":
        permitir_ping(ip_destino)
        mensaje = "Se ha permitido el ping remoto desde la dirección especificada."
    elif accion == "denegar":
        denegar_ping(ip_destino)
        mensaje = "Se ha denegado el ping remoto desde la dirección especificada."
    else:
        mensaje = "Entrada no válida. Por favor, ingresa 'permitir' o 'denegar'."
    
    return render_template('resultado.html', mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
