import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class WordGameUtilities {
	private static ArrayList<String> dictionary;
	
	public static ArrayList<String> loadWords(String filename) throws FileNotFoundException {
		Scanner wordSource = new Scanner(new File(filename));
		ArrayList<String> words = new ArrayList<>();
		while(wordSource.hasNext()) {
			String word = wordSource.next();
			words.add(word);
			/*
			if(word.length() > 2) {
				words.add(word);
			}
			*/
		}
		wordSource.close();
		return words;
	}
	
	// Dictionary must be sorted alphabetically
	public static ArrayList<String> deleteNeighbors(String root) {
		ArrayList<String> neighbors = new ArrayList<>();
		for(int i = 0; i < root.length(); i++) {
			StringBuilder rootBuilder = new StringBuilder(root);
			rootBuilder.deleteCharAt(i);
			String neighbor = rootBuilder.toString();
			if(inWordList(neighbor, dictionary)) {
				neighbors.add(neighbor);
			}
		}
		return neighbors;
	}
	
	// Dictionary must be sorted alphabetically
	public static ArrayList<String> insertNeighbors(String root) {
		ArrayList<String> neighbors = new ArrayList<>();
		for(int i = 0; i <= root.length(); i++) {
			for(char c = 'a'; c <= 'z'; c++) {
				StringBuilder rootBuilder = new StringBuilder(root);
				rootBuilder.insert(i, c);
				String neighbor = rootBuilder.toString();
				if(inWordList(neighbor, dictionary)) {
					neighbors.add(neighbor);
				}
			}
		}
		return neighbors;
	}
	
	// Dictionary must be sorted alphabetically
	public static ArrayList<String> replaceNeighbors(String root) {
		ArrayList<String> neighbors = new ArrayList<>();
		for(int i = 0; i < root.length(); i++) {
			StringBuilder rootBuilder = new StringBuilder(root);
			for(char c = 'a'; c <= 'z'; c++) {
				if(c == root.charAt(i)) {
					continue;
				}
				rootBuilder.setCharAt(i, c);
				String neighbor = rootBuilder.toString();
				if(inWordList(neighbor, dictionary)) {
					neighbors.add(neighbor);
				}
			}
		}
		return neighbors;
	}
	
	// Dictionary must be sorted alphabetically
	public static ArrayList<String> allNeighbors(String root) {
		ArrayList<String> neighbors = new ArrayList<>();
		neighbors.addAll(deleteNeighbors(root));
		neighbors.addAll(insertNeighbors(root));
		neighbors.addAll(replaceNeighbors(root));
		return neighbors;
	}
	
	public static int[] getCharRarity() {
		int[] charCounts = new int['z' - 'a' + 1];
		for(String word: dictionary) {
			for(int i = 0; i < word.length(); i++) {
				charCounts[word.charAt(i) - 'a']++;
			}
		}
		int maxValue = 0;
		int maxIndex = -1;
		int[] charRarity = new int['z' - 'a' + 1];
		for(int ranking = 1; ranking <= 'z' - 'a' + 1; ranking++) {
			for(int i = 0; i <= 'z' - 'a'; i++) {
				if(charCounts[i] > maxValue) {
					maxValue = charCounts[i];
					maxIndex = i;
				}
			}
			charRarity[maxIndex] = ranking;
			charCounts[maxIndex] = -1;
			maxValue = -1;
		}
		return charRarity;
	}
	
	// words must be sorted alphabetically
	public static boolean inWordList(String word, ArrayList<String> words) {
		int start = 0;
		int end = words.size() - 1;
		while(true) {
			int middle = (start + end) / 2;
			String middleWord = words.get(middle);
			int comparision = word.compareTo(middleWord);
			if(comparision < 0) {
				end = middle - 1;
			}
			else if(comparision > 0) {
				start = middle + 1;
			}
			else {
				return true;
			}
			if(end < start) {
				return false;
			}
		}
	}
	
	public static ArrayList<String> regexFind(String pattern) {
		ArrayList<String> matches = new ArrayList<>();
		try {
			Pattern p = Pattern.compile(pattern);
			for(String word: dictionary) {
				Matcher m = p.matcher(word);
				if(m.matches()) {
					matches.add(word);
				}
			}
		}
		catch(Exception e) {
			System.out.println("Invalid regex");
		}
		return matches;
	}
	
	// Dictionary must be sorted alphabetically
	public static ArrayList<String> permutationFind(int[] letterCounts) {
		ArrayList<String> results = new ArrayList<>();
		permutationFindHelper(0, dictionary.size() - 1, results, letterCounts, new StringBuilder());
		return results;
	}
	
	private static void permutationFindHelper(int start, int end, ArrayList<String> words, int[] letterCounts,
		StringBuilder strBuilder) {
		for(int i = 0; i < letterCounts.length; i++) {
			if(letterCounts[i] > 0) {
				char c = (char) ('a' + i);
				int index = strBuilder.length();
				strBuilder.append(c);
				int startstart = start;
				int startend = end;
				// Find the first word with c as its (index + 1)th letter
				int latestFound = -1;
				int earliestNotFound = end;
				while(true) {
					int startmid = (startstart + startend) / 2;
					String startmidWord = dictionary.get(startmid);
					
					int comparison = startmidWord.charAt(index) - c;
					if(comparison < 0) {
						startstart = startmid + 1;
					}
					else if(comparison > 0) {
						startend = startmid - 1;
						earliestNotFound = startend;
					}
					else if(startmid != start && dictionary.get(startmid - 1).charAt(index) == c) {
						startend = startmid - 1;
						if(latestFound == -1) {
							latestFound = startmid;
						}
					}
					else {
						if(startmidWord.length() == index + 1) {
							words.add(strBuilder.toString());
						}
						startstart = startmid + 1;
						break;
					}
					if(startend < startstart) {
						break;
					}
				}
				if(latestFound == -1) {
					strBuilder.deleteCharAt(index);
					continue;
				}
				int endstart = latestFound;
				int endend = earliestNotFound;
				while(true) {
					int endmid = (endstart + endend) / 2;
					String endmidWord = dictionary.get(endmid);
					
					int comparison = endmidWord.charAt(index) - c;
					if(comparison > 0) {
						endend = endmid - 1;
					}
					else if(endmid != endend && dictionary.get(endmid + 1).charAt(index) == c) {
						endstart = endmid + 1;
					}
					else {
						endstart = endmid;
						break;
					}
				}
				letterCounts[i]--;
				permutationFindHelper(startstart, endstart, words, letterCounts, strBuilder);
				letterCounts[i]++;
				strBuilder.deleteCharAt(index);
			}
		}
	}
	
	public static void playerAid(int[] charValues) {
		Sorter sorter = new ValueSorter(charValues);
		@SuppressWarnings("resource")
		Scanner scnr = new Scanner(System.in);
		System.out.println("Type in a word to check for its presence in the provided dictionary.");
		System.out.println("Type in \"/\" for a list of commands.");
		while(true) {
			System.out.print(">> ");
			String in = scnr.nextLine().toLowerCase();
			if(in.length() == 0) {
				continue;
			}
			else if(in.charAt(0) == '/') {
				int codendex = in.indexOf(' ');
				String code;
				if(codendex == -1) {
					code = ".null code.";
				}
				else {
					code = in.substring(1, codendex);
				}
				String string = in.substring(codendex + 1);
				String message;
				ArrayList<String> results;
				boolean printResultsCount = false;
				int printCount = 10;
				if(code.length() > 1) {
					if(code.length() == 2 && code.charAt(1) == 'a') {
						printCount = Integer.MAX_VALUE;
					}
					else {
						try {
							printCount = Integer.parseInt(code.substring(1));
						}
						catch(NumberFormatException e) {
							code = ".null code.";
						}
					}
				}
				switch(code.charAt(0)) {
					case 'n':
						message = "Neighbors";
						results = allNeighbors(string);
						sorter.sort(results);
						printResultsCount = true;
						break;
					case 'r':
						message = "Matches";
						results = regexFind(string);
						sorter.sort(results);
						printResultsCount = true;
						break;
					case 'p':
						message = "Possible Words";
						int[] letterCounts = new int['z' - 'a' + 1];
						String[] splode = string.split(" ");
						boolean fail = false;
						for(String str: splode) {
							if(str.length() != 1) {
								System.out.println("Invalid character \"" + str + "\"");
								fail = true;
								break;
							}
							letterCounts[str.charAt(0) - 'a']++;
						}
						if(fail) {
							results = new ArrayList<>(0);
							break;
						}
						results = permutationFind(letterCounts);
						sorter.sort(results);
						printResultsCount = true;
						break;
					case 's':
						message = "New sorter";
						results = new ArrayList<>(1);
						results.add(string);
						switch(string) {
							case "value":
								sorter = new ValueSorter(charValues);
								break;
							case "length":
								sorter = new LengthSorter();
								break;
							case "neighbor":
								sorter = new NeighborSorter();
								break;
							default:
								System.out.println("Invalid sorting type. Ex: \"/s value\"");
								message = "Valid sorting types";
								results.remove(0);
								results.add("value");
								results.add("length");
								results.add("neighbor");
						}
						break;
					default:
						message = "Invalid Command";
						results = new ArrayList<>(2);
						results.add("\"/n\" - print all neighbors");
						results.add("\"/r\" - find regex matches");
						results.add("\"/p\" - find all words which can be spelled using the given letters");
						results.add("\"/s\" - choose sorting method. Options: value, length, neighbor");
						results.add(
							"Type in a number after a command to specify the number of results shown (Default is 10).");
						results.add("Ex: \"/n20 \"");
				}
				System.out.println(message + ":");
				if(printResultsCount) {
					System.out.println("Found " + results.size() + " results");
				}
				for(int i = 0; i < Math.min(results.size(), printCount); i++) {
					System.out.println(results.get(i));
				}
			}
			else {
				if(inWordList(in, dictionary)) {
					System.out.println("Yes");
				}
				else {
					System.out.println("No");
				}
			}
		}
	}
	
	public static ArrayList<String> dictionaryIntersection(ArrayList<String> dict1, ArrayList<String> dict2) {
		ArrayList<String> newDictionary = new ArrayList<>();
		for(String word: dict1) {
			if(inWordList(word, dict2)) {
				newDictionary.add(word);
			}
		}
		System.out.println(newDictionary.size());
		return newDictionary;
	}
	
	public static void main(String[] args) throws FileNotFoundException {
		int[] charScrabbleScore = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
		dictionary = loadWords("ospd.txt");
		//ArrayList<String> dict1 = loadWords("mostcommon.txt");
		//ArrayList<String> dictionary = dictionaryIntersection(dict1, dict2);
		//int[] charRarity = getCharRarity(dictionary);
		playerAid(charScrabbleScore);
	}
	
	private static interface Sorter {
		public void sort(ArrayList<String> words);
	}
	
	private static class ValueSorter implements Sorter {
		private int[] charValues;
		
		public ValueSorter(int[] charValues) {
			this.charValues = charValues;
		}
		
		@Override
		public void sort(ArrayList<String> words) {
			ComparableWord[] comparableWords = new ComparableWord[words.size()];
			for(int i = 0; i < words.size(); i++) {
				String word = words.get(i);
				int value = 0;
				for(int j = 0; j < word.length(); j++) {
					value += charValues[word.charAt(j) - 'a'];
				}
				comparableWords[i] = new ComparableWord(word, value);
			}
			Arrays.sort(comparableWords);
			for(int i = 0; i < words.size(); i++) {
				words.set(i, comparableWords[i].str);
			}
		}
	}
	
	private static class LengthSorter implements Sorter {
		@Override
		public void sort(ArrayList<String> words) {
			ComparableWord[] comparableWords = new ComparableWord[words.size()];
			for(int i = 0; i < words.size(); i++) {
				String word = words.get(i);
				comparableWords[i] = new ComparableWord(word, word.length());
			}
			Arrays.sort(comparableWords);
			for(int i = 0; i < words.size(); i++) {
				words.set(i, comparableWords[i].str);
			}
		}
	}
	
	private static class NeighborSorter implements Sorter {
		@Override
		public void sort(ArrayList<String> words) {
			ComparableWord[] comparableWords = new ComparableWord[words.size()];
			for(int i = 0; i < words.size(); i++) {
				String word = words.get(i);
				comparableWords[i] = new ComparableWord(word, allNeighbors(word).size());
			}
			Arrays.sort(comparableWords);
			for(int i = 0; i < words.size(); i++) {
				words.set(i, comparableWords[i].str);
			}
		}
	}
}

class ComparableWord implements Comparable<ComparableWord> {
	int value;
	String str;
	
	ComparableWord(String str, int value) {
		this.str = str;
		this.value = value;
	}
	
	@Override
	public int compareTo(ComparableWord other) {
		return other.value - value;
	}
}
