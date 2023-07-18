from time import perf_counter
from math import inf

import chess
import chess.engine

from eval import evaluate_board
from search import negamax, negamaxalphabeta, generate_random_move



def main():
    board = chess.Board()

    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/fizzy/Downloads/t/stockfish/stockfish-windows-x86-64-avx2.exe")


    whitetime = 0
    blacktime = 0
    while not board.is_checkmate():
        start = perf_counter()
        if board.is_game_over():
            break
        if board.turn:
            move = negamaxalphabeta(4, board, -inf, inf, True)[1]
            whitetime += perf_counter() - start
        else:
            move = generate_random_move(board)
            # move = negamax(2, board, False)[1]
            blacktime += perf_counter() - start
            # move = engine.play(board, chess.engine.Limit(depth=1, time=1e-10000)).move
        board.push(move)


    print(board)
    print(board.fullmove_number)
    print(board.outcome())
    print(board.peek())
    print(evaluate_board(board))
    print(f"White time: {whitetime}, Black time: {blacktime}")
    print(f"{blacktime / whitetime}")

if __name__ == "__main__":
    while True:
        main()
        input()
