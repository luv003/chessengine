import chess
import random
from IPython.display import SVG, display
import chess.svg

from engine import SimpleChessEngine
def play_chess():
    board = chess.Board()
    engine = SimpleChessEngine(depth=5)

    while not board.is_game_over():
        display(SVG(chess.svg.board(board, size=400)))
        if board.turn == chess.WHITE:
            player_move = input("Your move (in UCI format, e.g., 'e2e4'): ")
            try:
                move = chess.Move.from_uci(player_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid move format. Try again.")
        else:
            print("Thinking...")
            best_move = engine.get_best_move(board)
            if best_move:
                board.push(best_move)
            else:
                print("No legal moves for Black. Game Over!")
                break

    display(SVG(chess.svg.board(board, size=400)))
    print("Game Over!")
    print("Result:", board.result())

if __name__ == "__main__":
    play_chess()
