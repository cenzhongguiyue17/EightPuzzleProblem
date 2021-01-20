from eightpuzzle import EightPuzzleState
from eightpuzzle import PuzzleSearchProblem
from search import Node
from search import ucs_compute_node_cost
import util
puzzle = EightPuzzleState([3, 0, 5, 6, 2, 4, 7, 8, 1])
problem = PuzzleSearchProblem(puzzle)
#print(problem.get_start_state())
#print(int(3/2))
pq = util.PriorityQueue()
state1 = EightPuzzleState([3, 0, 5, 6, 2, 4, 7, 8, 1])
state2 = EightPuzzleState([3, 0, 5, 6, 2, 4, 7, 8, 1])
state3 = EightPuzzleState([3, 1, 5, 6, 2, 4, 7, 8, 0])
node1 = Node(state1, ['left', 'down'])
node2 = Node(state2, ['right', 'up', 'right'])
node3 = Node(state3, ['down', 'down'])
pq.push(node1, ucs_compute_node_cost(problem, None, node1, None))
pq.push(node3, ucs_compute_node_cost(problem, None, node3, None))
print(ucs_compute_node_cost(problem, None, node1, None))
print(ucs_compute_node_cost(problem, None, node2, None))
print(ucs_compute_node_cost(problem, None, node3, None))
pq.update(node2, ucs_compute_node_cost(problem, None, node2, None))

while not pq.empty():
    print(pq.pop().state)