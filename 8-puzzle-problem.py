import heapq

class PuzzleState:
    def __init__(self, board, zero_pos, moves, previous=None):
        self.board = board  # Current board configuration
        self.zero_pos = zero_pos  # Position of the blank tile
        self.moves = moves  # Number of moves taken to reach this state
        self.previous = previous  # Reference to the previous state for path reconstruction

    def get_possible_moves(self):

        x, y = self.zero_pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left
        possible_moves = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:  # Stay within bounds
                new_board = [row[:] for row in self.board]  # Copy current board
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                possible_moves.append((new_board, (new_x, new_y)))  # Add new state

        return possible_moves

    def __lt__(self, other):
        """Define less than for priority queue (based on total cost)."""
        return self.moves + self.dynamic_heuristic() < other.moves + other.dynamic_heuristic()

    def manhattan_distance(self):
        distance = 0
        goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2), 
                          4: (1, 0), 5: (1, 1), 6: (1, 2),
                          7: (2, 0), 8: (2, 1)}

        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value != 0:  # Ignore the blank tile
                    goal_x, goal_y = goal_positions[value]
                    distance += abs(goal_x - i) + abs(goal_y - j)

        return distance

    def linear_conflict(self):
        conflict = 0
        goal_positions = {1: (0, 0), 2: (0, 1), 3: (0, 2), 
                          4: (1, 0), 5: (1, 1), 6: (1, 2),
                          7: (2, 0), 8: (2, 1)}

        # Check rows for linear conflicts
        for i in range(3):
            row_values = [self.board[i][j] for j in range(3) if self.board[i][j] != 0]
            for j in range(len(row_values)):
                for k in range(j + 1, len(row_values)):
                    if goal_positions[row_values[j]][0] == goal_positions[row_values[k]][0] == i:
                        if goal_positions[row_values[j]][1] > goal_positions[row_values[k]][1]:
                            conflict += 2  # Each conflict adds 2 to the heuristic

        # Check columns for linear conflicts
        for j in range(3):
            col_values = [self.board[i][j] for i in range(3) if self.board[i][j] != 0]
            for j1 in range(len(col_values)):
                for j2 in range(j1 + 1, len(col_values)):
                    if goal_positions[col_values[j1]][1] == goal_positions[col_values[j2]][1] == j:
                        if goal_positions[col_values[j1]][0] > goal_positions[col_values[j2]][0]:
                            conflict += 2  # Each conflict adds 2 to the heuristic

        return conflict

    def dynamic_heuristic(self):
        """Calculate the heuristic as the larger of Manhattan distance and linear conflict."""
        return max(self.manhattan_distance(), self.linear_conflict())

def is_goal_state(board):
    """Check if the current board is the goal state."""
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Standard goal configuration
    return board == goal

def a_star(initial_state):
    """Perform A* search to solve the 8-puzzle and return the path."""
    open_set = []
    heapq.heappush(open_set, initial_state)  # Use a priority queue for the open set
    closed_set = set()  # Set to keep track of visited states

    while open_set:
        current_state = heapq.heappop(open_set)  # Get the state with the lowest f value


        if is_goal_state(current_state.board):
            return reconstruct_path(current_state)  # Return the path if goal state is found

        closed_set.add(tuple(tuple(row) for row in current_state.board))  # Add current state to closed set

        for new_board, new_zero_pos in current_state.get_possible_moves():
            new_state = PuzzleState(new_board, new_zero_pos, current_state.moves + 1, current_state)  # Create new state

            state_tuple = tuple(tuple(row) for row in new_state.board)  # Create a tuple for the state

            if state_tuple in closed_set:
                continue  # Skip already visited states

            # Add the new state to the open set if not already present
            if new_state not in open_set:
                heapq.heappush(open_set, new_state)

    return None  # No solution found

def reconstruct_path(state):
    """Reconstruct the path from the initial state to the goal state."""
    path = []
    while state:
        path.append(state.board)
        state = state.previous  # Move to the previous state
    return path[::-1]  # Reverse the path to show from start to goal

# Example usage
initial_board = [[2, 1, 3],
                 [7, 4, 5],
                 [6, 0, 8]]

# Find the position of the blank tile (0)
zero_pos = next((i, j) for i in range(3) for j in range(3) if initial_board[i][j] == 0)
initial_state = PuzzleState(initial_board, zero_pos, 0)  # Create initial state

# Execute A* search
solution_path = a_star(initial_state)

if solution_path:
    print("Solution path:")
    for step in solution_path:
        for row in step:
            print(row)
        print()  # Print a blank line for better readability
else:
    print('No solution exists.')