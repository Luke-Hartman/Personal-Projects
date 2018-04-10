package simple;

import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

class Link {
	// All the cells contained in this row/column/box
	List<Cell> cells;
	// count[k] is the number of possibile locations n = k + 1 could have within
	// this link
	int[] count;
	// visited[k] is true if remove(k) has been called on this link
	boolean[] visited;
	// used for undoing wrong guesses
	Stack<Stack<Undo>> undoStack;
	
	Link(int L, Stack<Stack<Undo>> undoStack) {
		cells = new ArrayList<Cell>(L);
		count = new int[L];
		for(int a = 0; a < L; a++) {
			count[a] = L;
		}
		visited = new boolean[L];
		this.undoStack = undoStack;
	}
	
	// Called when the value of a cell in this link is known to be true
	void remove(Cell cell, int k) throws InvalidBoardException {
		undoStack.peek().add(new UndoLinkRemove(this, k));
		visited[k] = true;
		// It is now known that no other cell in this link is n = k + 1
		for(Cell other: cells) {
			if(other != cell && !other.visited[k]) {
				other.remove(k);
			}
		}
	}
	
	// Called when a value of a cell in this link is known to be false
	void decrement(int k) throws InvalidBoardException {
		undoStack.peek().add(new UndoDecrement(this, k));
		// If there is only one possibility for this link
		if(--count[k] == 1) {
			for(Cell cell: cells) {
				if(cell.selection[k] && !cell.added) {
					cell.add(k);
				}
			}
		}
	}
}
