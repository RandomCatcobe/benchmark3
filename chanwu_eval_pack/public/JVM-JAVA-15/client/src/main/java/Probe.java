import org.joda.time.DateTimeZone;
import org.joda.time.Instant;

public class Probe {
    public static void main(String[] args) {
        DateTimeZone zone = DateTimeZone.forID("Asia/Almaty");
        int offset = zone.getOffset(Instant.parse("2024-03-01T00:30:00Z"));
        System.out.println("{\"offset_seconds\":" + (offset / 1000) + "}");
    }
}
