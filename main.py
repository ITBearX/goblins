import pygame as pg
from game import Game


if __name__ == '__main__':
    playing = True
    while playing:
        the_game = Game()
        playing = the_game.run()
    pg.quit()
