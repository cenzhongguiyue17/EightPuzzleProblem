from abc import ABCMeta, abstractmethod

import util
class SearchProblem(metaclass=ABCMeta):
    @abstractmethod
    def get_start_state(self):
        pass

    @abstractmethod
    def is_goal_state(self, state):
        pass

    @abstractmethod
    def get_successor(self, state):
        # return (next_state, action, cost)
        pass

    @abstractmethod
    def get_costs(self, actions):
        pass

    @abstractmethod
    def get_goal_state(self):
        pass


class Node:
    def __init__(self, state, path=[], priority=0):
        self.state = state
        self.path = path
        self.priority = priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __lt__(self, other):
        return self.priority < other.priority


def search(problem, fringe, calc_heuristic=None, heuristic=None):
    """
    This is an simple abstracted graph search algorithm. You could
    using different combination of fringe storage, calc_heuristic, heuristic
    to implement different search algorithm.

    For example:
    LIFO Queue(Stack), None, None -> Depth First Search
    FIFO Queue, None, None -> Breadth First Search
    PriorityQueue, cost compute function, None -> Uniform Cost Search

    In order to avoid infinite graph/tree problem we setup a list (visited) to
    avoid expanding the same node.

    hint: please check the node first before expanding:

    if node.state not in visited:
        visited.append(node.state)
    else:
        continue

    hint: you could get the successor by problem.get_successor method.

    hint: for fringe you may want to use
        fringe.pop  get a node from the fringe
        fringe.push   put a node into the fringe
        fringe.empty  check whether a fringe is empty or not. If the fringe is empty this function return True
        problem.is_goal_state check whether a state is the goal state
        problem.get_successor get all successor from current state
            return value: [(next_state, action, cost)]
    """
    start_state = problem.get_start_state()
    if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
        fringe.push(Node(start_state))
    else:
        fringe.push(Node(start_state), 0)
    visited = []
    step = 0
    while not fringe.empty():
        "*** YOUR CODE HERE ***"
        # TODO search
        node = fringe.pop()
        if problem.is_goal_state(node.state):
            return node.path, step
        visited.append(node.state)
        for item in problem.get_successor(node.state):
            curr = Node(item[0], [])
            curr.path = node.path.copy()
            curr.path.append(item[1])
            step = step + 1
            if curr.state not in visited:
                visited.append(curr.state)
                fringe.update(curr, ucs_compute_node_cost(problem, None, curr, None))
        "*** END YOUR CODE HERE ***"
    return [] # no paproblem.is_goal_state(problem.get_start_state()):th is found


def a_start_heuristic(problem, current_state):
    h = 0
    "*** YOUR CODE HERE ***"
    list = current_state.cells
    for i in range(len(list)):
        for j in range(len(list[i])):
            goal_row = int(list[i][j]/len(list))
            goal_column = list[i][j]%len(list[i])
            if i - goal_row > 0:
                h = h + i - goal_row
            else:
                h = h + 3 * (goal_row - i)
            if j - goal_column > 0:
                h = h + 0
            else:
                h = h + 10 * (goal_column - j)

    # TODO a_start_heuristic
    "*** END YOUR CODE HERE ***"
    return h


def a_start_cost(problem, successor, node, heuristic):
    cost = 0
    "*** YOUR CODE HERE ***"
    # TODO a_start_cost
    cost = problem.get_costs(node.path) + heuristic
    "*** END YOUR CODE HERE ***"
    return cost


def a_start_search(problem):
    path = []
    step = 0
    "*** YOUR CODE HERE ***"
    # TODO a_start_search
    open = util.PriorityQueue()
    close = []
    start_state = problem.get_start_state()
    start_node = Node(start_state, path)
    open.push(start_node, a_start_cost(problem, None, start_node, a_start_heuristic(problem, start_state)))
    while not open.empty():
        node = open.pop()
        if problem.is_goal_state(node.state):
            return node.path, step
        close.append(node.state)
        for item in problem.get_successor(node.state):
            curr = Node(item[0], [])
            curr.path = node.path.copy()
            curr.path.append(item[1])
            step = step + 1
            if curr.state not in close:
                close.append(curr.state)
                open.update(curr, a_start_cost(problem, None, curr, a_start_heuristic(problem, curr.state)))
    "*** END YOUR CODE HERE ***"
    return path, step


def ucs_compute_node_cost(problem, successor, node, heuristic):
    """
    Define the method to compute cost within unit cost search
    hint: successor = (next_state, action, cost).
    however the cost for current node should be accumulative
    problem and heuristic should not be used by this function
    """
    cost = 0
    "*** YOUR CODE HERE ***"
    # TODO ucs_compute_node_cost
    cost = problem.get_costs(node.path)
    "*** END YOUR CODE HERE ***"
    return cost


def uniform_cost_search(problem):
    """
    Search the solution with minimum cost.
    """
    #return search(problem, util.PriorityQueue(), ucs_compute_node_cost)
    return search(problem, util.PriorityQueue())

def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    hint: using util.Queue as the fringe
    """
    path = []
    step = 0
    "*** YOUR CODE HERE ***"
    # TODO a_start_search
    start_node = Node(problem.get_start_state(),path)
    if problem.is_goal_state(problem.get_start_state()):
        return start_node.path, step
    frontier = util.Queue()
    frontier.push(start_node)
    explored = []
    while True:
        if frontier.empty():
            return 'no such path'
        node = frontier.pop()
        explored.append(node.state)
        for item in problem.get_successor(node.state):
            curr = Node(item[0],[])
            #之前没用copy函数直接让一个list等于另一个list,才发现它们地址相同
            curr.path = node.path.copy()
            curr.path.append(item[1])
            step = step+1
            if curr.state not in explored:
                if problem.is_goal_state(curr.state):
                    return curr.path,step
                frontier.push(curr)

    "*** END YOUR CODE HERE ***"
    #return path, step


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.get_start_state()
    print "Is the start a goal?", problem.is_goal(problem.get_start_state())
    print "Start's successors:", problem.get_successors(problem.get_start_state())

    hint: using util.Stack as the fringe
    """
    path = []
    step = 0
    "*** YOUR CODE HERE ***"
    # TODO a_start_search
    explored = []
    start_node = Node(problem.get_start_state(), path)
    frontier = util.Stack()
    frontier.push(start_node)
    return recursive_dfs(problem, frontier, step, explored)
    """
    if problem.is_goal_state(problem.get_start_state()):
        return start_node.path, step
    frontier = util.Stack()
    frontier.push(start_node)
    explored = []
    while True:
        if frontier.empty():
            return 'no such path'
        node = frontier.pop()
        explored.append(node.state)
        for item in problem.get_successor(node.state):
            curr = Node(item[0], [])
            # 之前没用copy函数直接让一个list等于另一个list,才发现它们地址相同
            curr.path = node.path.copy()
            print(item[1])
            curr.path.append(item[1])
            step = step + 1
            if curr.state not in explored:
                if problem.is_goal_state(curr.state):
                    return curr.path, step
                frontier.push(curr)
    "*** END YOUR CODE HERE ***"
    #return path, step
    """
def recursive_dfs(problem, frontier, step, explored):
    node = frontier.pop()
    if  problem.is_goal_state(node.state):
        return node.path, step
    explored.append(node.state)
    for item in problem.get_successor(node.state):
        curr = Node(item[0], [])
        # 之前没用copy函数直接让一个list等于另一个list,才发现它们地址相同
        curr.path = node.path.copy()
        curr.path.append(item[1])
        step = step + 1
        if curr.state not in explored:
            if problem.is_goal_state(curr.state):
                return curr.path, step
            frontier.push(curr)
            recursive_dfs(problem, frontier, step, explored)
