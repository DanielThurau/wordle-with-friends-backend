import uuid
import json
from flask import Flask
from flask import request
from flask import abort


def read_json():
    with open('json_data.json') as json_file:
        data = json.load(json_file)
        return data
    
def write_json(data):
    with open('json_data.json', 'w') as outfile:
        json.dump(data, outfile)

def decode_player_state_string(player_state_string):
    return list(map(int, player_state_string))
    

app = Flask(__name__)

@app.route('/start_game', methods=['POST'])
def start_game():
    if request.method == 'POST':
        player_name = request.args['player_name']
        player_id = request.args['player_id']
        
        data = read_json()

        game_id = str(uuid.uuid1())
        while game_id in data:
            game_id = str(uuid.uuid1())
            
        game = {}
        game["player_name"] = player_name
        game["player_state"] = [0] * 30
        
        data[game_id] = {player_id: game}
        
        write_json(data)
        
        return {
            "game_id": game_id
        }

@app.route('/join_game', methods=['POST'])
def join_game():
    if request.method == 'POST':
        # Decode the query parameter arguments
        game_id = request.args['game_id']
        player_id = request.args['player_id']
        player_name = request.args["player_name"]
        
        # Decode the query parameter "player_state" and validate it is the correct size
        player_state = request.args["player_state"]
        player_state_decoded = decode_player_state_string(player_state)
        if len(player_state_decoded) != 30: 
            print("player_state is not in the correct format")
            abort(400)
        
        # Read in the current data store
        data = read_json()
        
        # If the game_id is not in the data store there is no game to join
        if game_id not in data:
            abort(400)
            
        # Validate that the user input allows for joining a game
        if player_id in data[game_id]:
            # The player_state passed to join_game MUST match the player_state in the data store
            if data[game_id][player_id]["player_state"] != player_state_decoded:
                print("Player joined game with incorrect state")
                abort(400)
            # The player_name passed to join_game MUST match the player_name in the data store
            elif data[game_id][player_id]["player_name"] != player_name:
                print("Player_name does not match records")
                abort(400)

        # Create an entry for the player to join the game
        game = {}
        game["player_name"] = player_name
        game["player_state"] = player_state_decoded
        data[game_id][player_id] = game
        
        write_json(data)

        return data