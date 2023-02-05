import os
import pygame as pg

from config import (
    FPS, WIDTH, HEIGHT, BG_COLOR,
    PLAYER_SIZE, GEM_SIZE, GOBLIN_SIZE,
    IMG_FOLDER, PLAYER_IMG, GOBLIN_IMG, GEM_IMGS,
    INIT_GEMS
)
from player import Player
from gem import Gem
from goblin import Goblin


class Game():

    def __init__(self):

        pg.init()

        pg.display.set_caption("GOBLINS GAME")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE, 32)
        self.clock = pg.time.Clock()

        game_folder = os.path.dirname(__file__)
        img_folder = os.path.join(game_folder, IMG_FOLDER)

        self.sprites = pg.sprite.Group()

        player_img = pg.transform.scale(
            pg.image.load(os.path.join(img_folder, PLAYER_IMG)),
            (PLAYER_SIZE, PLAYER_SIZE)
        )
        player_img.set_colorkey((255, 255, 255))
        self.player = Player(self.screen, player_img)
        self.sprites.add(self.player)

        self.gem_images = [
            pg.transform.scale(
                pg.image.load(os.path.join(img_folder, img_name)),
                (GEM_SIZE, GEM_SIZE)
            )
            for img_name in GEM_IMGS
        ]
        self.gems = pg.sprite.Group()
        for _ in range(INIT_GEMS):
            gem = Gem(self.screen, self.gem_images, self.gems)
            self.sprites.add(gem)

        self.goblin_img = pg.transform.scale(
            pg.image.load(os.path.join(img_folder, GOBLIN_IMG)),
            (GOBLIN_SIZE, GOBLIN_SIZE)
        )
        self.goblins = pg.sprite.Group()

        self.running = False
        self.score = 0
        self.horiz_ctrl, self.vert_ctrl = 0, 0

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            st = (event.type == pg.KEYDOWN) - (event.type == pg.KEYUP)
            if st != 0:
                k = event.key
                self.horiz_ctrl += st * ((k == pg.K_RIGHT) - (k == pg.K_LEFT))
                self.vert_ctrl += st * ((k == pg.K_DOWN) - (k == pg.K_UP))
                self.player.control(self.horiz_ctrl, self.vert_ctrl)

    def emerge_objects(self):
        gem = Gem.emerge(self.screen, self.gem_images, self.gems)
        if gem is not None:
            self.sprites.add(gem)
        goblin = Goblin.emerge(self.screen, self.goblin_img, self.goblins)
        if goblin is not None:
            self.sprites.add(goblin)

    def check_collisions(self):

        collected = pg.sprite.spritecollide(
            self.player, self.gems, True, pg.sprite.collide_circle
        )
        for gem in collected:
            self.score += gem.value

        got_goblin = pg.sprite.spritecollideany(
            self.player, self.goblins, pg.sprite.collide_circle
        )
        if got_goblin:
            self.running = False

    def run(self):
        self.score = 0
        self.running = True
        while self.running:

            self.clock.tick(FPS)
            self.handle_events()

            self.emerge_objects()
            self.check_collisions()

            self.sprites.update()

            self.screen.fill(BG_COLOR)
            self.sprites.draw(self.screen)

            font = pg.font.SysFont(None, 96)
            img = font.render(str(self.score), True, (0, 255, 0))
            self.screen.blit(img, (20, 20))

            pg.display.update()
        return self.display_score()

    def display_score(self):
        self.screen.fill(BG_COLOR)
        font = pg.font.SysFont(None, 128)
        w, h = self.screen.get_size()
        y = (h - 3 * font.get_height()) // 2
        for msg in ("GAME OVER!", f"Score: {self.score}", "Press any key to start a new game"):
            img = font.render(msg, True, (0, 255, 0))
            self.screen.blit(
                img, ((w-img.get_width()) // 2, y)
            )
            y += img.get_height()
        while True:
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return False
                elif event.type == pg.KEYDOWN:
                    return True
