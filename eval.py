def evaluate_board(board):
    fen = board.fen()
    fen = fen.split()[0]
    score = 0
    for piece in fen:
        match piece:
            case "P":
                score += 1
            case "N":
                score += 3
            case "B":
                score += 3
            case "R":
                score += 5
            case "Q":
                score += 9
            case "p":
                score -= 1
            case "n":
                score -= 3
            case "q":
                score -= 9
            case "r":
                score -= 5
            case "b":
                score -= 3
    return score