import socket
import json

def send_request(host='localhost', port=65432, name='YourName'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = json.dumps({'name': name})
        s.sendall(request.encode('utf-8'))
        response = s.recv(1024)
        print('Received', response.decode('utf-8'))

if __name__ == "__main__":
    send_request(name='YourName')