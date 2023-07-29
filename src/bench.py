from time import perf_counter
from math import inf
from concurrent.futures import ThreadPoolExecutor

import chess
import chess.engine

from eval import evaluate_board
from search import negamaxalphabeta, generate_random_move, user_move
from epicengine import EpicEngine

# from ../../chessepic-old/src import EpicEngine as oldEngine



def main():
    board = chess.Board()
    # board.set_board_fen("")
    with ThreadPoolExecutor(max_workers=1) as executor:
        newengine = EpicEngine(executor=executor)
        # oldengine = oldengine()
        from time import sleep

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
                # fen_position = board.fen().split()[0]
                # oldengine.set_board(fen_position)
                # oldengine.board.turn = chess.BLACK

                # move = newengine.go()
                # whitetime += perf_counter() - start

            else:
                fen_position = board.fen().split()[0]
                newengine.set_board(fen_position)
                newengine.board.turn = chess.BLACK

                newengine.parse_cmd("go").split()[-1]
                # move = negamaxalphabeta(3, board, -inf, inf, False)[1]
                
                blacktime += perf_counter() - start
            try:
                board.push(move)
            except (AttributeError, AssertionError) as e:
                print(board)
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
