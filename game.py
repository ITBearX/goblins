import os
import pygame as pg

from config import (
    FPS, WIDTH, HEIGHT, BG_COLOR,
    IMG_FOLDER, OBJ_SIZE,
    PLAYER_IMG, GOBLIN_IMG, GOLD_IMG
)
from player import Player


class Game():

    def __init__(self):

        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE, 32)
        self.clock = pg.time.Clock()

        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, IMG_FOLDER)

        self.sprites = pg.sprite.Group()
        player_img = pg.transform.scale(
            pg.image.load(os.path.join(img_folder, PLAYER_IMG)),
            (OBJ_SIZE, OBJ_SIZE)
        )
        player_img.set_colorkey((255, 255, 255))
        self.player = Player(self.screen, player_img)
        self.sprites.add(self.player)

        self.horiz_ctrl, self.vert_ctrl = 0, 0

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            st = (event.type == pg.KEYDOWN) - (event.type == pg.KEYUP)
            if st != 0:
                k = event.key
                self.horiz_ctrl += st * ((k == pg.K_RIGHT) - (k == pg.K_LEFT))
                self.vert_ctrl += st * ((k == pg.K_DOWN) - (k == pg.K_UP))
                self.player.control(self.horiz_ctrl, self.vert_ctrl)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.handle_events()
            self.sprites.update()
            self.screen.fill(BG_COLOR)
            self.sprites.draw(self.screen)
            pg.display.update()
