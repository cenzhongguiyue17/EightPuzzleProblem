from eightpuzzle import EightPuzzleState
from search import a_start_heuristic
puzzle = EightPuzzleState([3, 0, 5, 6, 2, 4, 7, 8, 1])
h = a_start_heuristic(None, puzzle)
print(h)