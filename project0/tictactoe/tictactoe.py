"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If given an empty board, return X
    if not any(any(row) for row in board):
        return X

    # Count the X's and O's in the board
    count_of_X = sum(row.count(X) for row in board)
    count_of_O = sum(row.count(O) for row in board)

    # Compare the occurances of X and O in the board to determine who goes next
    # Any output is acceptable in the case of terminal state,
    # so we don't have to worry about it
    if count_of_X > count_of_O:
        # If X has had more turns than O, it's O's turn now
        return O
    else:
        # Else it's X's turn now, since X always starts the game
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Any place in the board which is EMPTY is available
    result = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if not col:
                result.add((i, j))

    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Validate the action
    if action not in actions(board):
        raise RuntimeError("Move not allowed!")

    # Determine the player
    pl = player(board)

    # Make a deep copy of the board and play the move
    result = deepcopy(board)
    result[action[0]][action[1]] = pl

    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i, row in enumerate(board):
        # Check rows
        if (
            board[i][0] == board[i][1]
            and board[i][1] == board[i][2]
            and board[i][2] != None
        ):
            return board[i][0]
        # Check columns
        if (
            board[0][i] == board[1][i]
            and board[1][i] == board[2][i]
            and board[2][i] != None
        ):
            return board[0][i]

    # Check diagonals
    if (
        board[0][0] == board[1][1]
        and board[1][1] == board[2][2]
        and board[2][2] != None
    ):
        return board[0][0]
    if (
        board[0][2] == board[1][1]
        and board[1][1] == board[2][0]
        and board[2][0] != None
    ):
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If the board is full and it is a tie
    if winner(board) is None and len(actions(board)) == 0:
        return True
    # If the board is not yet full but there is a winner
    elif winner(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)
    if won == X:
        return 1
    elif won == O:
        return -1
    else:
        return 0


def maxValue(state):
    v = -math.inf
    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v


def minValue(state):
    v = math.inf
    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If the game's over, no use continuing
    if terminal(board):
        return None

    # Determine whose turn it is
    turn = player(board)
    temp = []

    # Helper function, serves as a fn to be passed as key to max and min
    def get_second_elem(tupl):
        return tupl[1]

    if turn == O:
        # Minimizing player
        temp[:] = []
        for action in actions(board):
            temp.append((action, maxValue(result(board, action))))
        pair = min(temp, key=get_second_elem)
        return pair[0]
    else:
        # Maximizing player
        temp[:] = []
        for action in actions(board):
            temp.append((action, minValue(result(board, action))))
        pair = max(temp, key=get_second_elem)
        return pair[0]
