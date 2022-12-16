# queues.py

# ...

class IterableMixin:
    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

class Queue(IterableMixin):
    # ...

class Stack(Queue):
    # ...

class PriorityQueue(IterableMixin):
    # ...