import argparse
from math import inf
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import chess

from search import get_moves, negamaxalphabeta


class EpicEngine:
    def __init__(self, executor):
        self.active = True
        self.id = "EpicEngine"
        self.author = "the EpicEngine developers (see AUTHORS file)"
        self.debug = True
        self.board = chess.Board()
        # [curr, default, min, max]
        self.options = {
            # "Depth": [3,3,0,0],
        }
        self.executor = executor
        self.go_future = self.executor.submit(lambda: None)
        self.stop_event = Event()

        self.search = negamaxalphabeta
    def go(self, args):
        #movetime
        # (searchmoves=None, ponder=True, 
        
        #  btime=None, wtime=None, winc=None, binc=None, movestogo=None, depth=None, nodes=None, mate=None, movetime=inf)
        #clock() = time
        #setclock() = clock()
        #setclock() -= emt()
        #for searchmoves it needs to push board and depth - 1,
        
        #search
        player = True if self.board.turn == chess.WHITE else False

        # get_moves(self.board, player)
        #eval
        #return info periodically
        # info is depth, seldepth, time, nodes, pv, multipv, score(cp, mate, lowerbound, upperbound, currmove, currmovenumber, hashfull, 
        # nps, tbhits, sbhits, cpuload, string, refutation, currline, )
        #return best_move and ponder
        timeleft = 0
        if args.wtime or args.btime:
            if player:
                timeleft = args.wtime
            else:
                timeleft = args.btime
        
        depth=1
        move = [move for move in self.board.legal_moves][0]
        starttime = perf_counter()
        while not self.stop_event.is_set():
            result = self.search(self, depth, self.board, -inf, inf, player)
            if result:
                move = result[1]
                print(move, depth)
                depth += 1
                timeelapsed = perf_counter() - starttime
                timeleft -= timeelapsed
                if timeleft == 0:
                    self.stop_event.set()
            else:
                if self.debug:
                    print("Search discarded")

        # while in game

        bestmove = "bestmove " + str(move) + " \n"
        
        return bestmove

        #self.board.push(move)

    def is_ready(self) -> bool:
        return self.active

    def set_board(self, fen):
        # resets board
        self.board.set_board_fen(fen)
    
    def parse_error(self, args, e = None):
        msg = f"Error parsing command: {' '.join(args)}"
        if e:
            msg += "\n" + e
        print(msg)

    def parse_cmd(self, args):
        # https://backscattering.de/chess/uci/#whitespace
        # how fast are lookups? would this be faster?
        # first = args[0]

        if self.debug:
            print(f"Parsing: {' '.join(args)}")

        if not args:
            return

        if args[0] == "ping":
            print("pong")

        if args[0] == "uci":
            output = f"id name {self.id}\nid author {self.author}\n"
            for key, value in self.options:
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
        elif args[0] == "isready":
            print("readyok")
        elif args[0] == "setoption":
            # do this: https://backscattering.de/chefdxss/uci/#gui-setoption-name
            if args[1] == "name":
                try:
                    valuei = args.index("value")
                except ValueError as e:
                    # print("Value must be provided.")
                    if self.debug:
                        return self.parse_error(args, e=e)
                # except for no such option
                self.options[args[2:valuei]] = args[valuei + 1:]
        elif args[0] == "ucinewgame":
            self.board.reset()

        elif args[0] == "position":
            try:
                movesi = args.index("moves")
            except ValueError as e:
                movesi = -1
            if movesi != 2:
                mode = args[1]
                if mode == "fen":
                    self.set_board(args[2])
                    return
                elif mode == "startpos":
                    self.board.reset()
                    return
            
            if movesi == 2:
                moves = []
                if args.index("startpos") == 1:
                    self.board.reset()
                for movetoken in args[movesi+1:]:
                    move = chess.Move.from_uci(movetoken)
                    if move in self.board.legal_moves:
                        moves.append(move)
                        self.board.push(move)
                    else:
                        # print("Invalid move")
                        return self.parse_error(args)
                
                # if moves:
                #     for move in moves:
                #         self.board.push(move)
            #return "Error: position [ fen <fenstring> | <startpos> ] moves <move1> ... <movei>"
        elif args[0] == "go":
            options = " ".join(args[1:])
            potential_options = "searchmoves ponder wtime btime winc binc movestogo depth nodes mate movetime infinite".split()
            for pot_opt in potential_options:
                options = options.replace(pot_opt, "--" + pot_opt)
            options = options.split()

            parser = argparse.ArgumentParser(exit_on_error=False)
            parser.add_argument("--searchmoves", dest = "searchmoves", nargs="+")
            parser.add_argument("--ponder", dest = "ponder", default = False,
                                action = "store_true")
            parser.add_argument("--btime", dest = "btime", type = float)
            parser.add_argument("--wtime", dest = "wtime", type = float)
            parser.add_argument("--winc", dest = "winc", type = float)
            parser.add_argument("--binc", dest = "binc", type = float)
            parser.add_argument("--movestogo", dest = "movestogo", type = int)
            parser.add_argument("--depth", dest = "depth", type = int)
            parser.add_argument("--nodes", dest = "nodes",  type = int)
            parser.add_argument("--mate", dest = "mate", type = int)
            parser.add_argument("--movetime", dest = "movetime", nargs = 1, type = float, default = inf)
            parser.add_argument("--infinite", dest = "movetime", action = "store_const", const = inf, default = argparse.SUPPRESS)

            try:
                go_args = parser.parse_args(options)
            except Exception as e:
                return self.parse_error(args, e)
            
            self.stop_event.clear()
            self.go_future = self.executor.submit(self.go, go_args)
        elif args[0] == "stop":
            if self.go_future.running():
                if self.debug:
                    print("Stopping go")
                self.stop_event.set()
                self.go_future.result()
            else:
                if self.debug:
                    print("Go is not running")
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