import pygame
import objects

# Window size
WIN_W = 800
WIN_H = 600


def redraw(scr):
    scr.fill((0, 0, 0))
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Платформер")

    clock = pygame.time.Clock()
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        redraw(screen)
