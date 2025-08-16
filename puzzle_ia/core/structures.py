class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop()

    def is_empty(self):
        return len(self.data) == 0


class Queue:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.insert(0, item)

    def pop(self):
        return self.data.pop()

    def is_empty(self):
        return len(self.data) == 0


class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, item):
        """Insertar respetando propiedad de heap (usar sift-up)."""
        pass

    def pop(self):
        """Extraer mínimo y reordenar heap (usar sift-down)."""
        pass

    def is_empty(self):
        return len(self.data) == 0
