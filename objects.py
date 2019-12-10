"""Game objects and physics"""
import pygame


# Здесь будут функции игровой физики


class Entity:
    pass


class LivingCreature(Entity):
    pass


class Player(LivingCreature):
    pass


class Enemy(LivingCreature):
    pass


class Platform(Entity):
    pass


class Barrier(Entity):
    pass


class Background(Entity):
    pass


class Ladder(Entity):
    pass


class Button(Entity):
    pass


class Thing(Entity):
    pass


class Weapon(Thing):
    pass


class Supply(Thing):
    pass
