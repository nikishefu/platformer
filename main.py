import pygame
import objects
import vectors

# Размеры окна
WIN_W = 1080
WIN_H = 720

FPS = 60


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def get_pos(self):
        return self.x, self.y

    def set_x(self, value):
        self.x = value
        if self.x < 0:
            self.x = 0

    def set_y(self, value):
        self.y = value
        if self.y < 0:
            self.y = 0

    def update(self, target):
        self.set_x(round(target.x) + target.rect.width // 2 - WIN_W // 2)
        self.set_y(round(target.y) + target.rect.height // 2 - WIN_H // 2)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.running = True
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Платформер")

        self.to_delete = []

        # Группы спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.player_gr = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.group_list = [self.all_sprites, self.player_gr, self.platforms,
                           self.barriers]

        # Главные объекты
        self.camera = Camera()
        img = pygame.Surface((40, 60))
        pygame.draw.rect(img, (255, 255, 255), (0, 0, 40, 60))
        self.player = objects.Player((self.player_gr, self.all_sprites),
                                     img, self, 5, 100, 10)

        # Карта игры
        img2 = pygame.Surface((700, 100))
        pygame.draw.rect(img2, (0, 255, 255), (0, 0, 700, 100))
        objects.Entity((self.all_sprites, self.platforms), img2, False, self).move(10, 500)

        img3 = img.copy()
        pygame.draw.rect(img3, (255, 0, 0), (0, 0, 40, 60))
        objects.Entity((self.all_sprites, self.barriers), img3, False, self).move(200, 450)

        img4 = pygame.Surface((600, 100))
        objects.Polygon((self.all_sprites, self.barriers), self, (
            (0, 200), (0, 150), (100, 50), (300, 50), (350, 100), (450, 75),
            (500, 0), (550, 200)
        )).move(400, 200)

        img5 = img.copy()
        pygame.draw.rect(img5, (255, 0, 0), (0, 0, 40, 110))
        objects.Entity((self.all_sprites, self.barriers), img5, False, self).move(300, 400)

    def update_aim(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        vec = (mouse_x - self.player.rect.x, mouse_y - self.player.rect.y)
        self.player.fire_vector = vectors.normalize(vec)

    def load_level(self, path):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           pygame.mouse.get_pos(), 10)
        self.update_aim()
        pygame.display.flip()

    def delete_objects(self):
        for obj in self.to_delete[::-1]:
            for i in self.group_list:
                if i.has_internal(obj):
                    i.remove_internal(obj)
            del obj

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.delete_objects()
            clock.tick(FPS)


if __name__ == '__main__':
    Game().run()
