import push

def print_board(board):
    for row in board:
        row_str = ''
        for col in row:
            row_str += col
        print(row_str)


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
