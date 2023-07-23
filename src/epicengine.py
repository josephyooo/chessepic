import asyncio
import argparse
from math import inf

import chess

from search import get_moves, negamaxalphabeta


class EpicEngine:
    def __init__(self):
        self.active = True
        self.id = "EpicEngine"
        self.author = "the EpicEngine developers (see AUTHORS file)"
        self.debug = False
        self.board = chess.Board()
        self.state = 0
        # [curr, default, min, max]
        self.options = {
            # "Depth": [3,3,0,0],
        }
        #              keep searching?, bestmove
        self.best_move = 0
        self.tasks = {}
    async def go(self, args):
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

        # move_finder = asyncio.create_task(self.increasing_depth_search(player))
        # self.tasks.add(move_finder)
        # self.best_move = 0
        try:
            depth = 1
            while True:
                print(depth, self.best_move)
                self.best_move = negamaxalphabeta(depth, self.board, -inf, inf, player)[1]
                depth += 1
        except asyncio.CancelledError:
            print("cancelled")
            bestmove = "bestmove " + str(self.best_move) + " \n"
            
            self.best_move = bestmove
            return bestmove

        #self.board.push(move)
    
    # async def increasing_depth_search(self, player):
    #     depth = 1
    #     while True:
    #         print(depth, self.best_move)
    #         self.best_move = negamaxalphabeta(depth, self.board, -inf, inf, player)[1]
    #         depth += 1


    def stop(self):
        self.tasks.get(0).cancel()

    def is_ready(self) -> bool:
        return self.active

    def set_board(self, fen):
        # resets board
        self.board.set_board_fen(fen)

    # implement asyncio, per https://backscattering.de/chess/uci/#responsiveness
    async def parse_cmd(self, cmd):
        # https://backscattering.de/chess/uci/#whitespace
        tokens = cmd.split()

        # how fast are lookups? would this be faster?
        # first = tokens[0]

        if not tokens:
            return

        if tokens[0] == "t":
            print("started")
            await asyncio.sleep(2)
            print("done")

        if tokens[0] == "uci":
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

            return output
        elif tokens[0] == "isready":
            return "readyok"
        elif tokens[0] == "setoption":
            # do this: https://backscattering.de/chefdxss/uci/#gui-setoption-name
            if tokens[1] == "name":
                try:
                    valuei = tokens.index("value")
                except ValueError as e:
                    return "Value must be provided."
                # except for no such option
                self.options[tokens[2:valuei]] = tokens[valuei + 1:]
        elif tokens[0] == "ucinewgame":
            self.board.reset()
            return "got it"

        elif tokens[0] == "position":
            try:
                movesi = tokens.index("moves")
            except ValueError as e:
                movesi = -1
            if movesi != 2:
                mode = tokens[1]
                if mode == "fen":
                    self.set_board(tokens[2])
                    return
                elif mode == "startpos":
                    self.board.reset()
                    return
            
            if movesi == 2:
                moves = []
                if tokens.index("startpos") == 1:
                    self.board.reset()
                for movetoken in tokens[movesi+1:]:
                    move = chess.Move.from_uci(movetoken)
                    if move in self.board.legal_moves:
                        moves.append(move)
                        self.board.push(move)
                    else:
                        return "Invalid move"
                
                # if moves:
                #     for move in moves:
                #         self.board.push(move)
            #return "Error: position [ fen <fenstring> | <startpos> ] moves <move1> ... <movei>"
        elif tokens[0] == "go":
            options = " ".join(tokens[1:])
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
                args = parser.parse_args(options)
            except:
                return
            return await self.go(args)
        elif tokens[0] == "stop":
            self.stop()
            return
                
            
            


            
async def main():
    engine = EpicEngine()
    while True:
        cmd = input()
        # cmd = "go infinite"
        result = await engine.parse_cmd(cmd)
        print(result)
    

if __name__ == "__main__":
    asyncio.run(main())