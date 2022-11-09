from pong import game
from button import Button
import singlePong
import multiPong
import os
import neat
import pickle
import pygame, sys
pygame.init()
pygame.font.init()


WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # sets window
pygame.display.set_caption("Pong")  # Title for Window

BG = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'mainMenu.png')), (WIDTH, HEIGHT))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)


multiPong.WIN.blit(BG, (0, 0))


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 60))

        single_button = Button(image=pygame.image.load("assets/Single Rect.png"), pos=(350, 150),
                             text_input="SINGLE PLAYER", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        multi_button = Button(image=pygame.image.load("assets/Multi Rect.png"), pos=(350, 280),
                                text_input="MULTIPLAYER", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(350, 410),
                             text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")


        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [single_button, multi_button, quit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.checkForInput(MENU_MOUSE_POS):
                    singlePong.test_ai(config)
                if multi_button.checkForInput(MENU_MOUSE_POS):
                    multiPong.play_multi()
                if quit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

