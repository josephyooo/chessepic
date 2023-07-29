from math import inf
from random import choice, shuffle

import chess

from eval import evaluate_board, PIECE_VALUES


def get_moves(board, player, captures_only=False):
    """
    returns list of moves in optimized order
    attacks **pinned pieces still attack**
    is_attacked
    attackers see above
    pin command


    """
    PIECE_TYPES = [
        chess.PAWN,
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN,
        chess.KING,
    ]

    PIECE_TRANSLATE = {
        chess.PAWN: "P",
        chess.KNIGHT: "N",
        chess.BISHOP: "B",
        chess.ROOK: "R",
        chess.QUEEN: "Q",
        chess.KING: "K",
    }

    color = chess.WHITE if player else chess.BLACK
    moves = [i for i in board.legal_moves]
    if captures_only:
        moves = [move for move in moves if move.is_capture()]
    # for the moves in list, order by piece type| piece_type_at
    # from moves find piece type at from square
    pieces = []
    for move in moves:
        pieces.append(board.piece_type_at(move.from_square))

    sorted_moves = [
        move
        for _, move in sorted(
            zip(pieces, moves),
            key=lambda pair: PIECE_VALUES[PIECE_TRANSLATE[pair[0]]],
            reverse=True,
        )
    ]
    # sorted_moves.sort(reverse=True, key=lambda piece: PIECE_VALUES[PIECE_TRANSLATE[piece]])
    # takes sorted moves and orders them based off whether they attack, capture, or whatever

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


def static_evaluation(board, player):
    evaluation = evaluate_board(board)
    if not player:
        evaluation *= -1
    return evaluation


def negamaxalphabeta(self, depth, board, alpha, beta, player, captures_only):
    if depth == 0:
        # search remaining captures
        result = negamaxalphabeta(self, -1, board, -beta, -alpha, not player, True)
        # if not result:
        #     evaluation = static_evaluation(board, player)
        #     return (evaluation, board.peek())
        return result

    value = -inf
    legal_moves = get_moves(board, player, captures_only=captures_only)
    if not legal_moves and captures_only:
        evaluation = static_evaluation(board, player)
        return (evaluation, board.peek())
    best_move = 0
    for move in legal_moves:
        if self.stop_event.is_set():
            return False
        board.push(move)
        result = negamaxalphabeta(
            self, depth - 1, board, -beta, -alpha, not player, captures_only
        )
        if not result:
            return False
        last_move = board.pop()
        if -result[0] > value:
            value = -result[0]
            best_move = last_move
        if best_move == 0:
            best_move = legal_moves[0]
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    return (value, best_move)


# def negamax(depth, board, player):
#     if depth == 0:
#         evaluation = evaluate_board(board)
#         if not player: evaluation *= -1
#         return (evaluation, 0)
#     max = -inf
#     legal_moves = get_moves(board, player)
#     best_move = 0
#     for move in legal_moves:
#         board.push(move)
#         score = negamax(depth - 1, board, not player)
#         last_move = board.pop()
#         if -score[0] > max:
#             max = -score[0]
#             best_move = last_move

#     return (max, best_move)
