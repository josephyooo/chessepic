from math import inf

PIECE_VALUES = {
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 100,
    "p": -1,
    "n": -3,
    "b": -3,
    "r": -5,
    "q": -9,
    "k": -100,
}


def evaluate_board(board):
    fen = board.fen()
    fen = fen.split()[0]
    score = 0
    for piece in fen:
        if piece.isalpha():
            score += PIECE_VALUES[piece]
    if board.is_checkmate(): # brilliant !!!
        score += inf
    return score

def evaluate_game_phase(board):
    pass