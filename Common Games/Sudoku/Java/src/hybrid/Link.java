package hybrid;

import java.util.ArrayList;
import java.util.List;
import general.InvalidBoardException;

class Link {
	final int S;
	final int L;
	final int A;
	// All the cells contained in this row/column/box
	List<Cell> cells;
	// count[k] is the number of possibile locations n = k + 1 could have within
	// this link
	int[] count;
	// visited[k] is true if remove(k) has been called on this link
	boolean[] visited;
	// used for when advanced decrement logic is successful and can be skipped
	boolean[] success;
	
	Link(int S) {
		this.S = S;
		this.L = S * S;
		this.A = L * L;
		cells = new ArrayList<Cell>(L);
		count = new int[L];
		for(int a = 0; a < L; a++) {
			count[a] = L;
		}
		visited = new boolean[L];
		success = new boolean[L];
	}
	
	// Called when the value of a cell in this link is known to be true
	void remove(Cell cell, int k) throws InvalidBoardException {
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
		// If there is only one possibility for this link
		if(--count[k] == 1) {
			for(Cell cell: cells) {
				if(cell.selection[k] && !cell.added) {
					cell.add(k);
				}
			}
		}
		else if(count[k] == 0) {
			throw new InvalidBoardException();
		}
		// Advanced remove. Allows more options to be removed when all of the
		// viable options for a value in one link also belong to another.
		else if(count[k] <= S && !success[k]) { // Only bother if it is possible
			// for them to all share a link
			int hits = 1;
			Link strongestLink = null;
			// If this was a row, there are 3 boxes and 3 rows.
			List<Link> links = new ArrayList<Link>(6);
			boolean finished = false;
			// Look at all of the cells in this link which may have n = k + 1
			for(Cell cell: cells) {
				if(!cell.selection[k]) {
					continue;
				}
				// Look at all of the links in these other cells
				for(Link link: cell.links) {
					// Skip if it is the same link, or progress cannot be made
					if(this == link || link.count[k] <= count[k]) {
						continue;
					}
					// If this link is just strongestLink, you hit it again
					else if(link == strongestLink) {
						hits++;
					}
					else if(links.contains(link)) {
						// If this is the first link to be found twice
						if(hits == 1) {
							strongestLink = link;
							hits++;
						}
						// Else there were two links they are spread between
						else {
							finished = true;
							break;
						}
					}
					// If this link was just found for the first time
					else {
						links.add(link);
					}
					// Early exit
					if(hits == count[k]) {
						finished = true;
						success[k] = true;
						break;
					}
				}
				if(finished) {
					break;
				}
			}
			if(success[k]) {
				for(Cell cell: strongestLink.cells) {
					// If it belongs to strongestLink but NOT this link
					if(!cell.visited[k] && !cell.links.contains(this)) {
						cell.remove(k);
					}
				}
			}
		}
	}
}
