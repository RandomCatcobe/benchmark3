import org.apache.commons.validator.routines.IBANValidator;

public class Probe {
    public static void main(String[] args) {
        IBANValidator validator = IBANValidator.getInstance();
        System.out.println("{\"SO\":" + validator.hasValidator("SO")
                + ",\"MN\":" + validator.hasValidator("MN")
                + ",\"OM\":" + validator.hasValidator("OM") + "}");
    }
}
