import org.jsoup.Jsoup;

public class Probe {
    public static void main(String[] args) {
        String text = Jsoup.parse("<div>One</div><span>Two</span>").text();
        System.out.println("{\"text\":\"" + escape(text) + "\"}");
    }

    private static String escape(String text) {
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
