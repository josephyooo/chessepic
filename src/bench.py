from time import perf_counter
from math import inf
import asyncio

import chess
import chess.engine

from eval import evaluate_board
from search import negamax, negamaxalphabeta, generate_random_move, user_move
from epicengine import EpicEngine



async def main():
    board = chess.Board()
    # board.set_board_fen("")

    engine = EpicEngine()
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

            whitetime += perf_counter() - start
            
        else:
            fen_position = board.fen().split()[0]
            engine.set_board(fen_position)
            engine.board.turn = chess.BLACK
            # task = asyncio.create_task(engine.go(0))
            task = asyncio.ensure_future(engine.go(0))
            print(1)
            sleep(1)
            task.cancel()
            print(2)
            # try:
            # except asyncio.CancelledError:
            #     print(3)
            #     print(task.cancelled())
            # engine.stop()
                # move = engine.best_move

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
    print(f"White time: {whitetime} ({whitetime / half_moves} per move), Black time: {blacktime} ({blacktime / half_moves} per move)")
    # print(f"{blacktime / whitetime}")

if __name__ == "__main__":
    while True:
        asyncio.run(main())
        input()
