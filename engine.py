from chess import Board

class EpicEngine:
    def __init__(self):
        self.active = True
        self.id = "EpicEngine"
        self.authors = "..."
        self.debug = False
        self.board = Board()
        self.state = 0
        # [curr, default, min, max]
        self.options = {
            "a": [1,1,1,1],
        }
    
    def is_ready(self) -> bool:
        return self.active

    def set_board(self, fen):
        # resets board
        self.board.set_board_fen(fen)

    # implement asyncio, per https://backscattering.de/chess/uci/#responsiveness
    def parse_cmd(self, cmd):
        # https://backscattering.de/chess/uci/#whitespace
        tokens = cmd.split()

        # how fast are lookups? would this be faster?
        # first = tokens[0]

        if tokens[0] == "uci":
            output = f"id name {self.id}\nid author {self.authors}\n"
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
            # do this: https://backscattering.de/chess/uci/#gui-setoption-name
            if tokens[1] == "name":
                try:
                    valuei = tokens.index("value")
                except ValueError as e:
                    return "Value must be provided."
                # except for no such option
                self.options[tokens[2:valuei]] = tokens[valuei + 1:]
        elif tokens[0] == "position":
            mode = tokens[1]
            if mode == "fen":
                self.set_board(tokens[2])
            elif mode == "startpos":
                pass
            else:
                pass



if __name__ == "__main__":
    engine = EpicEngine()
    while True:
        cmd = input()
        engine.parse_cmd(cmd)
