# Aboyne

A Python implementation of the **Aboyne strategy board game**, developed with Pygame. The project combines a graphical game interface, turn-based gameplay, and artificial intelligence algorithms, allowing players to compete against each other or against computer-controlled opponents.

## Features

- **Multiple game modes**
  - Player vs Player
  - Player vs Computer
  - Computer vs Computer
- **Configurable board sizes:** 4, 5, and 6.
- **AI difficulty levels:** Easy, Medium, and Hard.
- **Artificial intelligence algorithms:**
  - Hill Climbing
  - Minimax
- **Interactive graphical interface** built with Pygame.
- **Move validation** and playable-piece selection.
- **Game timer** to track elapsed playing time.
- **Custom graphics and typography** using dedicated fonts.

## Screenshots

*Screenshots can be added here to showcase the main menu and gameplay.*

## Technologies

- **Python** – Core programming language.
- **Pygame** – Graphics, user input, and game interface.
- **NumPy** – Numerical computing dependency.

## Project Structure

```text
Aboyne/
├── fonts/
│   ├── RussoOne-Regular.ttf
│   └── Viga-Regular.ttf
├── board.py              # Board rendering and mouse interaction
├── config.py             # Screen dimensions, colours, and settings
├── game_controller.py    # Game loop and AI turn management
├── game_logic.py         # Board state, rules, and AI algorithms
├── main.py               # Application entry point
├── menu.py               # Main menu and game configuration
├── description.txt       # Game representation and problem description
└── README.md
```

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JPsobral20/Aboyne.git
   cd Aboyne
   ```

2. Install the required dependencies:

   ```bash
   pip install pygame numpy
   ```

### Running the Game

Start the application with:

```bash
python main.py
```

The main menu allows you to select the game mode, board size, and AI difficulty configuration.

## Artificial Intelligence

The project implements different approaches to computer-controlled gameplay:

| Difficulty | Algorithm | Description |
|---|---|---|
| Easy | Hill Climbing | Selects moves using a heuristic-based search approach. |
| Medium | Minimax | Evaluates possible moves using adversarial search. |
| Hard | Minimax | Uses the Minimax algorithm for more advanced move evaluation. |

The AI evaluates board configurations and searches for moves that improve its position towards the game's objective.

## Game Configuration

Players can choose between three board sizes:

- 4
- 5
- 6

The game supports human and computer-controlled players, with configurable AI difficulty combinations.

## Academic Context

This project was developed as part of an academic assignment at the **Faculty of Engineering of the University of Porto (FEUP)**, exploring artificial intelligence concepts through the implementation of a strategy board game.

---

Developed using Python and Pygame.
