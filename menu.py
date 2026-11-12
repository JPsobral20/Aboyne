import pygame
import sys
from config import *

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.russo_font_path = "./fonts/RussoOne-Regular.ttf"
        self.viga_font_path = "./fonts/Viga-Regular.ttf"
        pygame.font.init()

    def draw_text_center(self, text, pos, font_size, color, font_path):
        """
        Desenha um texto centralizado na tela.

        @param text: O texto a ser desenhado.
        @param pos: A posição (x, y) do centro do texto.
        @param font_size: O tamanho da fonte do texto.
        @param color: A cor do texto.
        @param font_path: O caminho para o arquivo da fonte a ser usada.
        """
        font = pygame.font.Font(font_path, font_size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, rect)


    def intro_screen(self):
        """
        Exibe a tela de introdução do jogo.

        Esta função é responsável por:
        - Preencher a tela com a cor DARK_BLUE
        - Desenhar o título do jogo "ABOYNE" centralizado na tela, com fonte de tamanho 120 e cor branca
        - Atualizar a tela para exibir o conteúdo
        - Aguardar 2 segundos antes de retornar
        """
        self.screen.fill(DARK_BLUE)
        self.draw_text_center("ABOYNE", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 120, WHITE, self.russo_font_path)
        pygame.display.flip()
        pygame.time.wait(2000)

    def button(self, position, text, button_width=300, button_height=70):
        """
        Desenha um botão na tela com texto centralizado.

        @param position: A posição (x, y) do centro do botão.
        @param text: O texto a ser exibido no botão.
        @param button_width: A largura do botão (padrão é 300 pixels).
        @param button_height: A altura do botão (padrão é 70 pixels).

        @return: True se o mouse estiver sobre o botão, False caso contrário.
        """
        font = pygame.font.Font(self.viga_font_path, 40)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=position)

        rect = pygame.Rect(0, 0, button_width, button_height)
        rect.center = position

        mouse_pos = pygame.mouse.get_pos()
        button_color = TEAL if rect.collidepoint(mouse_pos) else LIGHT_BLUE
        pygame.draw.rect(self.screen, button_color, rect)
        pygame.draw.rect(self.screen, OFF_WHITE, rect, 2, 5)
        self.screen.blit(text_surf, text_rect)

        return rect.collidepoint(mouse_pos)

    def display_options(self, options, start_y):
        """
        Exibe uma lista de opções na tela, com botões clicáveis.

        @param options: Uma lista de tuplas, onde cada tupla contém o texto da opção e uma função associada.
        @param start_y: A coordenada y inicial para a primeira opção.

        @return: O índice da opção selecionada pelo usuário, ou None se nenhuma opção foi selecionada.
        """
        mouse_pos = pygame.mouse.get_pos()
        total_height = len(options) * (70 + 20)
        start_y = (SCREEN_HEIGHT - total_height) // 2

        hovered_index = None
        for i, (text, _) in enumerate(options):
            y_pos = start_y + i * (70 + 20)
            if self.button((SCREEN_WIDTH // 2, y_pos), text):
                hovered_index = i
        return hovered_index


    def run(self):
        self.intro_screen()
        clock = pygame.time.Clock()

        game_mode_options = [("PC vs PC", "pc_vs_pc"), ("Player vs PC", "player_vs_pc"), ("Player vs Player", "player_vs_player")]
        board_size_options = [("Board Size: 4", 4), ("Board Size: 5", 5), ("Board Size: 6", 6)]
        difficulty_options = [("Easy", ("easy", "easy")), ("Medium", ("medium", "medium")), ("Hard", ("hard", "hard")), ("Easy vs Medium", ("easy", "medium")), ("Medium vs Hard", ("medium", "hard")), ("Easy vs Hard", ("easy", "hard"))]

        game_mode = None
        while not game_mode:
            self.screen.fill(DARK_BLUE)
            selected_index = self.display_options(game_mode_options, SCREEN_HEIGHT // 4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and selected_index is not None:
                    game_mode = game_mode_options[selected_index][1]
                    break
            pygame.display.flip()
            clock.tick(30)

        board_size = None
        while not board_size:
            self.screen.fill(DARK_BLUE)
            selected_index = self.display_options(board_size_options, SCREEN_HEIGHT // 4 + 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and selected_index is not None:
                    board_size = board_size_options[selected_index][1]
                    break
            pygame.display.flip()
            clock.tick(30)

        p1difficulty = None
        p2difficulty = None
        while not p1difficulty and not p2difficulty:
            self.screen.fill(DARK_BLUE)
            selected_index = self.display_options(difficulty_options, SCREEN_HEIGHT // 4 + 500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and selected_index is not None:
                    p1difficulty = difficulty_options[selected_index][1][0]
                    p2difficulty = difficulty_options[selected_index][1][1]
                    break
            pygame.display.flip()
            clock.tick(30)

        return game_mode, board_size, p1difficulty, p2difficulty
