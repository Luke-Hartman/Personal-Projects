package improved;

class Guess {
	Cell cell;
	int k;
	
	Guess(Cell cell, int k) {
		this.cell = cell;
		this.k = k;
	}
	
	void guess() throws InvalidBoardException {
		cell.add(k);
	}
}
