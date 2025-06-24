# Python Chess Game

A simple chess game implemented in Python using Pygame.

## Features

- Complete chess rules implementation
- Graphical user interface
- Valid move highlighting
- Turn-based gameplay
- Support for all chess pieces with proper movement rules

## Requirements

- Python 3.x
- Pygame 2.5.2

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python chess_game.py
```

2. Game Rules:
- White pieces move first
- Click on a piece to select it
- Valid moves will be highlighted
- Click on a highlighted square to move the selected piece
- Players take turns moving their pieces
- The game follows standard chess rules

## Controls

- Left mouse button: Select and move pieces
- Close window to exit the game

## Note

The game will use text representation for pieces if chess piece images are not available. To use custom piece images, create a `pieces` directory and add PNG images with the following naming convention:
- `white_pawn.png`
- `white_rook.png`
- `white_knight.png`
- `white_bishop.png`
- `white_queen.png`
- `white_king.png`
- `black_pawn.png`
- `black_rook.png`
- `black_knight.png`
- `black_bishop.png`
- `black_queen.png`
- `black_king.png` 