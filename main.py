import numpy as np


class Node:
    def __init__(self, g, h, previous_node, previous_move, previous_f, puzzle_array):
        self.previous_Node = previous_node
        self.previous_Move = previous_move
        self.g = g
        self.h = h
        self.previous_f = previous_f
        self.puzzle_array = puzzle_array


def find_pos(number, array):
    for i in range(3):
        for j in range(3):
            if array[i][j] == number:
                xtest = j
                ytest = i
                return xtest, ytest


def get_hamming_distance(puzzle, goal):
    sum = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle[i, j] != goal[i, j]:
                sum += 1
    return sum


def get_manhattan_distance(puzzle_array, goal_array):
    man_distance = 0
    for i in range(1, 9):
        x1, y1 = find_pos(i, puzzle_array)
        x2, y2 = find_pos(i, goal_array)
        man_distance = man_distance + (abs(x1 - x2) + abs(y1 - y2))
    return man_distance


def inversions(arr):  # 8-Puzzle are only then solvable, if there is an even number of inversions.
    # Therefore we count them before we try to solve the puzzle
    count = 0

    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] < arr[i]:
                count += 1

    return count


def solvability(puzzle):  # For the Inversion Function to work, we need a 1D Array.
    # Because the puzzle is an 2D Array we need to convert the data.
    count = 0
    arr = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 3):
        for j in range(0, 3):
            arr[count] = [puzzle[i][j]]
            count += 1

    inversions_count = inversions(arr)  # After converting the data to a 1D array we can count the number of Inversions

    if inversions_count % 2 == 0:  # If there are an even amount of inversions, the puzzle is solvable
        return True
    else:
        return False


def validate_move(node, direction):
    # get coordinates of empty tile, to validate the move into the right direction
    x_cords, y_cords = find_pos(0, puzzle)

    # check if move is possible
    if direction == "up" and x_cords > 0 and node.previous_move != "down":
        return True
    if direction == "down" and x_cords < 2 and node.previous_move != "up":
        return True
    if direction == "left" and y_cords > 0 and node.previous_move != "right":
        return True
    if direction == "right" and y_cords < 2 and node.previous_move != "left":
        return True
    else:
        return False


if __name__ == '__main__':

    puzzle = np.random.choice(np.arange(9), size=(3, 3), replace=False)

    for x in puzzle:
        print(x)

    print()

    goal = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    for x in goal:
        print(x)

    print()
    print(get_manhattan_distance(puzzle, goal))

    emptyX, emptyY = find_pos(0, puzzle)
    print(emptyX, emptyY)

    if solvability(puzzle):
        print("Yes, solving continues")
    else:
        print("Puzzle is not solvable, therefore program is terminated")
