import socket
import subprocess

HOST = '127.0.0.1'
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (HOST, PORT)
sock.bind(server_address)
sock.listen(1)

while True:
    print('Esperando conexiones...')
    conection, client_address = sock.accept()
    try:
        print('Cliente conectado', client_address)
        while True:
            data = conection.recv(1024)
            print('Recibido {!r}'.format(data))
            if(data):
                if(data.decode('utf-8') == 'quit\n'):
                    break
                result = subprocess.run(data.decode('utf-8').replace('\n', '').split('  '), stdout=subprocess.PIPE)
                conection.sendall(result.stdout)
            else:
                break
    finally:
        conection.close()




