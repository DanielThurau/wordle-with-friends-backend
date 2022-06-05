import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on('start_game')
def start_game(data):
    print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})
    
@sio.on('join_game')
def join_game(data):
    print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})
    
@sio.on('guess')
def guess(data):
    print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})

@sio.on('error')
def on_error_default(data):
    print('message received with ', data)
    
@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://127.0.0.1:5000')
sio.emit('start_game', {'player_name': 'Daniel', 'player_id': '01'})
# sio.emit('start_game', "Hello world from not a dict")
id = input('What\'s the game_id?.\n')

sio.emit('join_game', {'player_name': 'Spencer', 'player_id': '02', 'game_id': id})

time.sleep(5)

sio.emit('guess', {'player_name': 'Spencer', 'player_id': '02', 'game_id': id, "player_board": "cccccuuuuuuuuuuuuuuuuuuuuuuuuu"})



sio.wait()