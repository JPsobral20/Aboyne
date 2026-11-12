import pygame

from math import sin, cos, pi
from game_logic import GameBoard
from config import *


class GameUI:
    def __init__(self, screen, game_board):
        self.screen = screen
        self.game_board = game_board

    def draw_hexagon(self, surface, color, position, size):
        """
        Desenha um hexágono na superfície especificada.

        @param surface: A superfície na qual o hexágono será desenhado.
        @param color: A cor do preenchimento do hexágono.
        @param position: A posição (x, y) do centro do hexágono.
        @param size: O tamanho (raio) do hexágono.
        """
        x, y = position
        hexagon = []
        for i in range(6):
            angle = 2 * pi / 6 * (i + 0.5)
            xi = x + size * cos(angle)
            yi = y + size * sin(angle)
            hexagon.append((xi, yi))
        pygame.draw.polygon(surface, color, hexagon)
        pygame.draw.polygon(surface, OFF_WHITE, hexagon, 5) 
        
    def draw_goal(self, surface, color, position, radius = 7):
        """
        Desenha um círculo representando um objetivo no tabuleiro.

        @param surface: A superfície na qual o objetivo será desenhado.
        @param color: A cor do objetivo.
        @param position: A posição (x, y) do centro do objetivo.
        @param radius: O raio do objetivo (padrão é 7 pixels).
        """
        pygame.draw.circle(surface, color, position, radius)

    def handle_mouse_click(self, mouse_pos):
        """
        Função para lidar com o clique do mouse.

        Esta função é chamada quando o jogador clica no tabuleiro e processa o clique, determinando se uma peça é selecionada,
        movida ou se a jogada é inválida.

        Args:
            mouse_pos (tuple): As coordenadas (x, y) do clique do mouse.

        Returns:
            int: 1 se a jogada for válida e concluída com sucesso, 0 se a jogada for inválida.
        """
        row, col = self.calculate_cell_from_mouse_pos(mouse_pos)
        if row is not None and col is not None:  # Ensure the click is within the board
            if self.game_board.selected_cell is None:
                if self.game_board.board_state[row][col] == self.game_board.player and self.game_board.piece_playable(self.game_board.board_state, [row, col], self.game_board.player):
                    self.game_board.selected_cell = (row, col)
                    print(f"Piece selected: Row {row}, Col {col}")
                else:
                    print("Piece not playable or does not belong to the current player.")
            else:
                # If another piece of the same player is clicked
                if self.game_board.board_state[row][col] == self.game_board.player and self.game_board.piece_playable(self.game_board.board_state, [row, col], self.game_board.player):
                    print(f"Reselected piece: Row {row}, Col {col}")
                    self.game_board.selected_cell = (row, col)
                else:
                    # Second click
                    current_pos = self.game_board.selected_cell
                    if [row, col] in self.game_board.valid_move(self.game_board.player, self.game_board.board_state, current_pos):  
                        if self.game_board.move_piece(self.game_board.board_state, current_pos, [row, col], self.game_board.player):
                            self.game_board.update_player()
                            print(f"Moved piece to: Row {row}, Col {col}")
                            return 1
                        else:
                            print("Invalid move")
                        self.game_board.selected_cell = None  
                    else:
                        print("Invalid move")
        return 0




    def calculate_cell_from_mouse_pos(self, mouse_pos):
        """
        Calcula a célula do tabuleiro correspondente à posição do mouse.

        @param mouse_pos: A posição (x, y) do mouse na tela.

        @return: Uma tupla contendo a linha e a coluna da célula clicada, ou (None, None) se nenhuma célula foi clicada.
        """
        row_height = int(CELL_SIZE * 3 / 4)
        board_height = int(row_height * (self.game_board.board_size * 2 - 1))
        top_margin = (SCREEN_HEIGHT - board_height) // 2

        for row in range(len(self.game_board.board_state)):
            cols = len(self.game_board.board_state[row])
            offset_x = (SCREEN_WIDTH - (cols * CELL_SIZE)) // 2
            y = top_margin + row * row_height

            for col in range(cols):
                x = offset_x + col * CELL_SIZE
                center_x = int(x + CELL_SIZE // 2)
                center_y = int(y + row_height // 2)
                hex_size = CELL_SIZE // 2

                if abs(mouse_pos[0] - center_x) < hex_size and abs(mouse_pos[1] - center_y) < hex_size:
                    return row, col  # Return the row and column of the clicked cell

        return None, None  


    def draw_board(self):
        """
        Desenha o tabuleiro de jogo na tela.

        Esta função é responsável por desenhar todos os elementos do tabuleiro de jogo, incluindo:
        - O fundo escuro da tela
        - A borda branca do quadro da janela
        - As células do tabuleiro, com destaque para a célula selecionada
        - As peças do jogo, incluindo os objetivos
        """
        self.screen.fill(DARK_BLUE)

        window_frame_thickness = 5  
        pygame.draw.rect(self.screen, OFF_WHITE, self.screen.get_rect(), window_frame_thickness)
        
        board_state = self.game_board.board_state
        selected_cell = self.game_board.selected_cell
        board_size = self.game_board.board_size

        row_height = int(CELL_SIZE * 3/4)
        board_height = int(row_height * (board_size * 2 - 1))
        top_margin = (SCREEN_HEIGHT - board_height) // 2
        
        for row in range(len(board_state)):
            cols = len(board_state[row])
            offset_x = (SCREEN_WIDTH - (cols * CELL_SIZE)) // 2
            y = top_margin + row * row_height
            
            for col in range(cols):
                x = offset_x + col * CELL_SIZE
                center_x = int(x + CELL_SIZE // 2)
                center_y = int(y + row_height // 2)
                
                # Fill the hexagon 
                cell_color = CELL_COLOR if selected_cell != (row, col) else HIGHLIGHT_COLOR 
                self.draw_hexagon(self.screen, cell_color, (center_x, center_y), CELL_SIZE / 2)
                
                # Draw the pieces
                piece = board_state[row][col]
                if piece == 1:
                    pygame.draw.circle(self.screen, BLUE, (center_x, center_y), CELL_SIZE // 3.5)
                elif piece == 2:
                    pygame.draw.circle(self.screen, RED, (center_x, center_y), CELL_SIZE // 3.5)
                elif piece in [22, 11]: 
                    self.draw_goal(self.screen, RED if piece == 22 else BLUE, (center_x, center_y))
                