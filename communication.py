import socket
import re

def erro(a,b):
    raise EOFError("you must appoint a function to answer the requests.")

class Server(object):
    def __init__(self, host_name="", port=80, fun=erro):
        self._tcp_service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tcp_service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._tcp_service_socket.bind((host_name, port))
        self._tcp_service_socket.listen(16)
        self.fun_to_ans = fun
    
    def start_service(self):
        while True:
            self.new_socket, self.client_addr = self._tcp_service_socket.accept()
            self._service()

    def _service(self):
        rec = True
        request = ""
        # while rec:
        #     try:
        rec = self.new_socket.recv(1024)
            # except:
            #     break
        request += rec.decode("utf-8")
        res = self.fun_to_ans(request, self.client_addr)
        for i in tuple(res):
            self.new_socket.send(i)
        self.new_socket.close()

