import chess
import chess.engine
from random import choice, shuffle
from math import inf
import asyncio
from time import perf_counter

def generate_random_move(board):
    legalmoves = [move for move in board.legal_moves]
    return choice(legalmoves)

def evaluate_board(board):
    fen = board.fen()
    fen = fen.split()[0]
    score = 0
    for piece in fen:
        match piece:
            case "P":
                score += 1
            case "N":
                score += 3
            case "B":
                score += 3
            case "R":
                score += 5
            case "Q":
                score += 9
            case "p":
                score -= 1
            case "n":
                score -= 3
            case "q":
                score -= 9
            case "r":
                score -= 5
            case "b":
                score -= 3
    return score

def render_til_depth(board, depth):
    pass



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

def get_moves(board):
    moves = [i for i in board.legal_moves]
    shuffle(moves)
    return moves


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
        score = negamaxalphabeta(depth - 1, board, -alpha, -beta, not player)
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
    

"""
for move in legalmoves:
    new_board = board
    evaluate_board(new_board)
    returns minimum and maximum evals
    optimize search for attacks captures and checks

evaluate board
highest eval is move
evaluation algorithm
- positions have score
    heat map to determine where
    early to mid to late game can be determined by number of pieces left
"""


def main():
    board = chess.Board()

    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/fizzy/Downloads/t/stockfish/stockfish-windows-x86-64-avx2.exe")

    sum = 0
    while not board.is_checkmate():
        if board.is_game_over():
            break
        if board.turn:
            start = perf_counter()
            move = negamaxalphabeta(1, board, -inf, inf, True)[1]
            sum += perf_counter() - start
        else:
            # move = generate_random_move(board)
            move = negamax(2, board, False)[1]
            # move = engine.play(board, chess.engine.Limit(depth=1, time=1e-10000)).move
        board.push(move)


    print(board)
    print(board.fullmove_number)
    print(board.outcome())
    print(board.peek())
    print(evaluate_board(board))
    print(sum / (board.fullmove_number // 2))

if __name__ == "__main__":
    while True:
        main()
        input()
