package simple;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

class Cell {
	// Length of board
	final int L;
	// Length of a square
	final int S;
	// Area of board (number of cells)
	final int A;
	// row index
	int i;
	// column index
	int j;
	// array of length L, one for each value of possible for cell
	// selection[k] is true if the value n = k + 1 might be valid at this spot
	boolean[] selection;
	// number of trues in selection
	int variety;
	// the row, column and box containing this cell
	List<Link> links;
	// visited[k] is true if this cell has had remove(k) already called on it
	boolean[] visited;
	// same as visited[k] but for add(k);
	boolean added;
	// what the value for this cell wil be. Starts at 1; 0 means unknown.
	int value;
	// Used for undoing wrong guesses
	Stack<Stack<Undo>> undoStack;
	
	Cell(int i, int j, int S, Stack<Stack<Undo>> undoStack) {
		this.S = S;
		this.L = S * S;
		this.A = L * L;
		this.i = i;
		this.j = j;
		selection = new boolean[L];
		for(int a = 0; a < L; a++) {
			selection[a] = true;
		}
		variety = L;
		links = new ArrayList<Link>(3); // There will always be a row, col and
										// box
		visited = new boolean[L];
		added = false;
		value = 0;
		this.undoStack = undoStack;
	}
	
	// Called when a value for this cell is known to be true
	void add(int k) throws InvalidBoardException {
		undoStack.peek().add(new UndoAdd(this));
		added = true;
		value = k + 1;
		// This cell cannot be any other value
		for(int a = 0; a < L; a++) {
			if(selection[a] && a != k && !visited[a]) {
				remove(a);
			}
		}
		// No other cell linked to this cell can be n = k + 1
		for(Link link: links) {
			if(!link.visited[k]) {
				link.remove(this, k);
			}
		}
	}
	
	// Called when a value for this cell is known to be false
	void remove(int k) throws InvalidBoardException {
		undoStack.peek().add(new UndoCellRemove(this, k));
		visited[k] = true;
		selection[k] = false;
		// If there is only one possibility for this cell
		if(--variety == 1 && !added) {
			for(int a = 0; a < L; a++) {
				if(selection[a]) {
					add(a);
				}
			}
		}
		else if(variety == 0) {
			throw new InvalidBoardException();
		}
		// Inform the links
		for(Link link: links) {
			link.decrement(k);
		}
	}
}
