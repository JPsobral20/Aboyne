import pygame
import sys
import time
import math
from game_logic import GameBoard
from board import GameUI
from config import *
from menu import MainMenu

class GameController:
    def __init__(self, screen, game_mode, board_size, p1difficulty='medium', p2difficulty='medium'):
        self.screen = screen
        self.game_mode = game_mode
        self.game_board = GameBoard(board_size=board_size)
        self.game_ui = GameUI(screen, self.game_board)
        self.start_time = pygame.time.get_ticks()
        self.p1difficulty = p1difficulty
        self.p2difficulty = p2difficulty

    def run(self):
        """
        Função principal que executa o jogo.

        Esta função controla o loop principal do jogo, processando eventos do pygame, atualizando o estado do jogo e renderizando a tela.

        Returns:
            None
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_b:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        menu = MainMenu(screen) 
                        game_mode, board_size, p1difficulty, p2difficulty = menu.run() 
                        self.__init__(screen, game_mode, board_size, p1difficulty, p2difficulty)  # Reinitialize GameController with new settings
                        continue
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_mode != 'pc_vs_pc' and self.game_mode != 'player_vs_pc':
                    self.game_ui.handle_mouse_click(event.pos)

                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_mode != 'pc_vs_pc' and self.game_mode != 'player_vs_player':
                    check = self.game_ui.handle_mouse_click(event.pos)
                    if check == 1:
                        self.pc()
                
                

            self.screen.fill(DARK_BLUE)
            self.game_ui.draw_board()
            self.draw_time()

            if self.game_mode == 'pc_vs_pc':
                self.pc()

            winner = self.game_board.check_winner(self.game_board.board_state)  
            if winner:  
                print(f"Winner is Player {winner}")
                pygame.display.flip() 
                time.sleep(5) 
                running = False 

            pygame.display.flip()
            clock.tick(30)

    def pc(self):
        """
        Executa uma partida de jogo entre dois jogadores controlados por computador.

        Esta função é responsável por:
        - Verificar se há um vencedor no estado atual do tabuleiro
        - Encontrar a próxima jogada do jogador atual usando diferentes algoritmos de IA (fácil, médio ou difícil)
        - Mover a peça do jogador atual no tabuleiro
        - Atualizar o jogador atual
        - Desenhar o tabuleiro atualizado na tela
        - Verificar novamente se há um vencedor após a jogada
        - Encerrar o jogo após um vencedor ser determinado
        """
        pygame.time.delay(100)

        if not self.game_board.check_winner(self.game_board.board_state):
            find_piece = self.game_board.find_pieces_playable(self.game_board.board_state, self.game_board.player)
            if not find_piece:
                winner = 3 - self.game_board.player
                print(f"Winner is Player {winner}")
                pygame.time.delay(5000)
                self.quit_game()

            if self.game_board.player == 1:
                if self.p1difficulty == 'easy':
                    best_move = self.game_board.hill_climbing(self.game_board.player, self.game_board.board_state)
                elif self.p1difficulty == 'medium':
                    best_move = self.game_board.minimax_medium(self.game_board.player, self.game_board.board_state, 3, True)  # Adjust the depth as needed
                elif self.p1difficulty == 'hard':
                    best_move = self.game_board.minimax_hard(self.game_board.player, self.game_board.board_state, 3, True)  # Adjust the depth as needed

                if best_move:
                    if self.p1difficulty == 'easy':
                        self.game_board.move_piece(self.game_board.board_state, best_move[0], best_move[1], self.game_board.player)
                    elif self.p1difficulty == 'medium':
                        self.game_board.move_piece(self.game_board.board_state, best_move[0][0], best_move[0][1], self.game_board.player)
                    elif self.p1difficulty == 'hard':
                        self.game_board.move_piece(self.game_board.board_state, best_move[0][0], best_move[0][1], self.game_board.player)

            else:
                if self.p2difficulty == 'easy':
                    best_move = self.game_board.hill_climbing(self.game_board.player, self.game_board.board_state)
                elif self.p2difficulty == 'medium':
                    best_move = self.game_board.minimax_medium(self.game_board.player, self.game_board.board_state, 3, True)  # Adjust the depth as needed
                elif self.p2difficulty == 'hard':
                    best_move = self.game_board.minimax_hard(self.game_board.player, self.game_board.board_state, 3, True)  # Adjust the depth as needed

                if best_move:
                    if self.p2difficulty == 'easy':
                        self.game_board.move_piece(self.game_board.board_state, best_move[0], best_move[1], self.game_board.player)
                    elif self.p2difficulty == 'medium':
                        self.game_board.move_piece(self.game_board.board_state, best_move[0][0], best_move[0][1], self.game_board.player)
                    elif self.p2difficulty == 'hard':
                        self.game_board.move_piece(self.game_board.board_state, best_move[0][0], best_move[0][1], self.game_board.player)
                    

            self.game_board.update_player()
            self.screen.fill(DARK_BLUE)
            self.game_ui.draw_board()
            pygame.display.flip()
            winner = self.game_board.check_winner(self.game_board.board_state)
            if winner:
                print(f"Winner is Player {winner}")
                pygame.time.delay(5000)
                self.quit_game()

    def draw_time(self):
        """
        Desenha o tempo decorrido do jogo na tela.

        Esta função é responsável por:
        - Calcular o tempo decorrido desde o início do jogo
        - Formatar o tempo decorrido em um texto legível (minutos:segundos)
        - Criar uma superfície de texto com a informação do tempo
        - Desenhar a superfície de texto na tela, na posição (10, 10)
        """
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # milliseconds to seconds
        timer_text = f"Time: {elapsed_time // 60}:{elapsed_time % 60:02d}"
        font = pygame.font.Font("./fonts/Viga-Regular.ttf", 36)  
        text_surface = font.render(timer_text, True, WHITE)
        self.screen.blit(text_surface, (10, 10))

    def quit_game(self):
        pygame.quit()
        sys.exit()
