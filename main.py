import numpy as np

if __name__ == '__main__':

    puzzle = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    count = 8
    for i in range (3):
        for j in range (3):
            puzzle [i][j] = count
            count -= 1

    for x in puzzle:                   #dreckiger Julius Code
        print(x)
