import socketserver
import json

from db_methods.db_exceptions import MaxPlayersReachedException
from db_methods.requests import connect_player, add_player, initialize_game, open_game, start_game, end_game

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

                try :
                    connect_player(username)

                    response = {
                        'status': 'success',
                        'code': 200,
                        'message': f'Player {username} joined successfully'
                    }

                # if the game has reached the maximum number of players
                except MaxPlayersReachedException as e:
                    # return an error message
                    response = {
                        'status': 'error',
                        'code': 401,
                        'message': str(e)
                    }

            elif action == 'initialize_game':
                try:
                    nb_player = int(request.get('nb_player', 0))
                    map_size = request.get('map_size', '').strip()
                    max_nb_turn = int(request.get('max_nb_turn', 0))
                    max_turn_time = int(request.get('max_turn_time', 0))

                    if not (nb_player > 0 and map_size and max_nb_turn > 0 and max_turn_time > 0):
                        raise ValueError("Invalid parameters")

                    game_id = initialize_game(nb_player, map_size, max_nb_turn, max_turn_time)

                    response = {
                        'status': 'success',
                        'code': 200,
                        'message': f'Game initialized successfully',
                        'game_id': game_id
                    }

                except (ValueError, TypeError) as e:
                    response = {
                        'status': 'error',
                        'code': 400,
                        'message': f'Invalid input parameters: {str(e)}'
                    }

            
            elif action == 'open_game':
                open_game()
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': f'Game opened successfully'
                }
            elif action == 'start_game':
                start_game()
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': f'Game started successfully'
                }
            elif action == 'end_game':
                end_game()
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': f'Game ended successfully'
                }

            elif action == 'add_player':
                username = request.get('username')
                add_player(username)
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': f'Player {username} added successfully'
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