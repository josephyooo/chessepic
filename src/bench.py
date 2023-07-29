from time import perf_counter
from math import inf

import chess
import chess.engine

from eval import evaluate_board
from search import negamax, negamaxalphabeta, generate_random_move, user_move


def main():
    board = chess.Board()
    # board.set_board_fen("")

    # engine = chess.engine.SimpleEngine.popen_uci("C:/Users/fizzy/Downloads/t/stockfish/stockfish-windows-x86-64-avx2.exe")

    whitetime = 0
    blacktime = 0
    while not board.is_checkmate():
        # print("-"*10)
        # print(board.fen())
        # print(board)
        start = perf_counter()
        if board.is_game_over():
            break
        if board.turn:
            move = generate_random_move(board)
            whitetime += perf_counter() - start

        else:
            move = negamaxalphabeta(3, board, -inf, inf, False)[1]
            # move = generate_random_move(board)
            # move = negamax(2, board, False)[1]
            blacktime += perf_counter() - start
            # move = engine.play(board, chess.engine.Limit(depth=1, time=1e-10000)).move
        try:
            board.push(move)
        except AttributeError as e:
            print(e, move)

    print(board)
    print(board.fullmove_number)
    print(board.outcome())
    print(board.peek())
    print(evaluate_board(board))
    half_moves = board.fullmove_number // 2
    print(
        f"White time: {whitetime} ({whitetime / half_moves} per move), Black time: {blacktime} ({blacktime / half_moves} per move)"
    )
    # print(f"{blacktime / whitetime}")


if __name__ == "__main__":
    while True:
        main()
        input()
