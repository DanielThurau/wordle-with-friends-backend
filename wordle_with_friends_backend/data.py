import json

def read_game_state():
    return read_json()

def read_json():
    with open('json_data.json') as json_file:
        data = json.load(json_file)
        return data

    
def save_game_state(game_state):
    write_json(game_state)
    
    
def write_json(game_state):
    with open('json_data.json', 'w') as outfile:
        json.dump(game_state, outfile)