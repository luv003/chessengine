import chess
import chess.svg
import chess.engine
import random
from IPython.display import SVG, display


class SimpleChessEngine:
    def __init__(self, depth=3):
        self.depth = depth

    def get_best_move(self, board):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_move = random.choice(legal_moves)
        max_eval = -float('inf')

        for move in legal_moves:
            board.push(move)
            eval_score = self.alpha_beta(board, self.depth - 1, -float('inf'), float('inf'), False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

        return best_move

    def alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board):
        material_score = sum(self.get_material_value(piece) for piece in board.piece_map().values())

        positional_score = sum(self.get_positional_value(piece, square) for square, piece in board.piece_map().items())

        return material_score + positional_score

    def get_material_value(self, piece):
        material_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        return material_values.get(piece.piece_type, 0)

    def get_positional_value(self, piece, square):
        positional_values = {
    chess.PAWN: [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10,-20,-20, 10, 10,  5,
        5, -5,-10,  0,  0,-10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ],
    chess.ROOK: [
        0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        5, 10, 10, 10, 10, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0,
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20,
    ],
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]        }
        return positional_values.get(piece.piece_type, [0] * 64)[square]

def play_chess():
    board = chess.Board()
    engine = SimpleChessEngine(depth=3)

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
