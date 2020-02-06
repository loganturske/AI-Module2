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
    if board in history:
        if player is 'O':
            return {'done': True, 'winner': 'X'}
        elif player is 'X':
            return {'done': True, 'winner': "O"}
    return {'done': False, 'winner': None}


def minimax_versus_random():
    board = push.create()
    print_board(board)
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
