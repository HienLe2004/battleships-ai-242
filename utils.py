import functools
import heapq

def is_in(elt, seq):
    return any(x is elt for x in seq)

def memoize(fn, slot=None, maxsize=32):
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)
    return memoized_fn

class PriorityQueue:
    def __init__(self, order="min", f=lambda x: x):
        self.heap = []
        if order == "min":
            self.f = f
        elif order == "max":
            self.f = lambda x: -f(x)
        else:
            raise ValueError("Order must be either 'min' or 'max'.")
    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))
    def extend(self, items):
        for item in items:
            self.append(item)
    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception("Trying to pop from empty PriorityQueue.")
    def __len__(self):
        return len(self.heap)
    def __contains__(self, key):
        return any([item == key for _, item in self.heap])
    def __getitem__(self, key):
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")
    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)