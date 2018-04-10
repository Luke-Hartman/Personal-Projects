package superSimpleImproved;

// Current best? Hybrid w/ this might be better but meh.
public class SuperSimpleImproved {
	public static void main(String[] args) {
		double start = System.nanoTime();
		int[][] m = general.SampleBoards.Hard;
		solve(m);
		System.out.println((System.nanoTime() - start) / 1000000000);
		// Now do algorithm, but traverse in such a way that it can only check
		// previously visited spots in algorithm. This is the main
		// optimization.
	}
	
	static boolean solve(int[][] m) {
		final int S = (int) Math.sqrt(m.length);
		final int L = S * S;
		final int A = L * L;
		// Using illegal b/c it defaults as false.
		boolean[][][] illegal = new boolean[L][L][L];
		// Set illegals for all the spaces in the boolean array which are
		// illegal.
		// Doing box-wise traversals to avoid doing any % ops.
		for(int r = 0; r < L; r += S) {
			for(int s = 0; s < L; s += S) {
				for(int a = 0; a < S; a++) {
					for(int b = 0; b < S; b++) {
						int i = r + a;
						int j = s + b;
						int n = m[i][j];
						int k = n - 1;
						// If this value is 0, then remove from row/col/box
						if(n != 0) {
							for(int c = 0; c < L; c++) {
								illegal[c][j][k] = true;
								illegal[i][c][k] = true;
							}
							for(int c = 0; c < S; c++) {
								for(int d = 0; d < S; d++) {
									illegal[r + c][s + d][k] = true;
								}
							}
						}
					}
				}
			}
		}
		return solveHelper(0, 0, 0, -1, S, m, illegal);
	}
	
	static boolean solveHelper(int r, int s, int a, int b, int scale, int[][] m,
			boolean[][][] illegal) {
		final int S = scale;
		final int L = S * S;
		b++;
		while(r < L) {
			while(s < L) {
				while(a < S) {
					while(b < S) {
						int i = r + a;
						int j = s + b;
						if(m[i][j] == 0) {
							for(int n = 1; n <= L; n++) {
								if(!illegal[i][j][n - 1]
										&& isLegal(r, s, a, b, n, S, m)) {
									m[i][j] = n;
									if(solveHelper(r, s, a, b, S, m, illegal)) {
										return true;
									}
								}
							}
							m[i][j] = 0;
							return false;
						}
						b++;
					}
					b = 0;
					a++;
				}
				a = 0;
				s += S;
			}
			s = 0;
			r += S;
		}
		return true;
	}
	
	static boolean isLegal(int r, int s, int a, int b, int n, int scale,
			int[][] m) {
		final int S = scale;
		int i = r + a;
		int j = s + b;
		// Check box up to a, b
		for(int c = 0; c < a; c++) {
			for(int d = 0; d < S; d++) {
				if(m[r + c][s + d] == n) {
					return false;
				}
			}
		}
		for(int d = 0; d < b; d++) {
			if(m[i][s + d] == n) {
				return false;
			}
		}
		// Check rows
		for(int c = 0; c < r; c++) {
			if(m[c][j] == n) {
				return false;
			}
		}
		// Cols
		for(int d = 0; d < s; d++) {
			if(m[i][d] == n) {
				return false;
			}
		}
		return true;
	}
}
