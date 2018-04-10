package simple;

class UndoLinkRemove extends Undo {
	Link link;
	int k;
	
	UndoLinkRemove(Link link, int k) {
		this.link = link;
		this.k = k;
	}
	
	void undo() {
		link.visited[k] = false;
	}
}
