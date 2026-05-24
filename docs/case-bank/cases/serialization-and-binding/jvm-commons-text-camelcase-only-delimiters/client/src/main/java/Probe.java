import org.apache.commons.text.CaseUtils;

public class Probe {
    public static void main(String[] args) {
        String camel = CaseUtils.toCamelCase("---", false, '-', '_');
        System.out.println("{\"camel\":\"" + escape(camel) + "\"}");
    }

    private static String escape(String text) {
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
