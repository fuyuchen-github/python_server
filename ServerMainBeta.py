import re
import socket


def answer(request_lines):
    try:
        file_name = ''
        ret = re.match(r'[^/]+(/[^ ]*)', request_lines[0])
        if ret:
            file_name = ret.group(1)
            if file_name == '/':
                file_name = '/homepage.html'
    except:
        response = 'HTTP/1.1 404 NOT FOUND\r\n'
        response += '\r\n'
        f = open('./html/404.html', 'rb')
        html_content = f.read()
        f.close()
        return response, html_content

    try:
        f = open('./html' + file_name, 'rb')
    except:
        try:
            file_name += '.html'
            f = open('./html' + file_name, 'rb')
        except:
            response = 'HTTP/1.1 404 NOT FOUND\r\n'
            response += '\r\n'
            f = open('./html/404.html', 'rb')
            html_content = f.read()
            f.close()
            return response, html_content
        else:
            html_content = f.read()
            f.close()
            response = 'HTTP/1.1 200 OK\r\n'
            response += '\r\n'
            return response, html_content
    else:
        html_content = f.read()
        f.close()
        response = 'HTTP/1.1 200 OK\r\n'
        response += '\r\n'
        return response, html_content


def service(new_socket):
    try:
        request = new_socket.recv(1024).decode('utf-8')
    except:
        new_socket.close()
        return 0
    request_lines = request.splitlines()
    if len(request_lines) == 0:
        new_socket.close()
        return 0
    print('*' * 142)
    for x in request_lines:
        print(x)
    res = answer(request_lines)
    res = tuple(res)
    try:
        new_socket.send(res[0].encode('utf-8'))
        new_socket.send(res[1])
    except:
        new_socket.close()
        return 0


def main():
    tcp_service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_service_socket.bind(("", 80))
    tcp_service_socket.listen(16)
    print('service starts!')
    while True:
        new_socket, client_addr = tcp_service_socket.accept()
        print("ip address: %s" % client_addr[1])
        service(new_socket)


if __name__ == "__main__":
    main()
