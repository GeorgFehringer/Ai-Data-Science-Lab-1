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

def Inversions(arr):
    count = 0

    for i in range (0, 9):
        for j in range (i + 1, 9):
            if arr[j] != 0 and arr[i] != 0 and arr[j] < arr[i]:
                count += 1

    return count

def Solvability(puzzle):

    count = 0
    arr = [0,0,0,0,0,0,0,0,0]

    for i in range (0,3):
        for j in range (0,3):

            arr[count] = [puzzle[i][j]]
            count += 1

    inversions = Inversions(arr)

    if inversions % 2 == 0:
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

    print(manhattan_distance())

    emptyX, emptyY = find_pos(0, puzzle)
    print(emptyX, emptyY)

    if Solvability(puzzle):
        print ("Yes, solving continious")
    else:
        print ("Puzzle is not solveable therefore programm is terminated")