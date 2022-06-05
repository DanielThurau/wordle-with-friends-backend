from flask import Flask
from flask import request
from flask import abort
from flask_socketio import SocketIO, emit, join_room
from wordle_with_friends_backend.data import *
from wordle_with_friends_backend.lib import *


    

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# TODO validate input arguments to the start game api
def validate_start_game_request(args):
    return True

# TODO validate input arguments to the join game api
def validate_join_game_request(args):
    return True

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)
    print(e)

@socketio.on('connect')
def connect():
    print("Client connected")

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('start_game')
def handle_start_game_event(json):
    if not isinstance(json, dict):
        raise RuntimeError("Not the correct input")
    
    if not validate_start_game_request(json):
        pass
    
    player_name = json.get('player_name')
    player_id = json.get('player_id')
    
    game_state = read_game_state()
    print("GameState" + str(game_state))
    
    new_game_id = generate_unique_game_id(game_state)
        
    player_state = {}
    player_state["player_name"] = player_name 
    player_state["player_board"] = ['u'] * 30
    
    game_state[new_game_id] = {player_id: player_state}
    
    save_game_state(game_state)
    
    join_room(new_game_id)
    
    start_game_response = 'Player: ' + player_name + ' has entered game: ' + str(new_game_id)
    emit('start_game', start_game_response, to=new_game_id)
    
    return {
        "game_id": new_game_id
    }

@socketio.on('join_game')
def handle_start_game_event(json):
    if not can_join_game():
        pass
    
    if not isinstance(json, dict):
        pass
    
    if not validate_join_game_request(request.args):
        pass
    
    # Decode the query parameter arguments
    game_id = json.get('game_id')
    player_id = json.get('player_id')
    player_name = json.get('player_name')
    
    # Decode the query parameter "player_state" and validate it is the correct size
    player_board = request.args.get('player_board', 'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
    decoded_player_board = decode_player_board(player_board)
    if decoded_player_board is None: 
        exit()
    
    # Read in the current data store
    game_state = read_game_state()
    
    # If the game_id is not in the data store there is no game to join
    if game_id not in game_state:
        exit()
        
    # Validate that the user input allows for joining a game
    if player_id in game_state[game_id]:
        # The player_state passed to join_game MUST match the player_state in the data store
        if game_state[game_id][player_id]["player_state"] != decoded_player_board:
            print("Player joined game with incorrect state")
            exit()
        # The player_name passed to join_game MUST match the player_name in the data store
        elif game_state[game_id][player_id]["player_name"] != player_name:
            print("Player_name does not match records")
            exit()

    # Create an entry for the player to join the game
    player_state = {}
    player_state["player_name"] = player_name
    player_state["player_board"] = decoded_player_board 
    game_state[game_id][player_id] = player_state
    
    save_game_state(game_state)

    join_room(game_id)
    
    emit('join_game', game_state[game_id], to=game_id)

    return game_state[game_id]


@socketio.on('guess')
def handle_guess_event(json):
    # Decode the query parameter arguments
    game_id = json.get('game_id')
    player_id = json.get('player_id')
    player_name = json.get('player_name')
    
    # Decode the query parameter "player_state" and validate it is the correct size
    player_board = json.get('player_board')
    
    new_decoded_player_board = decode_player_board(player_board)
    if new_decoded_player_board is None: 
        exit()
    
    if not legal_guess(new_decoded_player_board):
        print("That wasn't a legal guess")
        pass

    # Read in the current data store
    game_state = read_game_state()
    
    # Validate that the user input allows for joining a game
    if player_id in game_state[game_id]:
        # The player_name passed to join_game MUST match the player_name in the data store
        if game_state[game_id][player_id]["player_name"] != player_name:
            print("Player_name does not match records")
            exit()
    else:
        print("Trying to guess in a game you're not part of")
        exit()

    # Read in the current data store
    game_state = read_game_state()
    
    
    game_state[game_id][player_id]["player_board"] = new_decoded_player_board
    
    save_game_state(game_state)
    
    emit('guess', game_state[game_id][player_id], to=game_id)



if __name__ == '__main__':
    socketio.run(app)