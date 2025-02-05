import socketserver
import json

from db_methods.requests import connect_player


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        if not data:
            return
        try:
            request = json.loads(data.decode('utf-8'))
            action = request.get('action')
            if action == 'player_join':
                username = request.get('username')
                print(f"Player joined: {username}")
                connect_player(username)
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': f'Player {username} joined successfully'
                }

            else:
                response = {
                    'status': 'error',
                    'code': 404,
                    'message': 'Invalid action'
                }
        except json.JSONDecodeError:
            response = {
                'status': 'error',
                'code': 400,
                'message': 'Invalid JSON'
            }
        except Exception as e:
            response = {
                'status': 'error',
                'code': 500,
                'message': str(e)
            }
        self.request.sendall(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = 'localhost', 65432
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f'Server started at {HOST}:{PORT}')
        server.serve_forever()