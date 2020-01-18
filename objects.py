"""Игровые объекты и их взаимодействие"""

import os
import pygame
from vectors import symmetry12

GRAVITY = 0.5  # px/frame^2


def load_image(filename):
    return pygame.image.load(os.path.join('img', filename))


def lines_collide(line1, line2) -> bool:
    """
    Автор: Михаил Грибушенков
    cool collision-testing function without dividing. So pretty and nice.
    """
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    # line1 or line2 = (x1, y1, x2, y2),
    # where (x1, y1) and (x2, y2) -  vertex coordinates

    ac = x3 - x1, y3 - y1
    ad = x4 - x1, y4 - y1
    ab = x2 - x1, y2 - y1
    # vector multiplication - only z component
    z1 = ab[0] * ac[1] - ab[1] * ac[0]
    z2 = ab[0] * ad[1] - ab[1] * ad[0]
    if z1 * z2 > 0:
        return False

    dc = x3 - x4, y3 - y4
    da = x1 - x4, y1 - y4
    db = x2 - x4, y2 - y4
    # second vector product
    z3 = dc[0] * da[1] - dc[1] * da[0]
    z4 = dc[0] * db[1] - dc[1] * db[0]
    if z3 * z4 > 0:
        return False
    return True


def blit_mask(source, dest, destpos, mask, maskrect):
    """
    Blit an source image to the dest surface, at destpos, with a mask, using
    only the maskrect part of the mask.
    """
    tmp = source.copy()
    tmp.blit(mask, maskrect.topleft, maskrect,
             special_flags=pygame.BLEND_RGBA_MULT)
    dest.blit(tmp, destpos, dest.get_rect().clip(maskrect))


def sin_from_line(line):
    """
    Синус угла наклона линии относительно горизонта для эффекта сложности
    подъёма
    """
    x1, y1, x2, y2 = line
    return abs((y2 - y1) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, image, absolute: bool, game):
        super().__init__(*groups)
        self.image = image
        self.image.set_colorkey((0, 0, 0))  # Для использования маски
        self.mask = pygame.mask.from_surface(self.image)

        # Содержит координаты относительно окна,
        # которые считаются автоматически в методе update
        self.rect = self.image.get_rect()

        # Координаты относительно игровой карты
        self.x = 0
        self.y = 0

        self.absolute = absolute
        self.game = game

    def sync_pos(self):
        if self.absolute:
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.rect.x = self.x - self.game.camera.x
            self.rect.y = self.y - self.game.camera.y

    def move(self, x, y):
        self.x += x
        self.y += y
        self.sync_pos()

    def set_x(self, x):
        self.x = x
        self.sync_pos()

    def set_y(self, y):
        self.y = y
        self.sync_pos()

    def get_surface_lines(self):
        return (
            (self.x, self.y, self.x + self.rect.width, self.y),
            (self.x + self.rect.width, self.y,
             self.x + self.rect.width, self.y + self.rect.height),
            (self.x + self.rect.width, self.y + self.rect.height,
             self.x, self.y + self.rect.height),
            (self.x, self.y, self.x, self.y + self.rect.height),

        )

    def update(self, *args):
        self.sync_pos()


class Polygon(Entity):
    def __init__(self, groups, game, points,
                 absolute: bool = False, image=None):
        self.points = points + (points[0], )
        canvas = pygame.Surface((max([i[0] for i in points]),
                                 max([i[1] for i in points])))
        pygame.draw.polygon(canvas, (0, 255, 0), points)
        super().__init__(groups, canvas, absolute, game)
        if image:
            blit_mask(image, self.image, (0, 0), self.mask, self.rect)

    def get_surface_lines(self):
        return (
            (self.points[i][0] + self.x, self.points[i][1] + self.y,
             self.points[i + 1][0] + self.x, self.points[i + 1][1] + self.y)
            for i in range(len(self.points) - 1)
        )


class Thing(Entity):
    def __init__(self, groups, image, absolute, game, picked_up):
        super().__init__(groups, image, absolute, game)
        self.picked_up = picked_up

    def use(self):
        pass


class Weapon(Thing):
    def __init__(self, groups, image, absolute, game,
                 picked_up, speed, damage, radius):
        super().__init__(groups, image, absolute, game, picked_up)
        self.speed = speed
        self.damage = damage
        self.radius = radius


class Bullet(Entity):
    def __init__(self, groups, game, speed, radius):
        self.radius = radius
        self.speed = speed
        image = pygame.Surface((2 * radius, 2 * radius))
        pygame.draw.circle(image, (254, 254, 255), (radius, radius), radius)
        super().__init__(groups, image, False, game)

    def update(self, *args):
        x, y = self.x, self.y
        line = (x, y, x + self.speed[0], y + self.speed[1])
        collided = False
        for obj in self.game.all_sprites:
            obj_lines = obj.get_surface_lines()
            for obj_line in obj_lines:
                if lines_collide(obj_line, line):
                    vec = (obj_line[2] - obj_line[0],
                           obj_line[3] - obj_line[1])
                    collided = True
                    break
            if collided:
                break
        if collided:
            self.speed = symmetry12(self.speed, vec)
        self.move(*self.speed)



class Supply(Thing):
    def __init__(self, groups, image, absolute, game, picked_up, thing_type):
        super().__init__(groups, image, absolute, game, picked_up)
        self.type = thing_type


class Inventory(Entity):
    def __init__(self, groups, game, max_len, cell_size):
        image = pygame.Surface((max_len * cell_size, cell_size))
        for i in range(max_len):
            pygame.draw.rect(image, (255, 255, 255),
                             (i * cell_size, 0,
                              (i + 1) * cell_size, cell_size))
        super().__init__(groups, image, True, game)
        self.max_len = max_len
        self.cell_size = cell_size


class LivingCreature(Entity):
    def __init__(self, groups, image, game, max_speed, health):
        super().__init__(groups, image, False, game)

        # directions
        self.RIGHT = 1
        self.LEFT = -1

        # object types
        self.BARRIER = 0
        self.PLATFORM = 1
        self.LADDER = 2
        self.BUTTON = 3

        self.max_speed = max_speed
        self.health = health
        self.speed = [0, 0]
        self.acceleration = max_speed / 5

        # flags
        self.stands = False
        self.moves = False
        self.direction = self.RIGHT
        # Проваливаться сквозь платформы
        self.ignore_platforms = False
        # Было ли столкновение на предыдущем кадре
        self.prev_frame_collision = False

        self.animated = None
        self.images = self.parse_image(image)
        self.current_image = 0
        self.image = self.images[0][self.current_image]

    def add_health(self, value):
        self.health += value
        if self.health:
            return True

    def set_health(self, value):
        self.health = value
        if self.health:
            return True

    def move_left(self):
        self.speed[0] -= self.acceleration
        if self.speed[0] < -self.max_speed:
            self.speed[0] = -self.max_speed

    def move_right(self):
        self.speed[0] += self.acceleration
        if self.speed[0] > self.max_speed:
            self.speed[0] = self.max_speed

    def refresh_image(self):
        super().update()
        if self.animated:
            pass

    def parse_image(self, image):
        if isinstance(image, pygame.Surface):
            self.animated = False
            return [[image]]
        # Example: 'player_6x3_6-5-5.png'
        self.animated = True
        images = []
        # TODO parse image

    def leave(self, obj, speed):
        while pygame.sprite.collide_mask(self, obj):
            self.move(*speed)

    def handle_collision(self, obj):
        sides = self.get_surface_lines()
        collision = [None, None, None, None]
        collided = 0
        for surface_line in obj.get_surface_lines():
            for j in range(len(sides)):
                if lines_collide(surface_line, sides[j]):
                    collided += 1
                    collision[j] = surface_line

        if ((collision[0] or collision[2]) and
                (collision[1] or collision[3])):
            if collision[0]:
                max_y = max(j for i in range(4) if collision[i]
                            for j in collision[i][1::2])
                if self.y - self.speed[1] > max_y:
                    self.leave(obj, (0, 1))
                    if self.speed[1] < 0:
                        self.speed[1] = 0
            else:
                # Синус для эффекта сложности подъёма
                self.leave(obj, (sin_from_line(collision[2]) * 1 if
                                 collision[3] else -1, -1))
                self.stands = True
                if self.speed[1] > 0:
                    self.speed[1] = 0
        if collision[1] and collision[3]:
            self.leave(obj, (0, 1 if self.speed[1] < 0 else -1))
            if self.speed[1] > 0:
                self.stands = True
            self.speed[1] = 0
        elif collision[0] and collision[2]:
            self.leave(obj, (1 if self.speed[0] < 0 else -1, 0))
            self.speed[0] = 0
        elif collision[0] and not (collision[1] or collision[3]):
            self.leave(obj, (0, 1))
        elif collision[1]:
            self.rect.y -= self.speed[1] - 2
            if pygame.sprite.collide_mask(self, obj):
                self.rect.y += self.speed[1]
                self.leave(obj, (-1, 0))
        elif collision[2]:
            self.leave(obj, (0, -1))
            self.stands = True
        elif collision[3]:
            self.leave(obj, (1, 0))

    def check_collision(self):
        for barrier in self.game.barriers:
            if pygame.sprite.collide_mask(self, barrier):
                self.handle_collision(barrier)
        for platform in self.game.platforms:
            if pygame.sprite.collide_mask(self, platform):
                if not self.ignore_platforms:
                    self.handle_collision(platform)
                    return True
        return False

    def update(self, *args):
        # Подсчёт скорости
        if self.moves:
            if self.direction == self.LEFT:
                self.move_left()
            else:
                self.move_right()
        elif self.speed[0] > 0:
            self.speed[0] -= self.acceleration
        elif self.speed[0] < 0:
            self.speed[0] += self.acceleration

        if self.speed[0] or not self.stands:
            self.speed[1] += GRAVITY
            self.stands = False

        if self.speed[0] or self.speed[1]:
            self.move(self.speed[0], self.speed[1])
            self.refresh_image()

            self.prev_frame_collision = self.check_collision()

            self.game.camera.update(self)
            self.refresh_image()


class Player(LivingCreature):
    def __init__(self, groups, image, game, max_speed, health, jump_speed):
        super().__init__(groups, image, game, max_speed, health)
        self.jump_speed = jump_speed
        self.inventory = []
        self.selection = 0

    def add_to_inventory(self, thing: Thing):
        pass

    def use_thing(self):
        # Использовать выбранную в инвентаре вещь
        pass

    def jump(self):
        self.stands = False
        self.speed[1] = -self.jump_speed

    def update(self, *args):
        pressed = pygame.key.get_pressed()

        # Движение по оси x
        if pressed[pygame.K_LEFT]:
            self.direction = self.LEFT
            self.moves = True
        elif pressed[pygame.K_RIGHT]:
            self.direction = self.RIGHT
            self.moves = True
        else:
            self.moves = False

        # Прыжок
        if pressed[pygame.K_UP] and self.stands:
            self.jump()

        # Bullet
        if pressed[pygame.K_SPACE]:
            Bullet((self.game.all_sprites, ), self.game,
                   (5 * self.direction, 0), 3).move(self.x, self.y)
        super().update(*args)


class Enemy(LivingCreature):
    def __init__(self, groups, images, game, speed: int, health: int,
                 weapon: Weapon = None):
        super().__init__(groups, images, game, speed, health)
        self.weapon = weapon

    def set_weapon(self, weapon):
        self.weapon = weapon

    def use_weapon(self):
        pass
