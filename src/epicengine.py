import argparse
from math import inf
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import sys

import chess

from search import get_moves, negamaxalphabeta


class EpicEngine:
    def __init__(self, executor):
        self.active = True
        self.id = "EpicEngine"
        self.author = "the EpicEngine developers (see AUTHORS file)"
        self.debug = False
        self.board = chess.Board()
        # [curr, default, min, max]
        self.options = {
            # "Depth": [10, 5, 0, 0],
        }
        self.executor = executor
        self.go_future = self.executor.submit(lambda: None)
        self.stop_event = Event()
        self.nodes = 0

        self.search = negamaxalphabeta

    def go(self, args):
        player = True if self.board.turn == chess.WHITE else False

        # get_moves(self.board, player)
        # eval
        # return info periodically
        # info is depth, seldepth, time, nodes, pv, multipv, score(cp, mate, lowerbound, upperbound, currmove, currmovenumber, hashfull,
        # nps, tbhits, sbhits, cpuload, string, refutation, currline, )
        # return best_move and ponder
        # timeleft = 0
        # if args.wtime or args.btime:
        #     if player:
        #         timeleft = args.wtime
        #     else:
        #         timeleft = args.btime

        # depth = 1
        move = [move for move in self.board.legal_moves][0]
        # while not self.stop_event.is_set():
        # starttime = perf_counter()
        self.nodes = 0
        result = self.search(self, 3, self.board, -inf, inf, player, False)
        # timeelapsed = perf_counter() - starttime
        # timeleft -= timeelapsed
        # if timeleft == 0 or depth == self.options["Depth"][0]:
        #     self.stop_event.set()
        if result:
            move = result[1]
            # if self.debug:
            #     print(move, depth, self.nodes, self.nodes / timeelapsed)
            # depth += 1
        else:
            if self.debug:
                print("Search discarded")

        bestmove = "bestmove " + str(move) + " \n"

        print(bestmove)

    def is_ready(self) -> bool:
        return self.active

    def set_board(self, fen):
        self.board.set_board_fen(fen)

    def parse_error(self, args, e=None):
        msg = f"Error parsing command: {' '.join(args)}"
        if e:
            msg += "\n" + e
        print(msg)

    def parse_cmd(self, args):
        # how fast are lookups? would this be faster?

        if self.debug:
            print(f"Parsing: {' '.join(args)}")
            if args[0] == "ping":
                print("pong")

        if not args:
            return

        start_i = -1
        for i in range(len(args)):
            if (
                args[i]
                in "uci isready setoption ucinewgame debug position go stop quit".split()
            ):
                start_i = i
                break

        if args[start_i] == "uci":
            output = f"id name {self.id}\nid author {self.author}\n"
            for key, value in self.options.items():
                curr, default, min, max = value
                output += f"option name {key} type {default.__class__.__name__} default"
                if default:
                    output += f" {default}"
                else:
                    output += " <empty>"
                if min:
                    output += f" min {min}"
                if max:
                    output += f" max {max}"
                output += "\n"

            output += "uciok\n"

            print(output)
        elif args[start_i] == "isready":
            print("readyok")
        elif args[start_i] == "setoption":
            if args[1] == "name":
                try:
                    valuei = args.index("value")
                except ValueError as e:
                    if self.debug:
                        return self.parse_error(args, e=e)
                self.options[args[start_i + 2 : valuei]] = args[valuei + 1 :]
        elif args[start_i] == "ucinewgame":
            self.board.reset()
        elif args[start_i] == "debug":
            if args[1] == "on":
                self.debug = True
            elif args[1] == "off":
                self.debug = False

        elif args[start_i] == "position":
            try:
                movesi = args.index("moves")
            except ValueError as e:
                movesi = -1
            if movesi != start_i + 2:
                mode = args[1]
                if mode == "fen":
                    self.set_board(args[start_i + 2])
                    return
                elif mode == "startpos":
                    self.board.reset()
                    return

            if movesi == start_i + 2:
                moves = []
                if args.index("startpos") == start_i + 1:
                    self.board.reset()
                for movetoken in args[movesi + 1 :]:
                    move = chess.Move.from_uci(movetoken)
                    if move in self.board.legal_moves:
                        moves.append(move)
                        self.board.push(move)
                    else:
                        return self.parse_error(args)

        elif args[start_i] == "go":
            options = " ".join(args[start_i + 1 :])
            potential_options = "searchmoves ponder wtime btime winc binc movestogo depth nodes mate movetime infinite".split()
            for pot_opt in potential_options:
                options = options.replace(pot_opt, "--" + pot_opt)
            options = options.split()

            parser = argparse.ArgumentParser(exit_on_error=False)
            parser.add_argument("--searchmoves", dest="searchmoves", nargs="+")
            parser.add_argument(
                "--ponder", dest="ponder", default=False, action="store_true"
            )
            parser.add_argument("--btime", dest="btime", type=float)
            parser.add_argument("--wtime", dest="wtime", type=float)
            parser.add_argument("--winc", dest="winc", type=float)
            parser.add_argument("--binc", dest="binc", type=float)
            parser.add_argument("--movestogo", dest="movestogo", type=int)
            parser.add_argument("--depth", dest="depth", type=int)
            parser.add_argument("--nodes", dest="nodes", type=int)
            parser.add_argument("--mate", dest="mate", type=int)
            parser.add_argument(
                "--movetime", dest="movetime", nargs=1, type=float, default=inf
            )
            parser.add_argument(
                "--infinite",
                dest="movetime",
                action="store_const",
                const=inf,
                default=argparse.SUPPRESS,
            )

            try:
                go_args = parser.parse_args(options)
            except Exception as e:
                return self.parse_error(args, e)
            if self.debug:
                print(go_args)

            self.stop_event.clear()
            self.go_future = self.executor.submit(self.go, go_args)
        elif args[start_i] == "stop":
            if self.go_future.running():
                if self.debug:
                    print("Stopping go")
                self.stop_event.set()
                self.go_future.result()
            else:
                if self.debug:
                    print("Go is not running")
        elif args[start_i] == "quit":
            sys.exit(0)
        else:
            return self.parse_error(args)


def main():
    with ThreadPoolExecutor(max_workers=1) as executor:
        engine = EpicEngine(executor)
        while True:
            args = input().split()
            engine.parse_cmd(args)


if __name__ == "__main__":
    main()
