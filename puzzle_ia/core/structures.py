
class Stack:
    def __init__(self): self._a = []
    def push(self, x): self._a.append(x)
    def pop(self):
        if not self._a: raise IndexError("pop from empty Stack")
        return self._a.pop()
    def is_empty(self): return not self._a
    def __len__(self): return len(self._a)

class Queue:
    # Cola circular para O(1) amortizado
    def __init__(self, capacity=16):
        self._a = [None]*capacity; self._head = 0; self._tail = 0; self._size = 0
    def _grow(self):
        b = [None]*(len(self._a)*2)
        for i in range(self._size):
            b[i] = self._a[(self._head+i) % len(self._a)]
        self._a, self._head, self._tail = b, 0, self._size
    def enqueue(self, x):
        if self._size == len(self._a): self._grow()
        self._a[self._tail] = x
        self._tail = (self._tail+1) % len(self._a)
        self._size += 1
    def dequeue(self):
        if self._size == 0: raise IndexError("dequeue from empty Queue")
        x = self._a[self._head]; self._a[self._head] = None
        self._head = (self._head+1) % len(self._a)
        self._size -= 1
        return x
    def is_empty(self): return self._size == 0
    def __len__(self): return self._size

class MinHeap:
    # Montículo mínimo binario 1-indexed
    def __init__(self): self._a = [None]
    def __len__(self): return len(self._a)-1
    def is_empty(self): return len(self) == 0
    def push(self, x):
        self._a.append(x); self._sift_up(len(self))
    def pop(self):
        if self.is_empty(): raise IndexError("pop from empty heap")
        root = self._a[1]; last = self._a.pop()
        if not self.is_empty():
            self._a[1] = last; self._sift_down(1)
        return root
    def _sift_up(self, i):
        while i > 1:
            p = i//2
            if self._a[p] <= self._a[i]: break
            self._a[p], self._a[i] = self._a[i], self._a[p]; i = p
    def _sift_down(self, i):
        n = len(self)
        while 2*i <= n:
            l, r = 2*i, 2*i+1
            m = l if r > n or self._a[l] <= self._a[r] else r
            if self._a[i] <= self._a[m]: break
            self._a[i], self._a[m] = self._a[m], self._a[i]; i = m

class PriorityQueue:
    # Evita comparar objetos no ordenables con un tiebreaker
    def __init__(self): self._h = MinHeap(); self._t = 0
    def push(self, priority, item):
        self._t += 1
        self._h.push((priority, self._t, item))
    def pop(self):
        return self._h.pop()[2]
    def is_empty(self): return self._h.is_empty()
    def __len__(self): return len(self._h)


