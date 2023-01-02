import numpy as np


def find_pos(number,array):
    for i in range (3):
        for j in range(3):
            if array[i][j] == number:
                x = j
                y = i
                return x, y

def manhattan_distance():
    sum = 0
    for i in range(1,9):
        x1, y1 = find_pos(i, puzzle)
        x2, y2 = find_pos(i, goal)
        sum = sum +(abs(x1 - x2) + abs(y1 - y2))
    return sum

if __name__ == '__main__':

    puzzle = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    count = 8
    for i in range (3):
        for j in range (3):
            puzzle [i][j] = count
            count -= 1

    for x in puzzle:                   #dreckiger Julius Code
        print(x)

    print()


    goal = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    for x in goal:
        print(x)

    print(manhattan_distance())

    emptyX, emptyY = find_pos(0, puzzle)
    print(emptyX, emptyY)
