package simple;

class UndoCellRemove extends Undo {
	Cell cell;
	int k;
	
	UndoCellRemove(Cell cell, int k) {
		this.cell = cell;
		this.k = k;
	}
	
	void undo() {
		cell.visited[k] = false;
		cell.selection[k] = true;
		cell.variety++;
	}
	
}
