import pygame
import sys
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
WHITE = (135, 206, 235)  # Sky blue color for white squares
BLACK = (255, 0, 0)      # Red color for black squares
HIGHLIGHT_COLOR = (124, 252, 0, 128)

class ChessPiece:
    def __init__(self, color: str, piece_type: str):
        self.color = color  # 'white' or 'black'
        self.piece_type = piece_type  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
        self.has_moved = False

    def get_valid_moves(self, start_pos: Tuple[int, int], board: List[List[Optional['ChessPiece']]]) -> List[Tuple[int, int]]:
        moves = []
        row, col = start_pos

        if self.piece_type == 'pawn':
            direction = -1 if self.color == 'white' else 1
            # Forward move
            if 0 <= row + direction < BOARD_SIZE and board[row + direction][col] is None:
                moves.append((row + direction, col))
                # Initial two-square move
                if not self.has_moved and 0 <= row + 2 * direction < BOARD_SIZE and board[row + 2 * direction][col] is None:
                    moves.append((row + 2 * direction, col))
            # Captures
            for c in [col - 1, col + 1]:
                if 0 <= c < BOARD_SIZE and 0 <= row + direction < BOARD_SIZE:
                    piece = board[row + direction][c]
                    if piece and piece.color != self.color:
                        moves.append((row + direction, c))

        elif self.piece_type == 'rook':
            # Horizontal and vertical moves
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r, c = r + dr, c + dc

        elif self.piece_type == 'knight':
            for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                r, c = row + dr, col + dc
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] is None or board[r][c].color != self.color:
                        moves.append((r, c))

        elif self.piece_type == 'bishop':
            # Diagonal moves
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r, c = r + dr, c + dc

        elif self.piece_type == 'queen':
            # Combine rook and bishop moves
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                r, c = row + dr, col + dc
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r, c = r + dr, c + dc

        elif self.piece_type == 'king':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                        if board[r][c] is None or board[r][c].color != self.color:
                            moves.append((r, c))

        return moves

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Chess Game")
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.current_player = 'white'
        self.initialize_board()
        self.load_piece_images()

    def load_piece_images(self):
        self.piece_images = {}
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        for piece in pieces:
            for color in colors:
                try:
                    image = pygame.image.load(f'pieces/{color}_{piece}.png')
                    image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                    self.piece_images[f'{color}_{piece}'] = image
                except:
                    # If images are not available, we'll use text representation
                    pass

    def initialize_board(self):
        # Set up pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = ChessPiece('black', 'pawn')
            self.board[6][col] = ChessPiece('white', 'pawn')

        # Set up other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(BOARD_SIZE):
            self.board[0][col] = ChessPiece('black', piece_order[col])
            self.board[7][col] = ChessPiece('white', piece_order[col])

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board[row][col]
                if piece:
                    if hasattr(self, 'piece_images') and f'{piece.color}_{piece.piece_type}' in self.piece_images:
                        self.screen.blit(self.piece_images[f'{piece.color}_{piece.piece_type}'],
                                       (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    else:
                        # Fallback to text representation if images are not available
                        font = pygame.font.Font(None, 36)
                        text = piece.piece_type[0].upper()
                        if piece.color == 'black':
                            text = text.lower()
                        text_surface = font.render(text, True, (0, 0, 0) if piece.color == 'white' else (255, 255, 255))
                        text_rect = text_surface.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE//2,
                                                                row * SQUARE_SIZE + SQUARE_SIZE//2))
                        self.screen.blit(text_surface, text_rect)

        # Highlight selected piece and valid moves
        if self.selected_piece:
            row, col = self.selected_piece
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR,
                           (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            piece = self.board[row][col]
            if piece:
                valid_moves = piece.get_valid_moves((row, col), self.board)
                for move_row, move_col in valid_moves:
                    pygame.draw.circle(self.screen, HIGHLIGHT_COLOR,
                                     (move_col * SQUARE_SIZE + SQUARE_SIZE//2,
                                      move_row * SQUARE_SIZE + SQUARE_SIZE//2),
                                     SQUARE_SIZE//4)

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return

        if self.selected_piece:
            # If a piece is already selected, try to move it
            start_row, start_col = self.selected_piece
            piece = self.board[start_row][start_col]
            
            if piece and (row, col) in piece.get_valid_moves((start_row, start_col), self.board):
                # Move the piece
                self.board[row][col] = piece
                self.board[start_row][start_col] = None
                piece.has_moved = True
                self.current_player = 'black' if self.current_player == 'white' else 'white'
            
            self.selected_piece = None
        else:
            # Select a piece if it belongs to the current player
            piece = self.board[row][col]
            if piece and piece.color == self.current_player:
                self.selected_piece = (row, col)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_click(event.pos)

            self.draw_board()
            pygame.display.flip()

if __name__ == '__main__':
    game = ChessGame()
    game.run() 