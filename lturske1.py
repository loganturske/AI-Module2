import push
import random

def random_move(board, player, n: int=4):
    """
    Makes a random move on the board passed in from the player passed in
    :param board: a game board
    :param player: a player
    :param n: size of the board, default 4
    :return: a game board
    """
    directions = ['T', 'B', 'L', 'R']
    return push.move(board, (player, random.choice(directions), random.randint(1, n)))


def minimax_move(board, player, max_ply):
    """
    Minimax algorithm playing to play push with limited ply
    :param board: a game board
    :param player: a player
    :param max_ply: number of ply to search out to
    :param n: size of the board, default 4
    :return: a game board
    """
    # Set defualt values and see what is the best move
    value = -1
    action = actions(board).pop()
    for a in actions(board):
        res = min_value(result(board, a, player), opponent(player), 1, max_ply)
        if value < res:
            value = res
            action = a
    return push.move(board, (player, action.get('side'), action.get('index')))


def max_value(board, player, ply, max_ply):
    """
    Max value portion of the minimax algorithm
    :param board: a game board
    :param player: a player
    :param ply: current ply
    :param max_ply: max ply to go to
    :return:
    """
    # Base Case, if you have reached max play just get value so far
    if ply is max_ply:
        return utility(board, player)
    # Choose the smallest value based on the min value portion of the minimax algorithm and return it
    v = -1
    for a in actions(board):
        res = min_value(result(board, a, player), opponent(player), ply+1, max_ply)
        if v < res:
            v = res
    return v


def min_value(board, player, ply, max_ply):
    """
    Min value portion of the minimax algorithm
    :param board: a game board
    :param player: a player
    :param ply: current ply
    :param max_ply: max ply to go to
    :return:
    """
    # Base Case, if you have reached max play just get value so far
    if ply is max_ply:
        return utility(board, player)
    v = 1000
    # Choose the smallest value based on the min value portion of the minimax algorithm and return it
    for a in actions(board):
        res = max_value(result(board, a, player), opponent(player), ply+1, max_ply)
        if v > res:
            v = res
    return v


def opponent(player):
    """
    Returns the opponent of the player
    :param player: a player
    :return: opponent player
    """
    if player is 'X':
        return 'O'
    return 'X'


def result(board, action, player):
    """
    Returns a board that with the move taken
    :param board: a game board
    :param action: an action to take
    :param player: a player
    :return: a game board
    """
    return push.move(board, (player, action.get('side'), action.get('index')))


def actions(board):
    """
    Get all the actions you can take on the board
    :param board: a game board
    :return: list of actions
    """
    directions = ['T', 'B', 'L', 'R']
    actions = []
    for direction in directions:
        for index in range(len(board)-1):
            actions.append({'side': direction, 'index': index+1})
    return actions


def utility(board, player):
    """
    Get the utility of the board based on this player
    :param board: a game board
    :param player: a player
    :return: integer of the utility of the board
    """
    return push.straights(board).get(player)


def print_board(board):
    """
    Prints the board passed in
    :param board: a game board
    """
    # Go through the rows and make a pretty print string of the row and print it
    for row in board:
        row_str = ''
        for col in row:
            row_str += col
        print(row_str)


def game_done(board, player, history):
    """
    Determines if the game is done given a board

    :param board: a game board
    :param player: a player who just took the turn
    :param history: the games previous board states
    :return: {done: boolean, winner: str}
    """

    # Get number of straight from each player
    straights = push.straights(board)
    oPlayer = straights.get('O')
    xPlayer = straights.get('X')

    # Determine if a player has more straights
    if oPlayer > xPlayer:
        return {'done': True, 'winner': 'O'}
    elif xPlayer > oPlayer:
        return {'done': True, 'winner': 'X'}
    # Determine if the player caused a cycle
    for old in history:
        if push.equal(board, old):
            print("ASDF")
            if player is 'O':
                return {'done': True, 'winner': 'X'}
            elif player is 'X':
                return {'done': True, 'winner': "O"}
    return {'done': False, 'winner': None}

def minimax_versus_random():
    board = push.create()
    history = []
    outcome = None
    while True:
        board = minimax_move(board, 'X', 3)
        if game_done(board, 'X', history).get('done'):
            print("Winner: " + game_done(board, 'X', history).get('winner'))
            break
        history.append(board)
        board = random_move(board, 'O')
        if game_done(board, 'O', history).get('done'):
            print("Winner: " + game_done(board, 'O', history).get('winner'))
            break
        history.append(board)
    #print_board(board)
    pass # remove


def minimax_versus_alphabeta():
    ### YOUR SOLUTION HERE ###
    # Refer to the PDF for an example of the output this function should print.
    ### YOUR SOLUTION HERE ### 
    pass # remove


if __name__ == "__main__":
    print("Random v. Minimax")
    minimax_versus_random()
    #print("\nMinimax v. Alpha Beta")
    #minimax_versus_alphabeta()
