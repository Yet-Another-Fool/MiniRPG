import pygame
from game.game import Game

def main():
    pygame.init()

    game = Game()
    game.loop()

    pygame.quit()

if __name__ == '__main__': # not very useful since we dont import 'main' but it's fancy and i like it :)
    main()
