"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # initialized the starting board
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # counter for X and O
    countX, countO = 0, 0
    # count X and O in board
    for x in board:
        for y in x:
            if y == 'X':
                countX += 1
            elif y == 'O':
                countO += 1
    # if there is more X than O in board
    if countX > countO:
        return O
    # if there is equal number of X and O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # find all None cooordinates in form of tuple (x,y) and return as a list
    return [(x, y) for y in range(len(board[0])) for x in range(len(board)) if board[x][y] == None]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # find who is the current player
    who = player(board)
    # if the player is O
    if who == 'O':
        board[action[0]][action[1]] = 'O'
    # else the player is X
    else:
        board[action[0]][action[1]] = 'X'
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check who win
    ans = utility(board)
    # if the result is 1 means X player has won
    if ans == 1:
        return X
    # else the result is -1 means O player has won
    elif ans == -1:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # initialize new board for input -1, 0, 1 as O, None, X in copy of board
    board2 = [[1 if y == 'X' else (-1 if y == 'O' else 0) for y in x] for x in board]
    # check any win in row
    for x in range(len(board2)):
        if sum(board2[x]) == -3 or sum(board2[x]) == 3:
            return True
    # check any win in column
    sum_columns = [sum(x) for x in zip(*board2)]
    if 3 in sum_columns or -3 in sum_columns:
        return True
    # check any win in diagonal
    left_right = sum(board2[i][i] for i in range(len(board2)))
    right_left = sum(board2[i][len(board2) - i - 1] for i in range(len(board2)))
    if left_right == -3 or left_right == 3 or right_left == -3 or right_left == 3:
        return True
    # check any None in board
    if None not in board[0] and None not in board[1] and None not in board[2]:
        return True
    # if no win
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # initialize new board for input -1, 0, 1 as O, None, X in copy of board
    board2 = [[1 if y == 'X' else (-1 if y == 'O' else 0) for y in x] for x in board]
    # check any win in row
    for x in range(len(board2)):
        if sum(board2[x]) == 3:
            return 1
        elif sum(board2[x]) == -3:
            return -1
    # check any win in column
    sum_columns = [sum(x) for x in zip(*board2)]
    if 3 in sum_columns:
        return 1
    elif -3 in sum_columns:
        return -1
    # check any win in diagonal
    left_right = sum(board2[i][i] for i in range(len(board2)))
    right_left = sum(board2[i][len(board2) - i - 1] for i in range(len(board2)))
    if left_right == 3 or right_left == 3:
        return 1
    elif left_right == -3 or right_left == -3:
        return -1
    # if no one will win
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # finding max/alpha
    def maxval(board):
        # copy board
        board2 = [[y for y in x] for x in board]
        # check if board is ended
        if terminal(board2):
            return (utility(board2), None)
        # initialize for searching max answer
        v = -1000
        # initialize for finding coordinates
        best = []
        # get all possible coordinates to be played
        action = actions(board2)
        for coor in action:
            test = minval(result(board2, coor))
            # if there is higher value
            if v <= test[0]:
                v = test[0]
                best.append(coor)
        # return value and coorinate in tuple
        return (v, best)

    # finding min/beta
    def minval(board):
        # copy board
        board2 = [[y for y in x] for x in board]
        # check if board is ended
        if terminal(board2):
            return (utility(board2), None)
        # initialize for searching min answer
        v = 1000
        # initialize for finding coordinates
        best = []
        # get all possible coordinates to be played
        action = actions(board2)
        for coor in action:
            test = maxval(result(board2, coor))
            # if there is lower value
            if v >= test[0]:
                v = test[0]
                best.append(coor)
        # return value and coorinate in tuple
        return (v, best)

    # return the coordinates as action
    choices=maxval(board)[1]
    import random
    return random.choice(choices)