import uuid

def generate_unique_game_id(game_state):
    game_id = str(uuid.uuid1())
    while game_id in game_state:
        game_id = str(uuid.uuid1())
    return game_id
        
def decode_player_board(player_board_string):
    player_board = list(map(str, player_board_string))
    if len(player_board) != 30:
        print("player_state is not in the correct format")
        return None
    return player_board

def can_join_game():
    return True

def legal_guess(guess):
    return True