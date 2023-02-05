from pygame.sprite import Sprite
from random import choice, randint, uniform

from config import FPS, GEM_EMERGE_TIME, GEM_LIFE_TIME, GEM_VALUES


GEM_EMERGE_PROB = 1 / (GEM_EMERGE_TIME * FPS)
GEM_DIE_PROB = 1 / (GEM_LIFE_TIME * FPS)


class Gem(Sprite):

    def __init__(self, screen, images, group):
        Sprite.__init__(self, group)
        self.value, self.image = choice(tuple(zip(GEM_VALUES, images)))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 4
        self.rect.x = randint(0, screen.get_width())
        self.rect.y = randint(0, screen.get_height())

    def update(self):
        if uniform(0, 1) < GEM_DIE_PROB:
            self.kill()

    def emerge(screen, images, group):
        if uniform(0, 1) < GEM_EMERGE_PROB:
            gem = Gem(screen, images, group)
            group.add(gem)
            return gem
        return None
