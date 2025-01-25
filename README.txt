
At this project we're looking for a solution for a famous CSP problem!(N-Queen)
	Using three different method on the Simulated Annealing algorithm which are:
	
		1Q: This solution would randomize the location of n queens on the board
		    at first and will change the place of one queen and making the neighbors
		    of our initial board. (place changing are also random)
		    
		2Q: This solution would randomize the location of n queens on the board
		at first and will change the place of a tuple of queens for the next board
		and finding the neighbors of our initial board. (place changings are also random)
		
		Qconflict: This solution would randomize the location of n queens on the board
		for the initial state but not like the two previous methods, in this solution 
		we decide to change the queens based on their conflicts, and reach the neighbors
		of our initial state. (place changing is not random)
		
	
	As it has been shown in figures, each method has its advantages and disadvantages
	
		1Q & 2Q: These two method have approximately the same running time,(faster)
			  and based on the random places of the initial state and 2Q method 
			  may stuck in 1 conflict beacuse of changing two queens and it might 
			  never reach zero, but takes less changing steps in the whole board state 
			  of the queens
			  
		Qconflict: This method has an advantage over the previous two methods and that is 
			   the fall of the conflicts. at first by two or three steps, this method 
			   would give you something that may the previous methods would give you after 
			   3000 steps, it's a lot faster to find a non-accurate answer, but it's precise!
			   
			   
As you wish to analyze the differences we have put a history diagram of each method for you!
