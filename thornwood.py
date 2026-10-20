import random
import math
import copy


GRID = [
    [52, 58, 52, 46, 40, 46, 53, 46],
    [58, 64, 58, 52, 46, 58, 60, 53],
    [64, 70, 64, 58, 53, 60, 67, 60],
    [58, 64, 58, 53, 60, 67, 74, 67],
    [52, 58, 53, 50, 67, 74, 81, 74],
    [46, 53, 60, 67, 74, 81, 88, 81],
    [53, 60, 67, 74, 81, 88, 95, 88],
    [46, 53, 60, 67, 74, 81, 88, 81],
]


def generate_neighbors(cell):
    """returns a list of valid neighbor states"""
    curr_row = cell[0]
    curr_col = cell[1]
    neighbors = []
    dx = [-1,0,1,0]
    dy = [0,1,0,-1]
    for i in range(4):
        next_cell = (curr_row + dx[i], curr_col + dy[i])
        if next_cell[0] > -1 and next_cell[0] < 8 and next_cell[1] > -1 and next_cell[1] < 8:
            neighbors.append(next_cell)
    return neighbors

def find_value(cell):
    return GRID[cell[0]][cell[1]]


def steepest_ascent_hill_climbing(initial_state):
    """Part A: climb to the highest strictly-higher neighbour (ties: first in up/right/down/left order).
    Returns (steps, final_cell, final_value)."""
    current_pos = initial_state
    steps = 0
    while(True):
        neighbors = generate_neighbors(current_pos)
        next_pos = current_pos
        for neighbor in neighbors:
            if find_value(neighbor) > find_value(next_pos):
                next_pos = neighbor

        
        if next_pos == current_pos:
            return steps, current_pos, find_value(current_pos)
        
        current_pos = next_pos
        steps += 1



def random_restart():
    """Part B: hill climb from (0,0), (4,0), (7,0), (0,4).
    Returns (best_value, start_of_first_climb_reaching_it, total_steps)."""
    initial_states = [(0,0),(4,0),(7,0),(0,4)]
    total_steps = 0
    max_value = 0
    for state in initial_states:
        steps, final_pos, value = steepest_ascent_hill_climbing(state)
        total_steps += steps
        if value > max_value:
            max_value = value
            best_start = state

    return max_value, best_start, total_steps




def simulated_annealing(initial_state, seed =2):
    """Part C: 200 iterations of simulated annealing, T starts at 20.0 and is multiplied by 0.97 each iteration.
    Returns (final_cell, final_value, best_value, accepted_count)."""
    rng = random.Random(seed)
    current_state = initial_state
    T = 20.0
    best_value = find_value(current_state)
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    accepted = 0
    for _ in range(200):
        d = int(rng.random() * 4)
        neighbor = (current_state[0] + dr[d], current_state[1] + dc[d])
        if (0 <= neighbor[0] < 8 and 0 <= neighbor[1] < 8):
            delta = find_value(neighbor) - find_value(current_state)

            if delta >= 0:
                current_state = neighbor
                accepted += 1
            else:
                r = rng.random()
                if r < math.exp(delta / T):
                    current_state = neighbor
                    accepted += 1
        if find_value(current_state) > best_value:
            best_value = find_value(current_state)
        T *= 0.97

    return current_state, find_value(current_state), best_value, accepted


def fate_test():
    """Part D: run Part C with seeds 1..20 from (0,0). Returns how many runs end with final value 95."""
    return sum(simulated_annealing((0, 0), seed)[1] == 95 for seed in range(1, 21))



MAX_LOAD = 86
MAX_VOLUME = 44

# (load, volume, usefulness), index = tool number
TOOLS = [
    (18, 9, 36),
    (11, 8, 9),
    (12, 5, 10),
    (9, 3, 32),
    (5, 7, 31),
    (5, 6, 8),
    (11, 3, 33),
    (20, 6, 27),
    (13, 6, 5),
    (11, 2, 35),
    (14, 6, 21),
    (15, 9, 13),
    (8, 8, 26),
    (10, 9, 19),
    (10, 7, 38),
]

# generation 0, positions 0 to 19, bit 0 first
INITIAL_POPULATION = [
    "110101101111101",
    "100010101111010",
    "010111011011001",
    "000010110111000",
    "010001001010000",
    "110111110111011",
    "000011100111110",
    "111100000010000",
    "111011111111111",
    "001111100111111",
    "011001010000111",
    "000110000001011",
    "111001000111110",
    "001001000011010",
    "011001110010001",
    "011000010011110",
    "111011001000011",
    "110110010001011",
    "000001000010100",
    "001000111111000",
]


def calculate_fitness(chromosome):
    """Total usefulness of packed tools if load and volume limits hold, else 0."""
    fitness = 0
    total_load = 0
    total_volume = 0
    for i, gene in enumerate(chromosome):
        if gene == 1:
            fitness += TOOLS[i][2]
            total_load += TOOLS[i][0]
            total_volume += TOOLS[i][1]
    if total_load <= MAX_LOAD and total_volume <= MAX_VOLUME:
        return fitness
    return 0


def crossover(parent1, parent2, rng):
    """One-point crossover with probability 0.9; returns two new lists."""
    r = rng.random()
    if r < 0.9:
        cut = int(rng.random() * 14) + 1
        child1 = parent1[:cut] + parent2[cut:]
        child2 = parent2[:cut] + parent1[cut:]
        return child1, child2
    return parent1[:], parent2[:]


def mutation(chromosome, rng):
    """Flip each bit with probability 1/15 (one draw per bit, in order); returns a new list."""
    return [1 - gene if rng.random() < 1/15 else gene for gene in chromosome]

def tournament(population, rng):
    """Draw three positions, return the fittest chromosome (tie goes to the one drawn first)."""
    selected = [population[int(rng.random() * 20)] for _ in range(3)]
    best = selected[0]
    for chromosome in selected[1:]:
        if calculate_fitness(chromosome) > calculate_fitness(best):
            best = chromosome
    return best

def evaluate(population):
    """Returns (best_fitness, average_fitness, ranked_population); ties keep the lower position."""
    ranked = sorted(population, key=calculate_fitness, reverse=True)
    best_fitness = calculate_fitness(ranked[0])
    average_fitness = sum(calculate_fitness(c) for c in population) / 20
    return best_fitness, average_fitness, ranked


def GA():
    """Genetic algorithm, seed 12, generations 0 to 50.
    Returns (best fitness at gens 0,10,..50, best chromosome string, best fitness, first generation reaching it, final average)."""
    population = [[int(bit) for bit in c] for c in INITIAL_POPULATION]
    rng = random.Random(12)
    best_by_gen = []
    for generation in range(51):
        best_fitness, average_fitness, ranked = evaluate(population)
        best_by_gen.append(best_fitness)
        if generation == 50:
            break
        new_population = [ranked[0][:], ranked[1][:]]

        while(len(new_population) < 20):
            parent1 = tournament(population, rng)
            parent2 = tournament(population, rng)
            child1, child2 = crossover(parent1, parent2, rng)
            child1 = mutation(child1, rng)
            child2 = mutation(child2, rng)
            new_population.extend([child1, child2])

        population = new_population
    return (best_by_gen[::10], "".join(map(str, ranked[0])), best_fitness,
            best_by_gen.index(best_fitness), average_fitness)

def tomos_check():
    """Brute force over all 2^15 pouches. Returns (best_usefulness, chromosome string, bit 0 first)."""
    best_fitness = 0
    best_chromosome = None
    for mask in range(1 << 15):
        load = volume = fitness = 0
        for k in range(15):
            if mask >> k & 1:
                load += TOOLS[k][0]
                volume += TOOLS[k][1]
                fitness += TOOLS[k][2]
        if load <= MAX_LOAD and volume <= MAX_VOLUME and fitness > best_fitness:
            best_fitness = fitness
            best_chromosome = "".join(str(mask >> k & 1) for k in range(15))
    return best_fitness, best_chromosome

        


# Stone Drop start position, START_BOARD[row][col], list index 4 is the bottom row, index 0 is the top row
START_BOARD = [
    list("....."),
    list(".O.X."),
    list("XX.O."),
    list("OXOO."),
    list("OXXXO"),
]

def is_finished(board):
    """Return True if someone has four in a line or the board is full, else False."""
    empty = sum(row.count(".") for row in board)
    w = winner(board)
    if w == "X":
        return True
    if w == "O":
        return True
    if empty == 0:
        return True
    return False

def winner(board):
    """Return 'X' or 'O' if that player has four in a line, else None."""
    for r in range(5):
        for c in range(5):
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                end_r, end_c = r + 3 * dr, c + 3 * dc
                if 0 <= end_r < 5 and 0 <= end_c < 5:
                    cells = [board[r + k * dr][c + k * dc] for k in range(4)]
                    if cells[0] != "." and cells.count(cells[0]) == 4:
                        return cells[0]
    return None



def calculate_E(board):
    count = 0
    for i in range(5):
            for j in range(5):
                if board[i][j] == '.':
                    count += 1
    return count

def utility(winner, board):
    E = calculate_E(board)
    if winner == 'X':
        return 1+E
    elif winner == 'O':
        return -(1+E)
    return 0

def turn(board):
    x_turns = sum(row.count('X') for row in board)
    o_turns = sum(row.count('O') for row in board)

    if x_turns == o_turns:
        return True
    elif x_turns > o_turns:
        return False
    return True

def play_move(board, i):
    
    if turn(board) == True:
        move = 'X'
    else:
        move = 'O'

    new_board = copy.deepcopy(board)

    for row in range(4, -1, -1):
        if new_board[row][i] == '.':
            new_board[row][i] = move
            return new_board

nodes = 0
leaves = 0

def minimax(board):
    """Part A: full minimax to the end of the game, column order 0 to 4. Counts nodes and leaves in globals; returns the value."""
    global nodes, leaves
    nodes += 1
    if is_finished(board):
        leaves += 1
        return utility(winner(board), board)
    if turn(board) == True:
        maximum = float('-inf')
        for i in range(5):
            if board[0][i] == '.':
                child = play_move(board, i)
                maximum = max(maximum, minimax(child))
        return maximum
    else:
        minimum = float('inf')
        for i in range(5):
            if board[0][i] == '.':
                child = play_move(board, i)
                minimum = min(minimum, minimax(child))
        return minimum


def best_move(board):
    """Part A root (X to move): first column with a strictly better minimax value. Returns (value, column, nodes, leaves)."""
    global nodes, leaves
    nodes = 0
    leaves = 0
    nodes += 1                 
    best_value = float('-inf')
    best_col = None
    for i in range(5):
        if board[0][i] == '.':
            child = play_move(board, i)
            value = minimax(child)
            if value > best_value: 
                best_value = value
                best_col = i
    return best_value, best_col, nodes, leaves


def evaluate_board(board):
    """Sum over all 28 windows: +k^2 for k>=1 X and no O, -k^2 for k>=1 O and no X, else 0."""
    total = 0
    for r in range(5):
        for c in range(5):
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                end_r, end_c = r + 3 * dr, c + 3 * dc
                if 0 <= end_r < 5 and 0 <= end_c < 5:
                    cells = [board[r + k * dr][c + k * dc] for k in range(4)]
                    x = cells.count('X')
                    o = cells.count('O')
                    if x >= 1 and o == 0:
                        total += x * x
                    elif o >= 1 and x == 0:
                        total -= o * o
    return total


dl_nodes = 0

def depth_limited_minimax(board, depth):
    """Minimax cut off at depth 0, where unfinished positions return evaluate_board; finished games return utility * 1000."""
    global dl_nodes
    dl_nodes += 1
    if is_finished(board):
        return utility(winner(board), board) * 1000
    if depth == 0:
        return evaluate_board(board)
    if turn(board):
        value = float('-inf')
        for i in range(5):
            if board[0][i] == '.':
                value = max(value, depth_limited_minimax(play_move(board, i), depth - 1))
    else:
        value = float('inf')
        for i in range(5):
            if board[0][i] == '.':
                value = min(value, depth_limited_minimax(play_move(board, i), depth - 1))
    return value


def best_move_depth_limited(board, depth=4):
    """Root of the depth-limited search (root is X's turn). Returns (value, column, nodes)."""
    global dl_nodes
    dl_nodes = 1
    best_value = float('-inf')
    best_col = None
    for i in range(5):
        if board[0][i] == '.':
            value = depth_limited_minimax(play_move(board, i), depth - 1)
            if value > best_value:
                best_value = value
                best_col = i
    return best_value, best_col, dl_nodes

    





    

    


    



    



            
                


