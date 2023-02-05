from pygame.sprite import Sprite
from random import randint

from config import ACCELERATION, SLOWDOWN, BUMP_RATIO, MAX_SPEED


class Player(Sprite):

    def __init__(self, screen, image):

        Sprite.__init__(self)

        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2

        w, h = screen.get_size()
        self.rect.x = randint(0.1 * w, 0.9 * w)
        self.rect.y = randint(0.1 * h, 0.9 * h)

        self.vx, self.vy = 0, 0
        self.ax, self.ay = 0, 0

    def update(self):

        self.vx *= SLOWDOWN
        if abs(self.vx) < MAX_SPEED:
            self.vx += self.ax
        self.rect.x += self.vx
        if self.rect.left < 0 or self.rect.right > self.screen.get_width():
            self.vx = -BUMP_RATIO * self.vx

        self.vy *= SLOWDOWN
        if abs(self.vy) < MAX_SPEED:
            self.vy += self.ay
        self.rect.y += self.vy
        if self.rect.top < 0 or self.rect.bottom > self.screen.get_height():
            self.vy = -BUMP_RATIO * self.vy

    def control(self, horiz_ctrl, vert_ctrl):
        self.ax, self.ay = ACCELERATION * horiz_ctrl, ACCELERATION * vert_ctrl
