import pygame
from config import *
from menu import MainMenu
from game_controller import GameController

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ABOYNE")

    menu = MainMenu(screen) 
    game_mode, board_size, p1difficulty, p2difficulty = menu.run()  

    if game_mode and board_size and p1difficulty and p2difficulty:
        game_controller = GameController(screen, game_mode, board_size, p1difficulty, p2difficulty)  
        game_controller.run()
    pygame.quit()

if __name__ == "__main__":
    main()
