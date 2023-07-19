lul
for move in legalmoves:
    new_board = board
    evaluate_board(new_board)
    returns minimum and maximum evals
    optimize search for attacks captures and checks

evaluate board
highest eval is move
evaluation algorithm
- positions have score
    heat map to determine where
    early to mid to late game can be determined by number of pieces left


# Order of business
## efficiency
      - ### choose order of moves to run through
          - [ ] by human thinking (dont move piece into danger)
      - ### search depths sequentially
          - [ ] **keep best moves to search first in later depths**
## improve ability to evaluate moves
- [x] checkmate is infinity evaluation
- [x] add ability to see checkmate in two
- [ ] heat map
- [ ] endgame vs middle vs early game eval
## opening/endgame database
## uci compatiblity
## arena chess gui