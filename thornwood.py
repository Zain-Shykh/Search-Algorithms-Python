import random
import math



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




            
                


