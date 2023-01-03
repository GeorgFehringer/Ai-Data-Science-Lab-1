import timeit
import numpy as np

h_time = np.zeros(100)
m_time = np.zeros(100)
h_nodes = np.zeros(100)
m_nodes = np.zeros(100)
counter_expanded = 0
counter_finished = 0


def solvability(solv):
    # For the Inversion Function to work, we need a 1D Array.
    # Because the puzzle is an 2D Array we need to convert the data.
    # Input a 3x3 array; output: boolean if the array is solvable
    count = 0
    arr = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 3):
        for j in range(0, 3):
            if solv[i][j] != 0:
                arr[count] = [solv[i][j]]
                count += 1

    inversions_count = inversions(arr)  # After converting the data to a 1D array we can count the number of Inversions

    if inversions_count % 2 == 0:  # If there are an even amount of inversions, the puzzle is solvable
        return True
    else:
        return False

def inversions(arr):
    # 8-Puzzle are only then solvable, if there is an even number of inversions.
    # Therefore we count them before we try to solve the puzzle
    # Input: and array Output: the number of inversions
    count = 0

    for i in range(0, 8):
        for j in range(i + 1, 8):
            if arr[j] < arr[i]:
                count += 1

    return count

class Node:
    def __init__(self, g, h, previous_node, previous_move, puzzle_array):
        self.previous_node = previous_node
        self.previous_move = previous_move
        self.g = g
        self.h = h
        self.puzzle_array = puzzle_array


def expand_node(node, node_list, heu):
    global counter_expanded
    counter_expanded += 1
    row, col = find_pos(0, node.puzzle_array)
    if validate_move(node, "u"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row-1, col]
        new_array[row-1, col] = 0
        new_node = Node(node.g + 1, heu(new_array, goal), node, "u", new_array)
        node_list.append(new_node)
    if validate_move(node, "d"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row+1, col]
        new_array[row+1, col] = 0
        new_node = Node(node.g + 1, heu(new_array, goal), node, "d", new_array)
        node_list.append(new_node)
    if validate_move(node, "l"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row, col-1]
        new_array[row, col-1] = 0
        new_node = Node(node.g + 1, heu(new_array, goal), node, "l", new_array)
        node_list.append(new_node)
    if validate_move(node, "r"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row, col+1]
        new_array[row, col+1] = 0
        new_node = Node(node.g + 1, heu(new_array, goal), node, "r", new_array)
        node_list.append(new_node)


def validate_move(node, direction):
    # Input: a node and a direction; output: boolean if the move is possible
    # get coordinates of empty tile, to validate the move into the right direction
    row, col = find_pos(0, node.puzzle_array)

    # check if move is possible and if it is not undoing the previous move
    # u = up; d = down; r = right; l = left
    if direction == "u" and row > 0 and node.previous_move != "d":
        return True
    if direction == "d" and row < 2 and node.previous_move != "u":
        return True
    if direction == "l" and col > 0 and node.previous_move != "r":
        return True
    if direction == "r" and col < 2 and node.previous_move != "l":
        return True
    else:
        return False


def calc_cost(node):
    # input: node; output: cost(int)
    # calculates the cost and returns it
    f = node.g + node.h
    return f


def find_pos(number, array):
    # input: a 3x3 array and a number; output: the position of the number in the array
    for i in range(3):
        for j in range(3):
            if array[i][j] == number:
                xtest = i
                ytest = j
                return xtest, ytest


def get_hamming_distance(puzzle_array_h, goal_array_h):
    # Input: 2 3x3 arrays one is the current and one is the goal state; Output: the number of correctly placed numbers
    ham_distance = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if puzzle_array_h[i, j] != goal_array_h[i, j]:
                ham_distance += 1
    return ham_distance


def get_manhattan_distance(puzzle_array_m, goal_array_m):
    # Input: 2 3x3 arrays one is the current and one is the goal state; Output: manhattan distance(int)
    # the manhattan distance is calculated by looking at the
    man_distance = 0
    #print(puzzle_array_m)
    for i in range(1, 9):
        x1, y1 = find_pos(i, puzzle_array_m)
        x2, y2 = find_pos(i, goal_array_m)
        man_distance = man_distance + (abs(x1 - x2) + abs(y1 - y2))
    return man_distance


def solve_8_puzzle(puzzle_array, heu):
    global h_time
    global m_time
    global counter_finished

    current_node = Node(0, heu(puzzle_array, goal), None, "n", puzzle_array)
    node_list = [current_node, ]
    start_time = timeit.timeit()
    while current_node.h != 0:
        expand_node(current_node, node_list, heu)
        del node_list[0]
        node_list.sort(key=calc_cost)
        current_node = node_list[0]
    end_time = timeit.timeit()
    if heu == get_hamming_distance:
        h_time[counter_finished] = end_time - start_time
        h_nodes[counter_finished] = counter_expanded
    if heu == get_manhattan_distance:
        m_time[counter_finished] = end_time - start_time
        m_nodes[counter_finished] = counter_expanded


def solve_all():
    global counter_finished
    counter_finished = 0
    while counter_finished < 100:
        puzzle = np.random.choice(np.arange(9), size=(3, 3), replace=False)
        if solvability(puzzle):
            solve_8_puzzle(puzzle, get_hamming_distance)
            solve_8_puzzle(puzzle, get_manhattan_distance)
            counter_finished += 1
            print(counter_finished)


if __name__ == '__main__':

    # puzzle = np.random.choice(np.arange(9), size=(3, 3), replace=False)
    # puzzle = np.array([[3, 1, 4], [6, 2, 7], [8, 0, 5]])

#    for x in puzzle:
#        print(x)
    goal = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])


    # if solvability(puzzle):
    #     print("Yes, solving continues")
    #     type = input("if you want to solve with manhattan type m if you want to solve with hamming typ h: ")
    #     if type == "m":
    #         solve_8_puzzle(puzzle, get_manhattan_distance)
    #     elif type == "h":
    #         solve_8_puzzle(puzzle, get_hamming_distance)
    #     else:
    #         print("invalid input")
    # else:
    #     print("Puzzle is not solvable, therefore program is terminated")

    solve_all()

    print("avg time hamming", np.sum(h_time)/100)
    print("avg nodes expanded hamming", np.sum(h_nodes)/100)
    print("avg time manhattan", np.sum(m_time)/100)
    print("avg nodes expanded manhattan", np.sum(m_nodes)/100)