import pygame


WINDOW_SIZE = width, height = 900, 900   # Размер окна (пиксели) + видимая область
FIELD_SIZE = horizontal, vertical = 10, 5   # Размеры поля (ячейки)
CELL_SIZE = 50   # Размер одной квадратной клетки (пиксели)


def draw_cells(cell_size, color, field_size):
    x = y = 0
    color = pygame.Color(color)
    for i in range(field_size[1]):
        for j in range(field_size[0]):
            pygame.draw.rect(screen, color, (x, y, x + cell_size, y + cell_size), 1)
            x += cell_size
        y += cell_size
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
draw_cells(CELL_SIZE, 'white', FIELD_SIZE)
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()