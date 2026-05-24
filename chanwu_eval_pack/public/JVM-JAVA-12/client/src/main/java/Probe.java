import org.apache.commons.io.FilenameUtils;

public class Probe {
    public static void main(String[] args) throws Exception {
        boolean contains = FilenameUtils.directoryContains("/tmp/base", "/tmp/base2/file.txt");
        System.out.println("{\"contains\":" + contains + "}");
    }
}
