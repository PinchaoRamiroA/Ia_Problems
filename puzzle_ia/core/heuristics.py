from core.problem import PuzzleState, GOAL, GOAL_POS

def misplaced(s: PuzzleState) -> int:
    return sum(1 for i,v in enumerate(s.tiles) if v != 0 and v != GOAL[i])

def manhattan(s: PuzzleState) -> int:
    dist = 0
    for i,v in enumerate(s.tiles):
        if v == 0: continue
        gi = GOAL_POS[v]
        x1,y1 = divmod(i,3); x2,y2 = divmod(gi,3)
        dist += abs(x1-x2) + abs(y1-y2)
    return dist

def linear_conflict(s: PuzzleState):
    # Primero, calculamos la distancia Manhattan
    dist = manhattan(s)

    # Ahora sumamos conflictos lineales
    conflicts = 0

    # Revisa filas
    for row in range(3):
        row_tiles = [s.tiles[row * 3 + col] for col in range(3)]
        for i in range(3):
            for j in range(i + 1, 3):
                a, b = row_tiles[i], row_tiles[j]
                if a != 0 and b != 0:
                    ga, gb = GOAL_POS[a], GOAL_POS[b]
                    # Ambos deben estar en esta fila en el estado meta
                    if ga // 3 == row and gb // 3 == row:
                        # Conflicto si están en orden invertido
                        if ga > gb:
                            conflicts += 1

    # Revisa columnas
    for col in range(3):
        col_tiles = [s.tiles[row * 3 + col] for row in range(3)]
        for i in range(3):
            for j in range(i + 1, 3):
                a, b = col_tiles[i], col_tiles[j]
                if a != 0 and b != 0:
                    ga, gb = GOAL_POS[a], GOAL_POS[b]
                    if ga % 3 == col and gb % 3 == col:
                        if ga > gb:
                            conflicts += 1

    return dist + 2 * conflicts

