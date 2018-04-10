package improved;

import java.util.EmptyStackException;
import java.util.Stack;
import general.SampleBoards;

/* Updates:
 * 
 * Expanded upon Link.decrement method.
 * Now able to figure out of how to remove more when all of the viable options
 * in one link also belong to another link
 * 
 * 
 */

public class Board {
	final int L; // Length of board
	final int S; // Scale
	final int A; // Area
	// Base board which is trying to be solved
	int[][] start;
	// 2D array of Cells in the same dimensions as start
	Cell[][] board;
	// Used for undoing wrong guesses
	Stack<Stack<Undo>> undoStack;
	// Keeps track of guesses to do
	Stack<Stack<Guess>> guessStack;
	
	// The following four methods correspond to traversals over the board
	// type 1 is row-wise, 2 is column-wise, 3 is box-wise
	int i(int a) {
		return i(a, 1);
	}
	
	int i(int a, int type) {
		switch (type) {
			case 1:
				return a / L;
			case 2:
				return a % L;
			case 3:
				return a % L / S + a / L / S * S;
		}
		return -1;
	}
	
	int j(int a) {
		return j(a, 1);
	}
	
	int j(int a, int type) {
		switch (type) {
			case 1:
				return a % L;
			case 2:
				return a / L;
			case 3:
				return a % S + a / L % S * S;
		}
		return -1;
	}
	
	public Board(int[][] sudoku) {
		L = sudoku.length;
		S = (int) Math.sqrt(L);
		A = L * L;
		
		start = sudoku;
		board = new Cell[L][L];
		// Make stacks
		undoStack = new Stack<Stack<Undo>>();
		undoStack.add(new Stack<Undo>());
		guessStack = new Stack<Stack<Guess>>();
		// Make cells
		for(int a = 0; a < A; a++) {
			int i = i(a);
			int j = j(a);
			board[i][j] = new Cell(i, j, S, undoStack);
		}
		// Make links
		for(int type = 1; type <= 3; type++) {
			for(int a = 0; a < A; a += L) {
				Link link = new Link(S, undoStack);
				for(int b = 0; b < L; b++) {
					Cell cell = board[i(a + b, type)][j(a + b, type)];
					cell.links.add(link);
					link.cells.add(cell);
				}
			}
		}
	}
	
	public static void main(String[] args) throws InvalidBoardException {
		System.out.println("v2");
		long t = System.currentTimeMillis();
		Board b = new Board(SampleBoards.Impossible);
		b.solve();
		System.out.println(toString(b.gatherValues()));
		System.out.println((System.currentTimeMillis() - t) / 1000.0);
	}
	
	// Solves the board
	public boolean solve() throws InvalidBoardException {
		// First add all of the known values
		for(int a = 0; a < A; a++) {
			int i = i(a);
			int j = j(a);
			int n = start[i][j];
			if(n != 0) {
				board[i][j].add(n - 1);
			}
		}
		// Throw away first undoStack since the above is certain
		undoStack.pop();
		// Add guesses to guessStack
		if(addGuesses()) {
			return true;
		}
		// Now to the guessing process
		while(guessStack.size() > 0) {
			// Get an undoStack ready
			undoStack.add(new Stack<Undo>());
			// Do a guess
			boolean caught = false;
			try {
				guessStack.peek().pop().guess();
			}
			// If this guess was found to be wrong
			catch(InvalidBoardException e) {
				caught = true;
				// Recurse backwards to the next guess
				try {
					undoStack();
					while(guessStack.peek().size() == 0) {
						guessStack.pop();
						undoStack();
					}
				}
				catch(EmptyStackException e2) {
					throw e;
				}
			}
			// Notice addGuesses() is called if the board is not filled or known
			// to be invalid
			if(!caught && addGuesses()) {
				return true;
			}
		}
		return false;
	}
	
	// Returns true if the board is finished
	boolean addGuesses() {
		// First find the cell with the highest variety
		Cell max = null;
		for(int a = 0; a < A; a++) {
			Cell cell = board[i(a)][j(a)];
			if(max == null || cell.variety > max.variety) {
				max = cell;
			}
		}
		if(max.variety == 1) {
			return true;
		}
		// Add the possible values for it to guessStack
		Stack<Guess> newGuesses = new Stack<Guess>();
		for(int k = L - 1; k >= 0; k--) {
			if(max.selection[k]) {
				newGuesses.add(new Guess(max, k));
			}
		}
		guessStack.add(newGuesses);
		return false;
	}
	
	// Undoes the results of a guess
	void undoStack() {
		Stack<Undo> stack = undoStack.pop();
		while(stack.size() > 0) {
			stack.pop().undo();
		}
	}
	
	// Gets the values of the Sudoku board from the cells
	int[][] gatherValues() {
		int[][] m = new int[L][L];
		for(int a = 0; a < A; a++) {
			int i = i(a);
			int j = j(a);
			m[i][j] = board[i][j].value;
		}
		return m;
	}
	
	void debug() {
		System.out.println(toString(gatherValues()));
		// This just prints stuff for debuging/ Incremental programming.
		for(int k = 0; k < L; k++) {
			int n = k + 1;
			int[][] printPossible = new int[L][L];
			for(int i = 0; i < L; i++) {
				for(int j = 0; j < L; j++) {
					if(!board[i][j].visited[k]) {
						printPossible[i][j] = n;
					}
				}
			}
			System.out.println(toString(printPossible));
		}
	}
	
	static String toString(int[][] matrix) {
		final int L = matrix.length;
		final int S = (int) Math.sqrt(L);
		String s = "[";
		for(int i = 0; i < L; i++) {
			s += "[";
			for(int j = 0; j < L; j++) {
				s += matrix[i][j];
				if(j < L - 1) {
					s += ",";
					if((j + 1) % S == 0) {
						s += " ";
					}
				}
			}
			s += "]";
			if(i < L - 1) {
				s += ",\n ";
				if((i + 1) % S == 0) {
					s += "\n ";
				}
			}
		}
		s += "]\n\n";
		return s;
	}
}
