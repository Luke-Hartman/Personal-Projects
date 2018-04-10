
public class Gate {
	// Number of gates it is composed of
	public final int SIZE;
	// Length of the longest path through this gate
	public final int LENGTH;
	// Subgates to make this gate
	private final Gate[] inputs;
	private final Gate main;
	// Equivalent truth table to this gate
	private final boolean[] TRUTHTABLE;
	// Number of inputs
	private final int N;
	// 2**N == TRUTHTABLE.length
	private final int L;
	// Name of gate, EX: "A" or "1"
	private final String NAME;
	
	/**
	 * This is the constructor for creating the inputs to the main gate, and the
	 * main gate itself.
	 * 
	 * @param truthTable - Equivalent truth table
	 * @param n - number of inputs/variables
	 * @param size - do 1 for actual gates (such as AND), 0 for inputs
	 *            represented by gates (such as A or 1)
	 * 			
	 */
	public Gate(boolean[] truthTable, int n, int size, String name) {
		TRUTHTABLE = truthTable;
		N = n;
		L = TRUTHTABLE.length;
		SIZE = size;
		LENGTH = size;
		inputs = null;
		main = null;
		NAME = name;
	}
	
	/**
	 * Creates a new gate from known gates
	 * 
	 * @param inputs
	 * @param main
	 */
	public Gate(Gate[] inputs, Gate main) {
		this.main = main;
		this.inputs = inputs;
		N = inputs.length;
		L = (int) Math.pow(2, N);
		int totalSize = 0;
		int maxLength = 0;
		for(Gate gate: inputs) {
			totalSize += gate.SIZE;
			if(gate.LENGTH > maxLength) {
				maxLength = gate.LENGTH;
			}
		}
		SIZE = totalSize + main.SIZE;
		LENGTH = maxLength + main.LENGTH;
		
		/*
		 *  This next bit is where the magic happens. 
		 *  It takes puts the generic A, B, C... inputs through the input gates
		 *  Then takes the input gates outputs, maps that to generic A, B, C...
		 *  inputs and sees how the main gate would react to those generic 
		 *  A, B, C... inputs (but it is actually the output of the input gates)
		 */
		TRUTHTABLE = new boolean[L];
		// index is the index in the TRUTHTABLE
		for(int index = 0; index < L; index++) {
			boolean[] inputValues = new boolean[N];
			// i is the index in the inputValues
			for(int i = 0; i < N; i++) {
				Gate gate = inputs[i];
				inputValues[i] = gate.TRUTHTABLE[index];
			}
			int n = nfrominputValues(inputValues);
			TRUTHTABLE[index] = main.TRUTHTABLE[n];
		}
		NAME = boolArrayToString(TRUTHTABLE);
	}
	
	/**
	 * Generates the input EX: N = 3, n = 0 returns {T, T, T} n = 1 returns {T,
	 * T, T} Used to generate the variable values (n = 1 is A = T, B = T, C = F)
	 * 
	 * @param n
	 * @return
	 */
	private boolean[] inputValues(int n) {
		// Flips n so it is normal binary
		n = L - n - 1;
		boolean[] inputValues = new boolean[N];
		int index = N;
		while(n > 0) {
			index--;
			inputValues[index] = n % 2 == 1;
			n /= 2;
		}
		return inputValues;
	}
	
	/**
	 * Inverse of inputValues(int n). Used for getting index in truth table
	 * 
	 * @param inputs - {A, B, C...} inputs as binary
	 * @return index in truth table (n)
	 */
	private int nfrominputValues(boolean[] inputValues) {
		int n = 0;
		for(int i = 0; i < N; i++) {
			if(!inputValues[i]) {
				n += Math.pow(2, N - i - 1);
			}
		}
		return n;
	}
	
	/**
	 * Compares truth tables
	 * 
	 * @param gate
	 * @return
	 */
	public boolean equals(Object other) {
		for(int n = 0; n < L; n++) {
			if(TRUTHTABLE[n] != ((Gate) other).TRUTHTABLE[n]) {
				return false;
			}
		}
		return true;
	}
	
	public String toString() {
		if(inputs == null) {
			return NAME;
		}
		String s = "{";
		for(Gate gate: inputs) {
			s += "[" + gate + "]-";
		}
		s += "> [" + main + "] <=> " + NAME + "}";
		return s;
	}
	
	private static String boolArrayToString(boolean[] a) {
		String s = "{ ";
		for(boolean b: a) {
			if(b) {
				s += "T ";
			}
			else {
				s += "F ";
			}
		}
		s += "}";
		return s;
	}
}
