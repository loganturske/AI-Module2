import push
import random

alpha = -1
beta = 1000
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


def minimax_move(board, player, max_ply, history):
    """
    Minimax algorithm playing to play push with limited ply
    :param board: a game board
    :param player: a player
    :param max_ply: number of ply to search out to
    :param history: the history of the game
    :return: a game board
    """
    # Set default values and see what is the best move
    value = -1
    action = actions(board)[0]
    for a in actions(board):
        res = min_value(result(board, a, player), opponent(player), 1, max_ply, history)
        if value < res:
            value = res
            action = a
    # Make the move
    return push.move(board, (player, action.get('side'), action.get('index')))


def alpha_beta_move(board, player, max_ply, history):
    """
    Minimax algorithm playing to play push with limited ply and alpha beta pruning
    :param board: a game board
    :param player: a player
    :param max_ply: number of ply to search out to
    :param history: the history of the game
    :return: a game board
    """
    # Set default values and see what is the best move
    value = -1
    action = actions(board)[0]
    # Reset alpha beta values
    global alpha
    global beta
    alpha = 1000
    beta = -1
    for a in actions(board):
        res = max_value_alpha_beta(result(board, a, player), opponent(player), 1, max_ply, history)
        if value < res:
            value = res
            action = a
    # Make the move
    return push.move(board, (player, action.get('side'), action.get('index')))


def max_value_alpha_beta(board, player, ply, max_ply, history):
    """
    Max value portion of the minimax algorithm with alpha beta pruning
    :param board: a game board
    :param player: a player
    :param ply: current ply
    :param max_ply: max ply to go to
    :param history: the history of the game
    :return: a node value
    """
    global alpha
    # Base Case, if you have reached max play just get value so far
    if ply is max_ply:
        return utility(board, player, history)
    # Choose the smallest value based on the min value portion of the minimax algorithm and return it
    v = -100

    for a in actions(board):
        v = max(v, min_value_alpha_beta(result(board, a, player), opponent(player), ply+1, max_ply, history))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def max_value(board, player, ply, max_ply, history):
    """
    Max value portion of the minimax algorithm
    :param board: a game board
    :param player: a player
    :param ply: current ply
    :param max_ply: max ply to go to
    :param history: the history of the game
    :return: value of node
    """
    # Base Case, if you have reached max play just get value so far
    if ply is max_ply:
        return utility(board, player, history)
    # Choose the smallest value based on the min value portion of the minimax algorithm and return it
    v = -1
    for a in actions(board):
        v = max(v, min_value(result(board, a, player), opponent(player), ply+1, max_ply, history))

    return v


def min_value_alpha_beta(board, player, ply, max_ply, history):
    """
    Min value portion of the minimax algorithm with alpha beta pruning
    :param board: a game board
    :param player: a player
    :param ply: current ply
    :param max_ply: max ply to go to
    :param history: the history of the game
    :return: value of node
    """
    global beta
    # Base Case, if you have reached max play just get value so far
    if ply is max_ply:
        return utility(board, player, history)
    v = 1000
    # Choose the smallest value based on the min value portion of the minimax algorithm and return it
    for a in actions(board):
        v = min(v, max_value_alpha_beta(result(board, a, player), opponent(player), ply+1, max_ply, history))
        if v <= alpha:
            return v
        beta = min(beta, v)
        print(beta)
    return v


def min_value(board, player, ply, max_ply, history):
    """
    Min value portion of the minimax algorithm
    :param board: a game board
    :param player: a player
    :param ply: current ply
    :param max_ply: max ply to go to
    :param history: the history of the game
    :return:
    """

    # Base Case, if you have reached max play just get value so far
    if ply is max_ply:
        return utility(board, player, history)
    v = 1000
    # Choose the smallest value based on the min value portion of the minimax algorithm and return it
    for a in actions(board):
        v = min(v, max_value(result(board, a, player), opponent(player), ply+1, max_ply, history))
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
        for index in range(len(board)):
            actions.append({'side': direction, 'index': index+1})
    return actions


def utility(board, player, history):
    """
    Get the utility of the board based on this player
    :param board: a game board
    :param player: a player
    :param history: the history of the game
    :return: integer of the utility of the board
    """
    res = game_done(board, player, history)
    # If you will win at this node
    if res.get('done') and res.get('winner') is player:
        return 50
    # If your opponent will win
    elif res.get('done') and res.get('winner') is opponent(player):
        return 0
    # If you have less straights than your opponents
    if push.straights(board).get(player) < push.straights(board).get(opponent(player)):
        return 0
    # How many straights will you have +1
    return push.straights(board).get(player) + 1


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
        return {'done': True, 'winner': 'O', 'board': board}
    elif xPlayer > oPlayer:
        return {'done': True, 'winner': 'X', 'board': board}
    # Determine if the player caused a cycle
    for old in history:
        if push.equal(board, old):
            if player is 'O':
                return {'done': True, 'winner': 'X', 'board':  board}
            elif player is 'X':
                return {'done': True, 'winner': "O", 'board': board}
    return {'done': False, 'winner': None, 'board': board}


def play_round_minimax_v_random(first, ply):
    """
    This will play a round of Push
    :param: will minimax go first
    :param: max ply
    :return: (done, winner, board)
    """
    board = push.create()
    history = []
    # If Minimax is going first play a round
    if first:
        while True:
            # Make a move
            board = minimax_move(board, 'X', ply, history)
            # Get the outcome of the move and determine if someone won the game
            outcome = game_done(board, 'X', history)
            if outcome.get('done'):
                return outcome
            history.append(board)
            board = random_move(board, 'O')
            outcome = game_done(board, 'O', history)
            if outcome.get('done'):
                return outcome
            history.append(board)
    else:
        while True:
            board = random_move(board, 'X')
            outcome = game_done(board, 'X', history)
            if outcome.get('done'):
                return outcome
            history.append(board)
            board = minimax_move(board, 'O', ply, history)
            outcome = game_done(board, 'O', history)
            if outcome.get('done'):
                return outcome
            history.append(board)


def play_round_minimax_v_alpha_beta(first, ply, alphaPly):
    """
    This will play a round of Push
    :param: will minimax go first
    :param: max ply
    :param alphaPly: how many ply for alpha beta to search
    :return: (done, winner, board)
    """
    board = push.create()
    history = []
    # If Minimax is going first play a round
    if first:
        while True:
            # Make a move
            board = minimax_move(board, 'X', ply, history)
            # Get the outcome of the move and determine if someone won the game
            outcome = game_done(board, 'X', history)
            if outcome.get('done'):
                return outcome
            history.append(board)
            board = alpha_beta_move(board, 'O', alphaPly, history)
            outcome = game_done(board, 'O', history)
            if outcome.get('done'):
                return outcome
            history.append(board)
    else:
        while True:
            board = alpha_beta_move(board, 'X', alphaPly, history)
            outcome = game_done(board, 'X', history)
            if outcome.get('done'):
                return outcome
            history.append(board)
            board = minimax_move(board, 'O', ply, history)
            outcome = game_done(board, 'O', history)
            if outcome.get('done'):
                return outcome
            history.append(board)


def minimax_versus_random():
    """
    Play push 5 times switching who goes first
    :return: nothing
    """
    minimax = 0
    rand = 0
    ply = 3
    first = True
    board = []
    print("Minimax Player is searching " + str(ply) + " ply.")
    # Play push 5 times switching who goes first
    for n in range(5):
        outcome = play_round_minimax_v_random(first, ply)
        if first and outcome.get('winner') is 'X':
            minimax += 1
        elif not first and outcome.get('winner') is 'O':
            minimax += 1
        else:
            rand += 1
        first = not first
        board = outcome.get('board')
    print("Minimax: " + str(minimax))
    print("Random: " + str(rand))
    print()
    print_board(board)


def minimax_versus_alphabeta():
    """
    Play push 5 times switching who goes first
    :return: nothing
    """
    minimax = 0
    alphawins = 0
    ply = 3
    alphaPly = 7
    first = True
    board = []
    print("Minimax Player is searching " + str(ply) + " ply.")
    print("Alpha Beta Player is searching " + str(alphaPly) + " ply.")
    # Play push 5 times switching who goes first
    for n in range(5):
        outcome = play_round_minimax_v_alpha_beta(first, ply, alphaPly)
        if first and outcome.get('winner') is 'X':
            minimax += 1
        elif not first and outcome.get('winner') is 'O':
            minimax += 1
        else:
            alphawins += 1
        first = not first
        board = outcome.get('board')

    print("Minimax: " + str(minimax))
    print("AlphaBeta: " + str(alphawins))
    print()
    print_board(board)


if __name__ == "__main__":
    print("Random v. Minimax")
    minimax_versus_random()
    print("\nMinimax v. Alpha Beta")
    minimax_versus_alphabeta()
