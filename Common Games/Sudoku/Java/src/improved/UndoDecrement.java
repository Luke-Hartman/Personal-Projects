package improved;

class UndoDecrement extends Undo {
	Link link;
	int k;
	
	UndoDecrement(Link link, int k) {
		this.link = link;
		this.k = k;
	}
	
	void undo() {
		link.count[k]++;
	}
}
