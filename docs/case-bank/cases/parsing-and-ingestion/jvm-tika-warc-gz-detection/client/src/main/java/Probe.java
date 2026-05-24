import org.apache.tika.Tika;

public class Probe {
    public static void main(String[] args) {
        String type = new Tika().detect("sample.warc.gz");
        System.out.println("{\"warc_gz\":\"" + type + "\"}");
    }
}
