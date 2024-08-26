from pygame.sprite import Sprite
from random import randint, choice, uniform

from config import FPS, GOBLIN_EMERGE_TIME, GOBLIN_MAX_SPEED


GOBLIN_EMERGE_PROB = 1 / (GOBLIN_EMERGE_TIME * FPS)


class Goblin(Sprite):

    def __init__(self, screen, image, group):
        Sprite.__init__(self)

        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2

        w, h = screen.get_size()
        if randint(0, 1) == 1:
            self.rect.x = randint(0, w)
            self.rect.y = randint(0, 1) * h
        else:
            self.rect.y = randint(0, h)
            self.rect.x = randint(0, 1) * w

        min_speed = GOBLIN_MAX_SPEED / 2
        vx = uniform(min_speed, GOBLIN_MAX_SPEED)
        vy = uniform(min_speed, GOBLIN_MAX_SPEED)
        self.vx = choice((vx, -vx))
        self.vy = choice((vy, -vy))

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left < 0 or self.rect.right > self.screen.get_width():
            self.kill()
        if self.rect.top < 0 or self.rect.bottom > self.screen.get_height():
            self.kill()

    def emerge(screen, image, group):
        if uniform(0, 1) < GOBLIN_EMERGE_PROB:
            goblin = Goblin(screen, image, group)
            group.add(goblin)
            return goblin
        return None
