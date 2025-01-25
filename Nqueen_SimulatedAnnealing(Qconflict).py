import random
import math
from matplotlib import pyplot as plt

class NQueenCSP: 
    def __init__(self, q_num): 
        # Initialize the N-Queens problem with the specified number of queens
        self.size = q_num
    
    def initial_assignment(self): 
        # Generates a random initial assignment of queens on the board
        return [random.randrange(self.size) for _ in range(self.size)]

    def next_assignment(self, assignment): 
        # Generates a new assignment by moving the queen with the most conflicts
        conflict_counts = [0] * self.size
        
        # Count conflicts for each queen
        for r in range(self.size):
            col = assignment[r]
            # Count row conflicts
            conflict_counts[col] += 1
            # Count diagonal conflicts
            for d in range(self.size):
                if d != r:
                    if assignment[d] == col:  # Same column conflict
                        conflict_counts[r] += 1
                    if abs(d - r) == abs(assignment[d] - col):  # Diagonal conflict
                        conflict_counts[r] += 1
        
        # Find the index of the queen with the most conflicts
        max_conflict_queen_index = max(range(self.size), key=lambda i: conflict_counts[i])
        
        # Create a new assignment
        next_assignment = assignment.copy()
        
        # Move the queen with the most conflicts to a new random position
        current_col = next_assignment[max_conflict_queen_index]
        new_col = current_col
        
        # Find a new column that is different from the current column
        while new_col == current_col:
            new_col = random.randrange(self.size)
        
        next_assignment[max_conflict_queen_index] = new_col
        return next_assignment
    
    def eval(self, assignment): 
        # Counts the number of conflicts in the current assignment
        conflict_num = 0
        row_conflicts = [0] * self.size
        diag1_conflicts = [0] * (2 * self.size - 1)  # Diagonal conflicts (r - c)
        diag2_conflicts = [0] * (2 * self.size - 1)  # Diagonal conflicts (r + c)
        
        # Count conflicts for each queen
        for r in range(self.size):
            col = assignment[r]
            row_conflicts[col] += 1
            diag1_conflicts[r - col + (self.size - 1)] += 1
            diag2_conflicts[r + col] += 1
        
        # Calculate total conflicts
        conflict_num += sum(count - 1 for count in row_conflicts if count > 1)
        conflict_num += sum(count - 1 for count in diag1_conflicts if count > 1)
        conflict_num += sum(count - 1 for count in diag2_conflicts if count > 1)
        
        return conflict_num

    def search(self, T, t):
        # Main simulated annealing algorithm
        current = self.initial_assignment()  # Start with a random assignment
        step = 0
        steps = []  # Track steps for plotting
        evals = []  # Track number of conflicts for plotting
        
        while T > 0: 
            steps.append(step)
            step += 1
            next_assignment = self.next_assignment(current)  # Generate a new assignment
            delta = self.eval(current) - self.eval(next_assignment)  # Evaluate change in conflicts
            
            # Decide to accept the new assignment based on simulated annealing criteria
            if delta > 0 or random.uniform(0, 1) < math.e**(delta / T): 
                current = next_assignment
            
            evals.append(self.eval(current))  # Record current conflicts
            T -= t  # Decrease temperature
        
        # Plot the number of conflicts over time
        plt.plot(steps, evals)
        plt.xlabel('Steps')
        plt.ylabel('Number of Conflicts')
        plt.title('Simulated Annealing for N-Queens Problem (Conflict-Based Assignment)')
        plt.show()
        
        final_conflicts = self.eval(current)  # Final evaluation of conflicts
        self.display_board(current)  # Display the final board configuration
        print("Final number of conflicts:", final_conflicts)  # Print final conflict count
        return current

    def display_board(self, assignment):
        # Visualizes the final board configuration
        board = [['.'] * self.size for _ in range(self.size)]  # Create an empty board
        for r in range(self.size):
            board[r][assignment[r]] = 'Q'  # Place queens on the board
        
        # Print the board row by row
        for row in board:
            print(' '.join(row))

# Example usage
a = NQueenCSP(20)  # Initialize the N-Queens problem with n queens
print(a.search(3.0, 0.00005))  # Execute the search and print the result