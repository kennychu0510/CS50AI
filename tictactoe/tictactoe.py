"""
Tic Tac Toe Player
"""

import math
from xml.dom import InvalidAccessErr
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


def empty(board):
    for row in board:
        for cell in row:
            if cell != EMPTY:
                return False
    return True


def cells_occupied(board):
    occupied = 0
    for row in board:
        for cell in row:
            if cell != EMPTY:
                occupied += 1
    return occupied


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # Check if board is empty
    if empty(board):
        return X

    # Board is not empty
    # 3 cases:
    #   1. board is full, cells_occupied == 9
    if cells_occupied(board) == 9:
        return None

    #   2. If number of occupied cells is even, X's turn
    if cells_occupied(board) % 2 == 0:
        return X

    #   3. If number of occupied cells is odd, O's turn
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    i = j = 0
    possible_moves = set()
    for row in board:
        for cell in row:
            if cell == EMPTY:
                possible_moves.add((i, j))
            j += 1
        i += 1
        j = 0

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    board_clone = copy.deepcopy(board)
    # If action is not valid, ie. action is taking place on a cell that is not empty
    if board[i][j] != EMPTY:
        raise ValueError

    # Update board reflecting the action
    board_clone[i][j] = player(board)

    return board_clone


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows:
    for row in range(3):
        for col in range(1, 3):
            winner = board[row][0]
            if board[row][col] != winner:
                break
            if col == 2:
                return winner

    # Check columns:
    for col in range(3):
        for row in range(1, 3):
            winner = board[0][col]
            if board[row][col] != winner:
                break
            if row == 2:
                return winner

    # Check diagonally from top left down
    for x in range(1, 3):
        winner = board[0][0]
        if board[x][x] != winner:
            break
        if x == 2:
            return winner

    # Check diagonally from top right down
    for x in range(1, 3):
        winner = board[0][2]
        if board[x][2-x] != winner:
            break
        if x == 2:
            return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner
    if winner(board) != None:
        return True

    # Check if all cells are filled
    if cells_occupied(board) == 9:
        return True

    # Game is still going
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # return none if game is over (terminal board is true)
    if terminal(board):
        return None

    # X wants to maximize the score
    # O wants to minimize the score

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -1000
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = 1000
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    # Create a dictionary that stores all possible moves and their utility number
    optimal_actions = {}

    for action in actions(board):
        board_after_action = result(board, action)
        if player(board) == X:
            optimal_actions[action] = max_value(board_after_action)
        else:
            optimal_actions[action] = min_value(board_after_action)

    # Check the dictionary for the action with the highest utility, if multiple action contains the same utility, the first action from the set will be returned
    if player(board) == X:
        return max(optimal_actions, key=optimal_actions.get)
    elif player(board) == O:
        return min(optimal_actions, key=optimal_actions.get)
