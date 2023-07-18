from math import inf
from random import choice, shuffle

from eval import evaluate_board



def get_moves(board):
    moves = [i for i in board.legal_moves]
    shuffle(moves)
    return moves

def generate_random_move(board):
    legalmoves = [move for move in board.legal_moves]
    return choice(legalmoves)

# def minimax(depth, board, alpha, beta, player):
#     # print(f"Minimax called with depth = {depth} and player = {player}")
#     if depth == 0:
#         return (evaluate_board(board), 0)
#     legal_moves = board.legal_moves
#     best_move = 0
#     if player:
#         max = -inf
#         for move in legal_moves:
#             board.push(move)
#             score = minimax(depth - 1, board, alpha, beta, not player)
#             last_move = board.pop()
#             if score[0] > max:
#                 max = score[0]
#                 best_move = last_move
#         return (max, best_move)
#     else:
#         min = inf
#         for move in legal_moves:
#             board.push(move)
#             score = minimax(depth - 1, board, alpha, beta, not player)
#             last_move = board.pop()
#             if score[0] < min:
#                 min = score[0]
#                 best_move = last_move
#         return (min, best_move)

def negamaxalphabeta(depth, board, alpha, beta, player):
    if depth == 0:
        evaluation = evaluate_board(board)
        if not player: evaluation *= -1
        return (evaluation, 0)

    value = -inf
    legal_moves = get_moves(board)
    best_move = 0
    for move in legal_moves:
        board.push(move)
        score = negamaxalphabeta(depth - 1, board, -beta, -alpha, not player)
        last_move = board.pop()
        if -score[0] > value:
            value = -score[0]
            best_move = last_move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    
    return (value, best_move)

def negamax(depth, board, player):
    if depth == 0:
        evaluation = evaluate_board(board)
        if not player: evaluation *= -1
        return (evaluation, 0)
    max = -inf
    legal_moves = get_moves(board)
    best_move = 0
    for move in legal_moves:
        board.push(move)
        score = negamax(depth - 1, board, not player)
        last_move = board.pop()
        if -score[0] > max:
            max = -score[0]
            best_move = last_move
    
    return (max, best_move)