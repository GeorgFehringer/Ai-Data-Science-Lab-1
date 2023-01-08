import math
import time
import numpy as np

h_time = np.zeros(100)  # creates an array for saving the time it takes to solve each puzzle using hamming distance
m_time = np.zeros(100)  # creates an array for saving the time it takes to solve each puzzle using manhattan distance
h_nodes = np.zeros(100)  # creates an array for saving the number of expanded nodes using hamming distance
m_nodes = np.zeros(100)  # creates an array for saving the number of expanded nodes using manhattan distance
counter_expanded = 0  # Counter for the expanded nodes for each puzzle and each heuristic
counter_finished = 0  # Counter for already solved puzzles with both algorithms
goal = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])  # The goal of the puzzle for comparison


def solvability(solv):
    # For the Inversion Function to work, we need a 1D Array.
    # Because the puzzle is a 2D Array we need to convert the data.
    # and then check it for the number of inversions
    # Input a 3x3 array; output: boolean for the solvability of the puzzle
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
    # 8-Puzzles are only solvable, if there is an even number of inversions.
    # Therefore, we count them before we try to solve the puzzle
    # Input: Starting Puzzle as 1D Array Output: the number of inversions
    count = 0

    for i in range(0, 8):
        for j in range(i + 1, 8):
            if arr[j] < arr[i]:
                count += 1

    return count


class Node:
    def __init__(self, g, h, previous_node, previous_move, puzzle_array):
        self.previous_node = previous_node  # "Parent Node"
        self.previous_move = previous_move  # how we came to that node
        self.g = g  # how many moves already happened
        self.h = h  # Hamming or Manhattan distance
        self.puzzle_array = puzzle_array  # the current state of the puzzle


def hash_state(array):
    # Function for assigning each Puzzle state a unique identifier. We multiply each field in the puzzle by a power of
    # ten. If we return to a previous puzzle state, we can identify it and will not create a new node.
    hash = (array[0, 0] * 1 + array[0, 1] * 10 + array[0, 2] * 100
            + array[1, 0] * 1000 + array[1, 1] * 10000 + array[1, 2] * 100000
            + array[2, 0] * 1000000 + array[2, 1] * 10000000 + array[2, 2] * 100000000)
    return hash


def expand_node(node, node_list, heu, hash_list):
    # Function for expanding the nodes. It checks all possible directions and saves the states
    # Input: current node, node_list, heuristic and hash_list - Output: None
    global counter_expanded
    counter_expanded += 1
    row, col = find_pos(0, node.puzzle_array)
    if validate_move(node, "u"):  # if the move is valid we create the new puzzle state and check if it already exists
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row - 1, col]
        new_array[row - 1, col] = 0
        hash = hash_state(new_array)
        if hash not in hash_list:
            new_node = Node(node.g + 1, heu(new_array, goal), node, "u", new_array)  # we create the new state
            node_list.append(new_node)  # and append it to the list to sort for cost
            hash_list.append(hash)
    if validate_move(node, "d"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row + 1, col]
        new_array[row + 1, col] = 0
        hash = hash_state(new_array)
        if hash not in hash_list:
            new_node = Node(node.g + 1, heu(new_array, goal), node, "d", new_array)
            node_list.append(new_node)
            hash_list.append(hash)
    if validate_move(node, "l"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row, col - 1]
        new_array[row, col - 1] = 0
        hash = hash_state(new_array)
        if hash not in hash_list:
            new_node = Node(node.g + 1, heu(new_array, goal), node, "l", new_array)
            node_list.append(new_node)
            hash_list.append(hash)
    if validate_move(node, "r"):
        new_array = np.copy(node.puzzle_array)
        new_array[row, col] = new_array[row, col + 1]
        new_array[row, col + 1] = 0
        hash = hash_state(new_array)
        if hash not in hash_list:
            new_node = Node(node.g + 1, heu(new_array, goal), node, "r", new_array)
            node_list.append(new_node)
            hash_list.append(hash)


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
    f = node.h  #+ node.g
    # At first, we wanted to sort by the f-score (Distance + Depth). Later on we figured out that our program is faster
    # if we are just using the distance.
    return f


def find_pos(number, array):
    # input: a 3x3 array and a number; output: the position of the number in the array
    for i in range(3):
        for j in range(3):
            if array[i][j] == number:
                x_cord = i
                y_cord = j
                return x_cord, y_cord


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
    # the manhattan distance is calculated by looking at the distance each number has from its correct position
    man_distance = 0
    for i in range(1, 9):
        x1, y1 = find_pos(i, puzzle_array_m)
        x2, y2 = find_pos(i, goal_array_m)
        man_distance = man_distance + (abs(x1 - x2) + abs(y1 - y2))
    return man_distance


def solve_8_puzzle(puzzle_array, heu):
    global h_time
    global m_time
    global counter_finished

    # First we create the first node as well as the node- and hashlist
    current_node = Node(0, heu(puzzle_array, goal), None, "n", puzzle_array)
    node_list = [current_node, ]
    hash_list = [hash_state(puzzle_array), ]
    start_time = time.time()  # We note the current time before solving the puzzles
    while current_node.h != 0:  # As long as the puzzle is not solved we expand and select the next move
        expand_node(current_node, node_list, heu, hash_list)
        del node_list[0]
        node_list.sort(key=calc_cost)
        current_node = node_list[0]
    end_time = time.time()  # After finishing we note the end time and save it in the correct array
    if heu == get_hamming_distance:
        h_time[counter_finished] = end_time - start_time
        h_nodes[counter_finished] = counter_expanded
    if heu == get_manhattan_distance:
        m_time[counter_finished] = end_time - start_time
        m_nodes[counter_finished] = counter_expanded


def solve_all():
    # This function starts the cycle, which solves 100 puzzle both with the Hamming and the Manhattan Heuristic.
    global counter_finished
    counter_finished = 0
    while counter_finished < 100:
        puzzle = np.random.choice(np.arange(9), size=(3, 3), replace=False)  # creates an random puzzle
        if solvability(puzzle):     # if the puzzle is not solvable we immediately create a new puzzle
            solve_8_puzzle(puzzle, get_hamming_distance)
            solve_8_puzzle(puzzle, get_manhattan_distance)
            counter_finished += 1   # only solvable (and solved) puzzles count.
            print(counter_finished)


def standard_deviation(array):
    # Function for calculate the standard deviation.
    # Input: array filled with the times; Output: Standard Deviation
    mean = np.sum(array) / 100
    sum_squared = 0
    for i in range(0, 100):
        sum_squared += math.pow(array[i] - mean, 2)
    var = np.sum(sum_squared) / 100
    dev = math.sqrt(var)
    return dev


if __name__ == '__main__':  # Function for starting the solving and printing out the stats
    solve_all()

    print("avg time hamming", np.sum(h_time) / 100)
    print("avg standard deviation time hamming", standard_deviation(h_time))
    print("avg nodes expanded hamming", np.sum(h_nodes) / 100)
    print("avg standard deviation nodes expanded hamming", standard_deviation(h_nodes))
    print("avg time manhattan", np.sum(m_time) / 100)
    print("avg standard deviation time manhattan", standard_deviation(m_time))
    print("avg nodes expanded manhattan", np.sum(m_nodes) / 100)
    print("avg standard deviation nodes expanded manhattan", standard_deviation(m_nodes))
