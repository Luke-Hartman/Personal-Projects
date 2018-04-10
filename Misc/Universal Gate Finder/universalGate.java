import java.util.ArrayList;

public class universalGate {
	/**
	 * Generates the basic gates which can always be used
	 * 
	 * @param N
	 * @return
	 */
	public static Gate[] constructFreeGates(int N) {
		int L = (int) Math.pow(2, N);
		Gate[] freeGates = new Gate[2 + N];
		for(int i = 0; i < N; i++) {
			boolean[] truthTable = new boolean[L];
			for(int n = 0; n < L; n++) {
				if(n / (1 << (N - i - 1)) % 2 == 0) {
					truthTable[n] = true;
				}
			}
			freeGates[i] = new Gate(truthTable, N, 0, "" + (char) ('A' + i));
		}
		Gate falseGate = new Gate(new boolean[L], N, 0, "0");
		boolean[] allTrue = new boolean[L];
		for(int i = 0; i < L; i++) {
			allTrue[i] = true;
		}
		Gate trueGate = new Gate(allTrue, N, 0, "1");
		freeGates[N] = falseGate;
		freeGates[N + 1] = trueGate;
		return freeGates;
	}
	
	public static Gate[] constructNOTGates(int N) {
		int L = (int) Math.pow(2, N);
		Gate[] NOTGates = new Gate[N];
		for(int i = 0; i < N; i++) {
			boolean[] truthTable = new boolean[L];
			for(int n = 0; n < L; n++) {
				if((n / (int) Math.pow(2, N - i - 1)) % 2 == 1) {
					truthTable[n] = true;
				}
			}
			NOTGates[i] = new Gate(truthTable, N, 0, "!" + (char) ('A' + i));
		}
		return NOTGates;
	}
	
	/**
	 * Increments the main gates to test by counting up in base 2
	 * 
	 * @param truthTable
	 * @return
	 */
	public static boolean next(boolean[] truthTable) {
		for(int i = truthTable.length - 1; i >= 0; i--) {
			truthTable[i] = !truthTable[i];
			if(truthTable[i]) {
				return true;
			}
		}
		return false;
	}
	
	/**
	 * Increments the input gates to test by counting up in base n
	 * 
	 * @param inputGateIndices
	 * @param n
	 * @return
	 */
	public static boolean next(int[] inputGateIndices, int n) {
		for(int i = inputGateIndices.length - 1; i >= 0; i--) {
			inputGateIndices[i] = (inputGateIndices[i] + 1) % n;
			if(inputGateIndices[i] % n > 0) {
				return true;
			}
		}
		return false;
	}
	
	public static void main(String[] args) {
		int N = 2;
		int L = (int) Math.pow(2, N);
		Gate[] freeGates = constructFreeGates(N);
		
		// Create AND, OR, and NOT gates
		boolean[] ANDTT = new boolean[L];
		ANDTT[0] = true;
		Gate AND = new Gate(ANDTT, N, 1, "AND");
		
		boolean[] ORTT = new boolean[L];
		for(int i = 0; i < L - 1; i++) {
			ORTT[i] = true;
		}
		Gate OR = new Gate(ORTT, N, 1, "OR");
		
		Gate[] NOTs = constructNOTGates(N);
		
		boolean[] mainTruthTable = new boolean[L];
		for(int i = 0; i < L; i++) {
			mainTruthTable[i] = true;
		}
		boolean first = true;
		while(next(mainTruthTable) || first) {
			first = false;
			ArrayList<Gate> knownGates = new ArrayList<>();
			for(Gate gate: freeGates) {
				knownGates.add(gate);
			}
			knownGates.add(new Gate(mainTruthTable, N, 1, "X"));
			
			boolean NOTDiscovered = false;
			Gate NOT = null;
			boolean ANDorORDiscovered = false;
			Gate ANDorOR = null;
			boolean universal = false;
			int size = 1;
			while(true) {
				int n = knownGates.size();
				// The last gate is the main one
				int[] inputGateIndices = new int[N + 1];
				for(int i = 0; i <= N; i++) {
					inputGateIndices[i] = n - 1;
				}
				int maxSize = 0;
				first = true;
				while(next(inputGateIndices, n) || first) {
					first = false;
					Gate[] inputs = new Gate[N];
					Gate main = knownGates.get(inputGateIndices[N]);
					int s = main.LENGTH;
					if(s == 0) {
						continue;
					}
					for(int i = 0; i < N; i++) {
						Gate gate = knownGates.get(inputGateIndices[i]);
						inputs[i] = gate;
						s += gate.LENGTH;
					}
					if(s > maxSize) {
						maxSize = s;
					}
					if(s != size) {
						continue;
					}
					Gate child = new Gate(inputs, main);
					boolean dupe = false;
					for(Gate gate: knownGates) {
						if(child.equals(gate)) {
							dupe = true;
							break;
						}
					}
					if(dupe) {
						continue;
					}
					knownGates.add(child);
					if(!ANDorORDiscovered && (child.equals(AND) || child.equals(OR))) {
						ANDorORDiscovered = true;
						ANDorOR = child;
					}
					else if(!NOTDiscovered) {
						for(int i = 0; i < N; i++) {
							if(child.equals(NOTs[i])) {
								NOTDiscovered = true;
								NOT = child;
								break;
							}
						}
					}
					if(ANDorORDiscovered && NOTDiscovered) {
						
						System.out.println("Found universal gate:");
						for(int i = 0; i < L; i++) {
							if(mainTruthTable[i]) {
								System.out.print("T ");
							}
							else {
								System.out.print("F ");
							}
						}
						System.out.println();
						System.out.println();
						System.out.println();
						System.out.println("This is either AND or OR");
						System.out.println(ANDorOR);
						System.out.println();
						System.out.println("This is NOT");
						System.out.println(NOT);
						System.out.println();
						System.out.println();
						
						universal = true;
						break;
					}
				}
				size++;
				if(size > maxSize) {
					break;
				}
			}
		}
	}
}
