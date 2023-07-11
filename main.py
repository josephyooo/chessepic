import chess
import chess.engine
from random import choice

def generate_random_move(board):
    legalmoves = [move for move in board.legal_moves]
    return choice(legalmoves)

def evaluate_board(board):
    fen = board.fen()
    fen = fen.split()[0]
    print(fen)
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

"""
for move in legalmoves:
    new_board = board
    evaluate_board(new_board)
    returns minimum and maximum evals

evaluate board
highest eval is move

"""


def main():
    board = chess.Board()

    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/fizzy/Downloads/stockfish/stockfish-windows-x86-64-avx2.exe" )

    while not board.is_checkmate():
        if board.is_game_over():
            break
        if board.turn:
            move = generate_random_move(board)
        else:
            # move = engine.play(board, chess.engine.Limit(depth=1, time=1e-10000)).move
            move = generate_random_move(board)
        board.push(move)


    print(board)
    print(board.fullmove_number)
    print(board.outcome())
    print(board.peek())
    print(evaluate_board(board))

if __name__ == "__main__":
    while True:
        main()
        input()
