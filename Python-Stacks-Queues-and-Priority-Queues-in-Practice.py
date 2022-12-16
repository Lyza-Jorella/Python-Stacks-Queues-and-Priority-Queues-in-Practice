# queues.py

from collections import deque

class Queue:
    def __init__(self):
        self._elements = deque()

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()

>>> from queues import Queue

>>> fifo = Queue()
>>> fifo.enqueue("1st")
>>> fifo.enqueue("2nd")
>>> fifo.enqueue("3rd")

>>> fifo.dequeue()
'1st'
>>> fifo.dequeue()
'2nd'
>>> fifo.dequeue()
'3rd'

# queues.py

from collections import deque

class Queue:
    def __init__(self, *elements):
        self._elements = deque(elements)

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

    def enqueue(self, element):
        self._elements.append(element)

    def dequeue(self):
        return self._elements.popleft()

>>> from queues import Queue

>>> fifo = Queue("1st", "2nd", "3rd")
>>> len(fifo)
3

>>> for element in fifo:
...     print(element)
...
1st
2nd
3rd

>>> len(fifo)
0

# queues.py

# ...

class Stack(Queue):
    def dequeue(self):
        return self._elements.pop()

>>> from queues import Stack

>>> lifo = Stack("1st", "2nd", "3rd")
>>> for element in lifo:
...     print(element)
...
3rd
2nd
1st

>>> lifo = []

>>> lifo.append("1st")
>>> lifo.append("2nd")
>>> lifo.append("3rd")

>>> lifo.pop()
'3rd'
>>> lifo.pop()
'2nd'
>>> lifo.pop()
'1st'

>>> from heapq import heappush

>>> fruits = []
>>> heappush(fruits, "orange")
>>> heappush(fruits, "apple")
>>> heappush(fruits, "banana")

>>> fruits
['apple', 'orange', 'banana']

>>> from heapq import heappop

>>> heappop(fruits)
'apple'

>>> fruits
['banana', 'orange']





