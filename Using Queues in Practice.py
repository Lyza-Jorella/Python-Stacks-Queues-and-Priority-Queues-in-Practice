>>> import networkx as nx
>>> print(nx.nx_agraph.read_dot("roadmap.dot"))
MultiGraph named 'Cities in the United Kingdom' with 70 nodes and 137 edges

>> > import networkx as nx
>> > graph = nx.nx_agraph.read_dot("roadmap.dot")
>> > graph.nodes["london"]
{'country': 'England',
 'latitude': '51.507222',
 'longitude': '-0.1275',
 'pos': '80,21!',
 'xlabel': 'City of London',
 'year': 0}

# graph.py

from typing import NamedTuple

class City(NamedTuple):
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, attrs):
        return cls(
            name=attrs["xlabel"],
            country=attrs["country"],
            year=int(attrs["year"]) or None,
            latitude=float(attrs["latitude"]),
            longitude=float(attrs["longitude"]),
        )

# graph.py

import networkx as nx

# ...

def load_graph(filename, node_factory):
    graph = nx.nx_agraph.read_dot(filename)
    nodes = {
        name: node_factory(attributes)
        for name, attributes in graph.nodes(data=True)
    }
    return nodes, nx.Graph(
        (nodes[name1], nodes[name2], weights)
        for name1, name2, weights in graph.edges(data=True)
    )

>>> from graph import City, load_graph

>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)

>>> nodes["london"]
City(
    name='City of London',
    country='England',
    year=None,
    latitude=51.507222,
    longitude=-0.1275
)

>>> print(graph)
Graph with 70 nodes and 137 edges

>> > for neighbor in graph.neighbors(nodes["london"]):
    ...
    print(neighbor.name)
...
Bath
Brighton & Hove
Bristol
Cambridge
Canterbury
Chelmsford
Coventry
Oxford
Peterborough
Portsmouth
Southampton
Southend - on - Sea
St
Albans
Westminster
Winchester

>>> for neighbor, weights in graph[nodes["london"]].items():
...     print(weights["distance"], neighbor.name)
...
115 Bath
53 Brighton & Hove
118 Bristol
61 Cambridge
62 Canterbury
40 Chelmsford
100 Coventry
58 Oxford
85 Peterborough
75 Portsmouth
79 Southampton
42 Southend-on-Sea
25 St Albans
1 Westminster
68 Winchester

>>> def sort_by(neighbors, strategy):
...     return sorted(neighbors.items(), key=lambda item: strategy(item[1]))
...
>>> def by_distance(weights):
...     return float(weights["distance"])
...
>>> for neighbor, weights in sort_by(graph[nodes["london"]], by_distance):
...     print(f"{weights['distance']:>3} miles, {neighbor.name}")
...
  1 miles, Westminster
 25 miles, St Albans
 40 miles, Chelmsford
 42 miles, Southend-on-Sea
 53 miles, Brighton & Hove
 58 miles, Oxford
 61 miles, Cambridge
 62 miles, Canterbury
 68 miles, Winchester
 75 miles, Portsmouth
 79 miles, Southampton
 85 miles, Peterborough
100 miles, Coventry
115 miles, Bath
118 miles, Bristol

>>> import networkx as nx
>>> from graph import City, load_graph

>>> def is_twentieth_century(year):
...     return year and 1901 <= year <= 2000
...
>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)
>>> for node in nx.bfs_tree(graph, nodes["edinburgh"]):
...     print("📍", node.name)
...     if is_twentieth_century(node.year):
...         print("Found:", node.name, node.year)
...         break
... else:
...     print("Not found")
...
📍 Edinburgh
📍 Dundee
📍 Glasgow
📍 Perth
📍 Stirling
📍 Carlisle
📍 Newcastle upon Tyne
📍 Aberdeen
📍 Inverness
📍 Lancaster
Found: Lancaster 1937

>>> def order(neighbors):
...     def by_latitude(city):
...         return city.latitude
...     return iter(sorted(neighbors, key=by_latitude, reverse=True))

>>> for node in nx.bfs_tree(graph, nodes["edinburgh"], sort_neighbors=order):
...     print("📍", node.name)
...     if is_twentieth_century(node.year):
...         print("Found:", node.name, node.year)
...         break
... else:
...     print("Not found")
...
📍 Edinburgh
📍 Dundee
📍 Perth
📍 Stirling
📍 Glasgow
📍 Newcastle upon Tyne
📍 Carlisle
📍 Aberdeen
📍 Inverness
📍 Sunderland
Found: Sunderland 1992

# graph.py

from queues import Queue

# ...

def breadth_first_traverse(graph, source):
    queue = Queue(source)
    visited = {source}
    while queue:
        yield (node := queue.dequeue())
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

def breadth_first_search(graph, source, predicate):
    for node in breadth_first_traverse(graph, source):
        if predicate(node):
            return node

def breadth_first_traverse(graph, source):
    queue = Queue(source)
    visited = {source}
    for node in queue:
        yield node
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

>>> from graph import (
...     City,
...     load_graph,
...     breadth_first_traverse,
...     breadth_first_search as bfs,
... )

>>> def is_twentieth_century(city):
...     return city.year and 1901 <= city.year <= 2000

>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)
>>> city = bfs(graph, nodes["edinburgh"], is_twentieth_century)
>>> city.name
'Lancaster'

>>> for city in breadth_first_traverse(graph, nodes["edinburgh"]):
...     print(city.name)
...
Edinburgh
Dundee
Glasgow
Perth
Stirling
Carlisle
Newcastle upon Tyne
Aberdeen
Inverness
Lancaster
⋮

>>> import networkx as nx
>>> from graph import City, load_graph

>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)

>>> city1 = nodes["aberdeen"]
>>> city2 = nodes["perth"]

>>> for i, path in enumerate(nx.all_shortest_paths(graph, city1, city2), 1):
...     print(f"{i}.", " → ".join(city.name for city in path))
...
1. Aberdeen → Dundee → Perth
2. Aberdeen → Inverness → Perth

# graph.py

# ...

def shortest_path(graph, source, destination, order_by=None):
    queue = Queue(source)
    visited = {source}
    previous = {}
    while queue:
        node = queue.dequeue()
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                previous[neighbor] = node
                if neighbor == destination:
                    return retrace(previous, source, destination)

# graph.py

from collections import deque

# ...

def retrace(previous, source, destination):
    path = deque()

    current = destination
    while current != source:
        path.appendleft(current)
        current = previous.get(current)
        if current is None:
            return None

    path.appendleft(source)
    return list(path)

>>> from graph import shortest_path

>>> " → ".join(city.name for city in shortest_path(graph, city1, city2))
'Aberdeen → Dundee → Perth'

>>> def by_latitude(city):
...     return -city.latitude
...
>>> " → ".join(
...     city.name
...     for city in shortest_path(graph, city1, city2, by_latitude)
... )
'Aberdeen → Inverness → Perth'

# graph.py

# ...

def connected(graph, source, destination):
    return shortest_path(graph, source, destination) is not None

>>> from graph import connected
>>> connected(graph, nodes["belfast"], nodes["glasgow"])
False
>>> connected(graph, nodes["belfast"], nodes["derry"])
True

>>> import networkx as nx
>>> from graph import City, load_graph

>>> def is_twentieth_century(year):
...     return year and 1901 <= year <= 2000
...
>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)
>>> for node in nx.dfs_tree(graph, nodes["edinburgh"]):
...     print("📍", node.name)
...     if is_twentieth_century(node.year):
...         print("Found:", node.name, node.year)
...         break
... else:
...     print("Not found")
...
📍 Edinburgh
📍 Dundee
📍 Aberdeen
📍 Inverness
📍 Perth
📍 Stirling
📍 Glasgow
📍 Carlisle
📍 Lancaster
Found: Lancaster 1937

# graph.py

from queues import Queue, Stack

# ...

def depth_first_traverse(graph, source, order_by=None):
    stack = Stack(source)
    visited = set()
    while stack:
        if (node := stack.dequeue()) not in visited:
            yield node
            visited.add(node)
            neighbors = list(graph.neighbors(node))
            if order_by:
                neighbors.sort(key=order_by)
            for neighbor in reversed(neighbors):
                stack.enqueue(neighbor)

# graph.py

# ...

def recursive_depth_first_traverse(graph, source, order_by=None):
    visited = set()

    def visit(node):
        yield node
        visited.add(node)
        neighbors = list(graph.neighbors(node))
        if order_by:
            neighbors.sort(key=order_by)
        for neighbor in neighbors:
            if neighbor not in visited:
                yield from visit(neighbor)

    return visit(source)

# graph.py

# ...

def breadth_first_search(graph, source, predicate, order_by=None):
    return search(breadth_first_traverse, graph, source, predicate, order_by)

# ...

def depth_first_search(graph, source, predicate, order_by=None):
    return search(depth_first_traverse, graph, source, predicate, order_by)

def search(traverse, graph, source, predicate, order_by=None):
    for node in traverse(graph, source, order_by):
        if predicate(node):
            return node

>>> from graph import (
...     City,
...     load_graph,
...     depth_first_traverse,
...     depth_first_search as dfs,
... )

>>> def is_twentieth_century(city):
...     return city.year and 1901 <= city.year <= 2000
...
>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)
>>> city = dfs(graph, nodes["edinburgh"], is_twentieth_century)
>>> city.name
'Lancaster'

>>> for city in depth_first_traverse(graph, nodes["edinburgh"]):
...     print(city.name)
...
Edinburgh
Dundee
Aberdeen
Inverness
Perth
Stirling
Glasgow
Carlisle
Lancaster
⋮

# graph.py

from math import inf as infinity
from queues import MutableMinHeap, Queue, Stack

# ...

def dijkstra_shortest_path(graph, source, destination, weight_factory):
    previous = {}
    visited = set()

    unvisited = MutableMinHeap()
    for node in graph.nodes:
        unvisited[node] = infinity
    unvisited[source] = 0

    while unvisited:
        visited.add(node := unvisited.dequeue())
        for neighbor, weights in graph[node].items():
            if neighbor not in visited:
                weight = weight_factory(weights)
                new_distance = unvisited[node] + weight
                if new_distance < unvisited[neighbor]:
                    unvisited[neighbor] = new_distance
                    previous[neighbor] = node

    return retrace(previous, source, destination)

>>> import networkx as nx
>>> from graph import City, load_graph, dijkstra_shortest_path

>>> nodes, graph = load_graph("roadmap.dot", City.from_dict)

>>> city1 = nodes["london"]
>>> city2 = nodes["edinburgh"]

>>> def distance(weights):
...     return float(weights["distance"])
...
>>> for city in dijkstra_shortest_path(graph, city1, city2, distance):
...     print(city.name)
...
City of London
St Albans
Coventry
Birmingham
Stoke-on-Trent
Manchester
Salford
Preston
Lancaster
Carlisle
Edinburgh

>>> def weight(node1, node2, weights):
...     return distance(weights)
...
>>> for city in nx.dijkstra_path(graph, city1, city2, weight):
...     print(city.name)
...
City of London
St Albans
Coventry
Birmingham
Stoke-on-Trent
Manchester
Salford
Preston
Lancaster
Carlisle
Edinburgh