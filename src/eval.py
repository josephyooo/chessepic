from math import inf
import chess

PIECE_TYPES = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

board = chess.Board()
player = board.turn

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

    #score adjusts for certain moves
    #based off of game state
    #endgame = majors and minors less than 6
    
    earlygame = 3
    midgame = 2
    endgame = 1
    
    piecetypes = []
    for square in chess.SquareSet(board.occupied - (board.pawns + board.kings)):
        piece = board.piece_type_at(square)
        piecetypes.append(piece)
    piece_n = len(piecetypes)
    if piece_n > 10:
        gamestate = earlygame
    elif piece_n > 5:
        gamestate = midgame
    else:
        gamestate = endgame
    
    #castling, pushed pawns, knights in center, bishop developed    
    lastmove = board.peek()
    if board.is_castling(lastmove):
        score += (3 * gamestate)
    if board.piece_type_at(lastmove.from_square) == chess.PAWN:
        score += (1/gamestate)
    

    for piece in fen:
        if piece.isalpha():
            score += PIECE_VALUES[piece]
    if board.is_checkmate(): # brilliant !!!
        score += 50000
    return score

def evaluate_game_phase(board):
    pass


