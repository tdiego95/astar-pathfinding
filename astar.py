# A* PATHFINDING ALGORITHM #

from queue import PriorityQueue
import numpy as np

# 10x10 board
# A -> starting point
# B -> target point
# x -> blocked spot
# Edit this board and try it out!
board = [
    ['A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'x', ' ', ' ', 'x', 'x', 'x', ' ', ' '],
    [' ', ' ', 'x', ' ', ' ', 'x', ' ', ' ', ' ', ' '],
    [' ', ' ', 'x', 'x', ' ', 'x', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'x', ' ', 'x', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', 'B', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
]


class Node:
    def __init__(self, position: tuple):
        self.x, self.y = position

    def get_pos(self) -> tuple:
        return self.x, self.y

    def get_neighbors(self, grid):
        neighbors = []
        if self.x < len(board) - 1 and not board[self.x + 1][self.y] == 'x':  # DOWN
            neighbors.append(grid[self.x + 1][self.y])

        if self.x > 0 and not board[self.x - 1][self.y] == 'x':  # UP
            neighbors.append(grid[self.x - 1][self.y])

        if self.y < len(board) - 1 and not board[self.x][self.y + 1] == 'x':  # RIGHT
            neighbors.append(grid[self.x][self.y + 1])

        if self.y > 0 and not board[self.x][self.y - 1] == 'x':  # LEFT
            neighbors.append(grid[self.x][self.y - 1])

        return neighbors


def reconstruct_path(came_from: dict, current: Node):
    while current in came_from:
        current = came_from[current]
        board[current.x][current.y] = 'o'  # DRAW STEP

    board[current.x][current.y] = 'A'


def calculate_h(current_pos: tuple, target_pos: tuple) -> int:
    x, y = current_pos
    target_x, target_y = target_pos
    return abs(target_x - x) + abs(target_y - y)


def make_nodes_grid():
    nodes_grid = []
    for i in range(len(board)):
        nodes_grid.append([])
        for j in range(len(board)):
            node = Node((i, j))
            nodes_grid[i].append(node)

    return nodes_grid


# Print board on console
def print_board():
    for j in range(len(board)):
        print('- - - - - - - - - - - - - - - - - - - - - - - - -')
        for k in range(len(board[0])):
            print('| ', end='')

            if k == len(board[0]) - 1:
                print(board[j][k], ' ')
            else:
                print(board[j][k], ' ', end='')


def main():
    print_board()
    grid = make_nodes_grid()

    a = np.array(board)
    b = np.where(a == 'A')
    start_node: Node = grid[b[0][0]][b[1][0]]
    b = np.where(a == 'B')
    target_node: Node = grid[b[0][0]][b[1][0]]

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_node))
    came_from: dict = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start_node] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start_node] = calculate_h(start_node.get_pos(), target_node.get_pos())

    open_set_hash = {start_node}

    while not open_set.empty():

        current_node: Node = open_set.get()[2]
        open_set_hash.remove(current_node)

        if current_node.x == target_node.x and current_node.y == target_node.y:
            print('Path found!')
            reconstruct_path(came_from, target_node)
            print_board()
            break

        for neighbor in current_node.get_neighbors(grid):
            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + calculate_h(neighbor.get_pos(), target_node.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)


if __name__ == '__main__':
    main()
