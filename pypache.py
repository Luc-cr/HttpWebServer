import socket
import datetime

class createHttp:
    def __init__(self, host, port):
        self.events = {} # Eventos para los decoradores
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Iniciamos comunicacion TCP ip
        server.bind((host, port)) # bindeamos puento
        server.listen(1) # Escuchando
        print("[Console] Server initialized")
        self.server = server

    def start(self):
        print("[Console] Server started")
        while True:
            send = "HTTP/1.1 404 NOT FOUND\n\n<h1>Pagina no encontrada</h1>" # En caso de no encotrar la pagina
            client_con, client_addr = self.server.accept() # Info del cliente
            request = client_con.recv(65535).decode()

            # Para separar cada key de su value 
            header = request.replace("\r\n", ": ").split(": ")

            # Obtengo el basico del HTTP(Metodo, dir y version)
            head = header[0].split(" ")
            del header[0]
            
            #Lo coloco en un dic para ser llamado
            data = {
                "client-addr": client_addr,
                "method": head[0],
                "page": head[1],
                "http-version": head[2]
            }
            
            # Agregamos al diccionario los parametros del header
            i = 0
            while i < len(header) -1 :
                if header[i] == '': # Termino el header y empieza el body
                    break
                else:
                    data[header[i]] = header[i + 1]
                    i += 2

            body = ""
            while i < len(header):
                body += header[i]
                i += 1
            data['body'] = body
            # Busco si existe una funcion handler de la pagina
            for key in self.events.keys():
                if key == data["page"] and data["method"] in self.events[key][0]:
                    send = self.events[key][1](data) # Si existe y tiene el mismo metodo la ejecuto

            # Envio la data y cierro la conexion
            client_con.sendall(send.encode())
            client_con.close()

    #Decorador para crear funciones que devuelvan una pagina 
    def AddPage(self, page, method):
        def inner(*args, **kwargs):
            self.events[page] = [method,args[0]]
        return inner


# Clase para ayudar a manejar el header de la respuesta
class Response:
    ok = "HTTP/1.1 200 OK"
    notfound = "HTTP/1.1 404 NOT FOUND"
    nocontent = "HTTP/1.1 204 NO CONTENT"
    badrequest = "HTTP/1.1 400 BAD REQUEST"
    forbidden = "HTTP/1.1 403 FORBIDDEN"
    internalerror = "HTTP/1.1 500 INTERNAL SERVER ERROR"

    def header(self, response :str, contentype :str, body :str) -> str:
        header = response + "\n"\
                 "Date: {}".format(str(datetime.datetime.now())) + "\n" \
                 "Server: PyPache \n" \
                 "Content-Length: "+ str(len(body)) +"\n" \
                 "Content-type: " + str(contentype) + "\n" \
                 "\n" + body
        return header
    
    def json(self, response :str, body :str) -> str:
        header = response + "\n"\
                 "Date: {}".format(str(datetime.datetime.now())) + "\n"\
                 "Server: PyPache \n" \
                 "Content-Length: " + str(len(body)) + "\n"\
                 "Content-type: application/json" + "\n"\
                 "\n" + body
        return header

    def text(self, response :str, body :str) -> str:
        header = response + "\n"\
                 "Date: {}".format(str(datetime.datetime.now())) + "\n"\
                 "Server: PyPache \n" \
                 "Content-Length: " + str(len(body)) + "\n"\
                 "Content-type: plain/text" + "\n"\
                 "\n" + body
        return header