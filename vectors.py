"""
Функции для работы с двумерными векторами вида tuple(float, float).
Copyright Gribushenkov N.A. Or copycenter. Or, maybe, copyleft.
Нет, сделать класс с названием Vector не проще. Ибо так быстрее.
"""


def get_len(vector) -> float:
    """Длина вектора"""
    return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def normalize(vector) -> (float, float):
    """Приведение к единичной длине"""
    vec_len = get_len(vector)
    return (0, 0) if vec_len == 0 else (vector[0] / vec_len,
                                        vector[1] / vec_len)


def dot_product(vector1, vector2) -> float:
    """Скалярное произведение"""
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]


def vector_product_z(vector1, vector2) -> float:
    """Компонента Z векторного произведения"""
    return vector1[0] * vector2[1] - vector1[1] * vector2[0]


def mult_vector_by_scal(vector, scal) -> (float, float):
    """Умножение вектора на число"""
    return vector[0] * scal, vector[1] * scal


def symmetry12(vector1, vector2) -> (float, float):
    """
    Получение вектора, симметричного vector1, относительно прямой, на
    которой лежит нормаль к vector2, в перевёрнутом виде
    """
    vector2 = normalize(vector2)
    vector2 = mult_vector_by_scal(vector2, 2 * dot_product(vector1, vector2))
    return vector2[0] - vector1[0], vector2[1] - vector1[1]
