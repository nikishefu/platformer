import pygame


WINDOW_SIZE = width, height = 500, 500   # Размер окна (пиксели) + видимая область


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


def grid(lst):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            draw_cell(lst, lst[i][j][5], (255, 255, 255), True)
            pygame.display.flip()


def draw_cell(lst, cell_id, color, name=False):
    if isinstance(color, str):
        color = pygame.Color(color)
    elif isinstance(color, list):
        color = pygame.Color(color[0], color[1], color[2])
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j][5] == cell_id:
                pygame.draw.rect(screen, color, ((lst[i][j][0], lst[i][j][1]),
                                                 (lst[i][j][2] - lst[i][j][0], lst[i][j][3] - lst[i][j][1])), 1)
            if name:
                number = lst[i][j][5]
                y_cord = lst[i][j][1] + 15
                x_cord = lst[i][j][0] + 20
                if len(str(number)) == 2:
                    x_cord = lst[i][j][0] + 14
                elif len(str(number)) == 3:
                    x_cord = lst[i][j][0] + 7
                elif len(str(number)) == 4:
                    x_cord = lst[i][j][0]
                font = pygame.font.Font(None, 30)
                text = font.render(str(number), True, (255, 255, 255))
                screen.blit(text, (x_cord, y_cord))


cells = cell_lst((10, 10), 50)
print(cells)
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
screen.fill((0, 0, 0))
running = True
cell_status = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                if not cell_status:
                    cell_status = True
                    grid(cells)
                else:
                    cell_status = False
                    screen.fill((0, 0, 0))
                    pygame.display.flip()
