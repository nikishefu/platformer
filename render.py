import pygame


WINDOW_SIZE = width, height = 900, 900   # Размер окна (пиксели) + видимая область


def cell_lst(field_size, cell_size):   # field_size - размер поля (ячейки), cell_size - размер ячейки (пиксели)

    #   Создание списка хранящего в себе клетки (координаты, свойства, id)
    lst = [[[0, 0, 0, 0, ['properties'], 1] for i in range(field_size[0])] for j in range(field_size[1])]

    #   Создание изначальных характеристик клеток
    x_cell_one = y_cell_one = 0   # Координаты начала клетки
    x_cell_two = y_cell_two = x_cell_one + cell_size   # Координаты конца клетки
    id = 1   # id каждой клетки

    #   Назначении каждой клетки ее координат и id
    for j in range(field_size[1]):
        for i in range(field_size[0]):

            #   Присваивание координат клетки
            lst[j][i][0], lst[j][i][1], lst[j][i][2], lst[j][i][3] = x_cell_one, y_cell_one, x_cell_two, y_cell_two
            lst[j][i][5] = id

            # Изменение на следующие координаты по X
            x_cell_one += cell_size
            x_cell_two += cell_size

            id += 1   # Изменение id

        #   Изменение на следующие координаты по Y
        y_cell_one += cell_size
        y_cell_two += cell_size

        #   Обнуление координат по X
        x_cell_one = 0
        x_cell_two = x_cell_one + cell_size

    return lst


cells = cell_lst((10, 5), 50)
print(cells)
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()