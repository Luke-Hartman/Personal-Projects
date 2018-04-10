import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Scanner;

public class SMBCdownloader {
	@SuppressWarnings("resource")
	public static void main(String[] args) {
		System.out.println("Starting...");
		String base = "http://www.smbc-comics.com/index.php?id=";
		int count = 3760;

		for(int i = 1; i < count; i++) {
			String out;
			try {
				out = new Scanner(new URL(base + i).openStream(), "UTF-8").useDelimiter("\\A").next();
				String find = "title=";
				int index = out.indexOf(find);
				int start = out.indexOf("src=", index) + 5;
				int end = out.indexOf("id=", index)-2;
				
				String urlname = "http://www.smbc-comics.com/" + out.substring(start, end);
				int dot = urlname.lastIndexOf(".");
				String extension = urlname.substring(dot, urlname.length());
				String filename = "C:\\Users\\lukeh_000\\Pictures\\SMBC\\" + i + extension;
				
				try {
					imageFromUrl(urlname, filename);
				} catch (IOException e) {
					System.out.println("Failed to find image at " + filename);
				}
				System.out.println("Completed " + i + extension);
			} catch (IOException e1) {
				System.out.println("Failed to find comic at " + base + i);
			}
		}
	}

	public static void imageFromUrl(String urlname, String filename) throws IOException {
		URL url = new URL(urlname);
		InputStream in = new BufferedInputStream(url.openStream());
		OutputStream out = new BufferedOutputStream(new FileOutputStream(filename));

		for ( int i; (i = in.read()) != -1; ) {
			out.write(i);
		}
		in.close();
		out.close();
	}
}
