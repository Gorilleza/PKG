import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Определяем координаты вершин буквы "X"
vertices = np.array([
    [-1, -1, 0],
    [1, 1, 0],
    [-1, 1, 0],
    [1, -1, 0],
    [0, 0, 1],
    [0, 0, -1]
])

# Функция для построения каркасной модели
def plot_wireframe(vertices):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Создаем ребра между вершинами
    edges = [
        (0, 1), (2, 3),  # "X" верхние и нижние диагонали
        (4, 0), (4, 1), (4, 2), (4, 3),  # соединение с верхней вершиной
        (5, 0), (5, 1), (5, 2), (5, 3)   # соединение с нижней вершиной
    ]

    for edge in edges:
        ax.plot3D(*zip(vertices[edge[0]], vertices[edge[1]]), color='b')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title("Wireframe Model of 'X'")
    plt.show()

# Функция для применения преобразований
def transform_vertices(vertices, translation=None, scale=None, rotation_axis=None, theta=0):
    # Перенос
    if translation is not None:
        vertices += translation
    
    # Масштабирование
    if scale is not None:
        vertices *= scale
    
    # Вращение
    if rotation_axis is not None:
        # Создание матрицы вращения
        theta_rad = np.radians(theta)
        if rotation_axis == 'x':
            rotation_matrix = np.array([[1, 0, 0],
                                         [0, np.cos(theta_rad), -np.sin(theta_rad)],
                                         [0, np.sin(theta_rad), np.cos(theta_rad)]])
        elif rotation_axis == 'y':
            rotation_matrix = np.array([[np.cos(theta_rad), 0, np.sin(theta_rad)],
                                         [0, 1, 0],
                                         [-np.sin(theta_rad), 0, np.cos(theta_rad)]])
        elif rotation_axis == 'z':
            rotation_matrix = np.array([[np.cos(theta_rad), -np.sin(theta_rad), 0],
                                         [np.sin(theta_rad), np.cos(theta_rad), 0],
                                         [0, 0, 1]])
        else:
            raise ValueError("Invalid rotation axis. Choose 'x', 'y', or 'z'.")

        vertices = vertices @ rotation_matrix.T
    
    return vertices

# Основная функция
def main():
    # Начальное построение
    plot_wireframe(vertices)

    # Применяем преобразования
    translation = np.array([2, 2, 0])   # Перенос на (2, 2, 0)
    scale = np.array([1.5, 1.5, 1.5])   # Масштабирование на 1.5
    rotation_axis = 'z'                 # Вращение вокруг оси Z
    theta = 45                           # Угол вращения в градусах

    transformed_vertices = transform_vertices(vertices.copy(), translation=translation, scale=scale,
                                               rotation_axis=rotation_axis, theta=theta)

    # Построение после преобразований
    plot_wireframe(transformed_vertices)

if __name__ == "__main__":
    main()
