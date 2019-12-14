"""Game objects and physics"""
import pygame


# Здесь будут функции игровой физики


class Entity(pygame.sprite.Sprite):
    def __init__(self, images, groups):
        super().__init__(*groups)
        self.current_image = 0
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def animate(self):
        pos = self.rect.x, self.rect.y
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def set_x(self, x):
        self.rect.x = x

    def set_y(self, y):
        self.rect.y = y


class LivingCreature(Entity):
    def __init__(self, groups, images, weapon, speed):
        super().__init__(groups, images)
        self.speed = speed
        self.weapon = weapon

    def set_weapon(self, weapon):
        self.weapon = weapon


class Player(LivingCreature):
    def __init__(self, groups, images, weapon, speed, jump_speed):
        super().__init__(groups, images, weapon, speed)
        self.jump_speed = jump_speed


class Enemy(LivingCreature):
    pass


class Thing(Entity):
    pass


class Weapon(Thing):
    pass


class Supply(Thing):
    pass
