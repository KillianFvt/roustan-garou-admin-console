import json
import socket

from db_methods.requests import initialize_game, end_game


def test_player_join_request(host='localhost', port=65432, name='YoussefGoat'):

    initialize_game(2, "5x6", 20, 10)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = json.dumps(
            {'action': 'player_join', 'username': name}
        )
        s.sendall(request.encode('utf-8'))
        response = s.recv(1024)
        print('Received', response.decode('utf-8'))

    end_game()

if __name__ == "__main__":
    test_player_join_request(name='YoussefGoat')