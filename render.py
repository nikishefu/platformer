import pygame


WINDOW_SIZE = width, height = 900, 900   # Размер окна (пиксели) + видимая область
FIELD_SIZE = horizontal, vertical = 10, 5   # Размеры поля (ячейки)
CELL_SIZE = 50   # Размер одной квадратной клетки (пиксели)

#   Создание списка хранящего в себе клетки (координаты, свойства, id)
lst = [[[0, 0, 0, 0, ['properties'], 1] for i in range(horizontal)] for j in range(vertical)]

#   Создание изначальных характеристик клеток
x_cell_one = y_cell_one = 0   # Координаты начала клетки
x_cell_two = y_cell_two = x_cell_one + CELL_SIZE   # Координаты конца клетки
id = 1   # id каждой клетки

#   Назначении каждой клетки ее координат и id
for j in range(vertical):
    for i in range(horizontal):

        #   Присваивание координат клетки
        lst[j][i][0], lst[j][i][1], lst[j][i][2], lst[j][i][3] = x_cell_one, y_cell_one, x_cell_two, y_cell_two
        lst[j][i][5] = id

        # Изменение на следующие координаты по X
        x_cell_one += CELL_SIZE
        x_cell_two += CELL_SIZE

        id += 1   # Изменение id

    #   Изменение на следующие координаты по Y
    y_cell_one += CELL_SIZE
    y_cell_two += CELL_SIZE

    #   Обнуление координат по X
    x_cell_one = 0
    x_cell_two = x_cell_one + CELL_SIZE


print(lst)
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()