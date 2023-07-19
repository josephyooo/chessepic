from math import inf
from random import choice, shuffle

import chess

from eval import evaluate_board, PIECE_VALUES



def get_moves(board, player):
    """
    returns list of moves in optimized order
    attacks **pinned pieces still attack**
    is_attacked
    attackers see above
    pin command

    
    """
    PIECE_TYPES = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

    PIECE_TRANSLATE = {
        chess.PAWN: "P",
        chess.KNIGHT:"N",
        chess.BISHOP: "B",
        chess.ROOK: "R",
        chess.QUEEN: "Q",
        chess.KING: "K",
    }


    color = chess.WHITE if player else chess.BLACK
    moves = [i for i in board.legal_moves]
    #for the moves in list, order by piece type| piece_type_at
    # from moves find piece type at from square
    pieces = []
    for move in moves:
        pieces.append(board.piece_type_at(move.from_square))
    
    sorted_moves = [move for _,move in sorted(zip(pieces, moves), key=lambda pair: PIECE_VALUES[PIECE_TRANSLATE[pair[0]]], reverse=True)]
    # sorted_moves.sort(reverse=True, key=lambda piece: PIECE_VALUES[PIECE_TRANSLATE[piece]])

    # shuffle(moves)
    return sorted_moves



def generate_random_move(board):
    legalmoves = [move for move in board.legal_moves]
    return choice(legalmoves)

def user_move(board):
    while True:
        move = chess.Move.from_uci(input())
        if move in board.legal_moves:
            break
        print("invalid move")
    return move

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
        return (evaluation, board.peek())

    value = -inf
    legal_moves = get_moves(board, player)
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
    legal_moves = get_moves(board, player)
    best_move = 0
    for move in legal_moves:
        board.push(move)
        score = negamax(depth - 1, board, not player)
        last_move = board.pop()
        if -score[0] > max:
            max = -score[0]
            best_move = last_move
    
    return (max, best_move)