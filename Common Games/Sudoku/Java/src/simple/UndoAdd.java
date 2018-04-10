package simple;

class UndoAdd extends Undo {
	Cell cell;
	
	UndoAdd(Cell cell) {
		this.cell = cell;
	}
	
	void undo() {
		cell.added = false;
		cell.value = 0;
	}
}
