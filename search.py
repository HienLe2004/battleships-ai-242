from collections import deque
from utils import *
class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        return [
            self.child_node(problem, action) for action in problem.actions(self.state)
        ]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(
            next_state,
            self,
            action,
            problem.path_cost(self.path_cost, self.state, action, next_state),
        )
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

def breadth_first_tree_search(problem):
    frontier = deque([Node(problem.initial)])
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def depth_first_tree_search(problem):
    frontier = [Node(problem.initial)]
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def best_first_graph_search(problem, f, display=False):
    f = memoize(f, "f")
    node = Node(problem.initial)
    frontier = PriorityQueue("min", f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(
                    len(explored),
                    "paths have been expanded and",
                    len(frontier),
                    "paths remain in the frontier",
                )
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search(problem, h=None, display=False):
    h = memoize(h or problem.h, "h")
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
