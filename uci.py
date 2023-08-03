import engine
import chess
import random
import numpy


board=chess.Board()
engine=SimpleChessEngine()

while True:
  msg=sys.stdin.readline().strip()
  if msg=='uci':
    print('uciok')
  elif msf=='isready':
    print('readyok')
  elif msg.startswith('position'):
    moves=msg.split(' ')[1:]
    if moves[0]=='startpos':
      engine.board.set_fen(chess.STARTING_FEN)
      moves=moves[2:]
    elif moves[0]=='fen':
      engine.board.set_fen(' '.join(moeves[1:7]))
      moves=moves[8:]
    for move in moves:
      engine.board.push_san(move)
  elif msg.startswith('go'):
    best_move=engine.get_best_move()
    print(f'bestmove{best_move}')
  sys.stdout.flush()
  
    
