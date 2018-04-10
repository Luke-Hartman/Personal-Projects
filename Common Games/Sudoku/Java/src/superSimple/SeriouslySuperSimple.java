package superSimple;

public class SeriouslySuperSimple {
	static boolean solve(int[][] board) {
		return solve(0, -1, (int) Math.sqrt(board.length), board);
	}
	
	static boolean solve(int i, int j, int scale, int[][] board) {
		final int S = scale;
		final int L = S * S;
		j++;
		while(i < L) {
			while(j < L) {
				if(board[i][j] == 0) {
					for(int n = 1; n <= L; n++) {
						if(isLegal(i, j, n, S, board)) {
							board[i][j] = n;
							if(solve(i, j, S, board)) {
								return true;
							}
						}
					}
					board[i][j] = 0;
					return false;
				}
				j++;
			}
			j = 0;
			i++;
		}
		return true;
	}
	
	static boolean isLegal(int i, int j, int n, int scale, int[][] board) {
		final int S = scale;
		final int L = S * S;
		// Check box
		int boxI = i / S * S;
		int boxJ = j / S * S;
		for(int a = 0; a < S; a++) {
			for(int b = 0; b < S; b++) {
				if(board[boxI + a][boxJ + b] == n) {
					return false;
				}
			}
		}
		// Row
		for(int a = 0; a < L; a++) {
			if(board[a][j] == n) {
				return false;
			}
		}
		// Col
		for(int a = 0; a < L; a++) {
			if(board[i][a] == n) {
				return false;
			}
		}
		return true;
	}
	
	public static void main(String[] args) {
		double timer = System.nanoTime();
		int[][] m = general.SampleBoards.Hard;
		solve(m);
		// System.out.println(general.SampleBoards.toString(m));
		System.out.println((System.nanoTime() - timer) / 1000000000);
	}
}
