import paramiko

def apagar_remoto(host, username, key_filename):
    try:
        # Establecer conexión SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, username=username, key_filename=key_filename)

        # Ejecutar comando de apagado
        stdin, stdout, stderr = ssh_client.exec_command('sudo shutdown -h now')

        # Capturar salida
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            return f'Error al apagar: {error}'
        else:
            return 'La computadora se está apagando correctamente.'
    except Exception as e:
        return f'Error de conexión SSH: {str(e)}'
    finally:
        ssh_client.close()

# Ejemplo de uso
host = '192.168.43.225'  # Cambia esto por la dirección IP de la computadora remota
username = 'mariachi'
key_filename = '/home/adolf/.ssh/id_rsa'  # Ruta a tu clave privada

resultado = apagar_remoto(host, username, key_filename)
print(resultado)