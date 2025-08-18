import random

# Verificar si el estado es resoluble
def validate_state(puzzle):
    inv_count = 0
    tiles = [x for x in puzzle if x != 0]
    for i in range(len(tiles)):
        for j in range(i+1, len(tiles)):
            if tiles[i] > tiles[j]:
                inv_count += 1
    return inv_count % 2 == 0

# Crear un estado aleatorio resoluble
def create_state():
    while True:
        state = list(range(9))
        random.shuffle(state)
        state = tuple(state)
        if validate_state(state):
            return state