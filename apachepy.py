import socket
import json

class createHttp:
    def __init__(self, host, port):
        self.events = {}
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print("[Console] Server initialized")
        self.server = server

    def start(self):
        print("[Console] Server started")
        while True:
            send = Response.notfound
            #.replace("\r\n", " ").split(" ")
            client_con, client_addr = self.server.accept()
            request = client_con.recv(1024).decode()
            header = request.replace("\r\n", " ").split(" ")

            if header[0] == "GET":
                data = {
                    "method": header[0],
                    "page": header[1],
                    "version": header[2]
                }
            else:
                if header[4] == "application/json":
                    body = "{\n" + request.split("{")[1]
                if header[4] == "text/plain":
                    body = request.split(" ")[len(request.split(" "))-1].split("\n")
                data = {
                    "method": header[0],
                    "page": header[1],
                    "version": header[2],
                    "content-type": header[4],
                    "body": body
                }

            for key in self.events.keys():
                if(key == data["page"]):
                    send = self.events[key](data)

            client_con.sendall(send.encode())
            client_con.close()

    def AddPage(self, page):
        def inner(*args, **kwargs):
            self.events[page] = args[0]
        return inner

class Response:
    ok = "HTTP/1.0 200 OK\n\n"
    notfound = "HTTP/1.0 404 NOT FOUND\n\n"
    nocontent = "HTTP/1.0 204 NO CONTENT\n\n"
    badrequest = "HTTP/1.0 400 BAD REQUEST\n\n"
    forbidden = "HTTP/1.0 403 FORBIDDEN\n\n"
    internalerror = "HTTP/1.0 500 INTERNAL SERVER ERROR\n\n"

