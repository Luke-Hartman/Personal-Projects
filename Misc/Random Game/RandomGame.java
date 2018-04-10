import java.util.LinkedList;
import java.util.Queue;
import java.util.Random;
import java.util.Scanner;

public class RandomGame {
	private static final int N = 3;
	private static final int ORDER = 3;
	
	public static void main(String[] args) {
		userInput();
	}
	
	public static void userInput() {
		// Stores the table required to make markov chain guesses
		int[][] guessHistory = new int[(int) Math.pow(N, ORDER)][N];
		for(int i = 0; i < guessHistory.length; i++) {
			for(int n = 0; n < N; n++) {
				guessHistory[i][n] = 1;
			}
		}
		// Keeps track of most recently made guesses
		Queue<Integer> recentGuesses = new LinkedList<>();
		Scanner scnr = new Scanner(System.in);
		double totalGuesses = 0;
		double correctGuesses = 0;
		while(true) {
			try {
				int guess = getGuess(guessHistory, recentGuesses);
				System.out.print("Pick a number between 1 and " + N + ": ");
				int actual = Integer.parseInt(scnr.nextLine()) - 1;
				if(actual >= N) {
					throw new Exception();
				}
				System.out.println("Guess was " + (guess + 1) + ", actual was " + (actual + 1));
				totalGuesses++;
				if(actual == guess) {
					correctGuesses++;
				}
				System.out.println("Guess accuracy " + (correctGuesses / totalGuesses * 100) + "%");
				if(recentGuesses.size() == ORDER) {
					int index = getIndex(recentGuesses);
					guessHistory[index][actual]++;
					recentGuesses.remove();
				}
				recentGuesses.add(actual);
			}
			catch(Exception e) {
				e.printStackTrace();
				System.out.println("Don't worry about it : )");
			}
		}
	}
	
	private static int getGuess(int[][] guessHistory, Queue<Integer> recentGuesses) {
		Random rng = new Random();
		if(recentGuesses.size() < ORDER) {
			return rng.nextInt(N);
		}
		int[] guesses = guessHistory[getIndex(recentGuesses)];
		int sum = 0;
		for(int n = 0; n < N; n++) {
			sum += guesses[n];
		}
		int guessNum = rng.nextInt(sum);
		for(int n = 0; n < N; n++) {
			guessNum -= guesses[n];
			if(guessNum <= 0) {
				return n;
			}
		}
		return -1;
	}
	
	private static int getIndex(Queue<Integer> recentGuesses) {
		int index = 0;
		int power = 0;
		for(int n: recentGuesses) {
			index += n * (int) Math.pow(N, power++);
		}
		return index;
	}
}
