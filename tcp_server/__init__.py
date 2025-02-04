import socketserver
import json

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        if not data:
            return
        try:
            request = json.loads(data.decode('utf-8'))
            name = request.get('name', 'World')
            response = {'message': f'Hello world {name}'}
        except json.JSONDecodeError:
            response = {'error': 'Invalid JSON'}
        self.request.sendall(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = 'localhost', 65432
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f'Server started at {HOST}:{PORT}')
        server.serve_forever()