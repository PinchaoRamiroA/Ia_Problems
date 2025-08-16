class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Devuelve lista de acciones posibles desde el estado."""
        raise NotImplementedError

    def result(self, state, action):
        """Devuelve el nuevo estado aplicando la acción."""
        raise NotImplementedError

    def is_goal(self, state):
        """Verifica si es estado objetivo."""
        return state == self.goal

    def cost(self, state1, action, state2):
        """Devuelve el costo de pasar de state1 a state2."""
        return 1  # por defecto, costo uniforme


class EightPuzzle(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def actions(self, state):
        pass  # TODO: mover el hueco (0) arriba/abajo/izq/der si se puede

    def result(self, state, action):
        pass  # TODO: intercambiar 0 con vecino

    def is_goal(self, state):
        return state == self.goal
