package hybrid;

import general.InvalidBoardException;
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
		// Make cells
		for(int a = 0; a < A; a++) {
			int i = i(a);
			int j = j(a);
			board[i][j] = new Cell(i, j, S);
		}
		// Make links
		for(int type = 1; type <= 3; type++) {
			for(int a = 0; a < A; a += L) {
				Link link = new Link(S);
				for(int b = 0; b < L; b++) {
					Cell cell = board[i(a + b, type)][j(a + b, type)];
					cell.links.add(link);
					link.cells.add(cell);
				}
			}
		}
	}
	
	public static void main(String[] args) throws InvalidBoardException {
		double t = System.nanoTime();
		Board b = new Board(SampleBoards.Hard);
		b.solve();
		System.out.println((System.nanoTime() - t) / 1000000000);
	}
	
	// Solves the board
	public int[][] solve() throws InvalidBoardException {
		// First add all of the known values
		for(int a = 0; a < A; a++) {
			int i = i(a);
			int j = j(a);
			int n = start[i][j];
			if(n != 0) {
				board[i][j].add(n - 1);
			}
		}
		int[][] m = gatherValues();
		if(bruteForce(0, -1, m)) {
			return m;
		}
		throw new InvalidBoardException();
	}
	
	boolean bruteForce(int i, int j, int[][] m) {
		j++;
		while(i < L) {
			while(j < L) {
				if(board[i][j].value == 0) {
					for(int n = 1; n <= L; n++) {
						if(isLegal(i, j, n, m)) {
							m[i][j] = n;
							if(bruteForce(i, j, m)) {
								return true;
							}
						}
					}
					m[i][j] = 0;
					return false;
				}
				j++;
			}
			j = 0;
			i++;
		}
		return true;
	}
	
	boolean isLegal(int i, int j, int n, int[][] m) {
		// Use already made deductions
		int k = n - 1;
		if(!board[i][j].selection[k]) {
			return false;
		}
		// Check box
		int boxI = i / S * S;
		int boxJ = j / S * S;
		for(int a = 0; a < S; a++) {
			for(int b = 0; b < S; b++) {
				if(m[boxI + a][boxJ + b] == n) {
					return false;
				}
			}
		}
		// Row
		for(int a = 0; a < L; a++) {
			if(m[a][j] == n) {
				return false;
			}
		}
		// Col
		for(int a = 0; a < L; a++) {
			if(m[i][a] == n) {
				return false;
			}
		}
		return true;
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
		System.out.println(SampleBoards.toString(gatherValues()));
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
			System.out.println(SampleBoards.toString(printPossible));
		}
	}
}
