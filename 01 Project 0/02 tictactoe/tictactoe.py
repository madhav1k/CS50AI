"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # raise NotImplementedError
    xCounter = 0
    oCounter = 0

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                xCounter += 1
            elif board[i][j] == O:
                oCounter += 1

    if xCounter > oCounter:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError

    possibleActions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # raise NotImplementedError

    for i in range(len(board)):
        for j in range(len(board[0])):
            if action == (i, j) and board[i][j] != EMPTY:
                raise ValueError
            
    if action[0] not in range(len(board)) or action[1] not in range(len(board[0])):
        raise ValueError

    # Create new board, without modifying the original board received as input
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # raise NotImplementedError

    # Check horizontally
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][0] != EMPTY:
        return board[1][0]
    elif board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][0] != EMPTY:
        return board[2][0]
    # Check vertically
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] != EMPTY:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] != EMPTY:
        return board[0][2]
    # Check diagonals
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
   # raise NotImplementedError

    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None):
        return True
    else:
        return False
    # return True if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # raise NotImplementedError

    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # raise NotImplementedError

    if terminal(board):
        return None
    else:
        if player(board) == X:
            # user chose O so AI is X, X will always be utility maximizer

            # maximize X's gain (gain = uti) (MAXImin), minimize X's loss (loss = -uti) (MINImax)
            uti, move = maximize(board)
            return move
        else:
            # user chose X so AI is O, O will always be utility minimizer

            # minimize O's loss (loss = uti) (MINImax), maximize O's gain (gain = -uti) (MAXImin)
            uti, move = minimize(board)
            return move


def maximize(board):
    """
    Maximizes board utility, X is the maximizer.
    """
    if terminal(board):
        return utility(board), None

    uti = float('-inf')
    move = None
    for act in actions(board):
        # uti = max(uti, minimize(result(board, act)))

        # minimizing utility for every action (X's gain, opponent O's loss) (maxiMIN) equivalent to maximizing -utility for every action (X's loss, opponent O's gain) (miniMAX)
        min_uti, min_act = minimize(result(board, act))
        
        # maximizing utility for X: taking maxima from minimum utilities (maximize X's gain, opponent O's loss) (MAXImin) equivalent to taking minima from maximum -utilities (X's loss, opponent O's gain) (MINImax)
        if min_uti > uti:
            uti = min_uti
            move = act
            if uti == 1:
                return uti, move

    return uti, move


def minimize(board):
    """
    Minimizes board utility, O is the minimizer.
    """
    if terminal(board):
        return utility(board), None

    uti = float('inf')
    move = None
    for act in actions(board):
        # uti = min(uti, maximize(result(board, act)))

        # maximizing utility for every action (O's loss, opponent X's gain) (miniMAX) equivalent to minimizing -utility for every action (O's gain, opponent X's loss) (maxiMIN)
        max_uti, max_act = maximize(result(board, act))
        
        # minimizing utility for O: taking minima from maximum utilities (minimize O's loss, opponent X's gain) (MINImax) equivalent to taking maxima from minimum -utilities (O's gain, opponent X's loss) (MAXImin)
        if max_uti < uti:
            uti = max_uti
            move = act
            if uti == -1:
                return uti, move

    return uti, move