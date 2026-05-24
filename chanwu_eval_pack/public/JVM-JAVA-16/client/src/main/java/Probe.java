import com.google.i18n.phonenumbers.PhoneNumberUtil;
import com.google.i18n.phonenumbers.Phonenumber.PhoneNumber;

public class Probe {
    public static void main(String[] args) throws Exception {
        PhoneNumberUtil util = PhoneNumberUtil.getInstance();
        PhoneNumber number = util.parse("+16455551234", "US");
        boolean valid = util.isValidNumber(number);
        String type = util.getNumberType(number).toString();
        System.out.println("{\"valid\":" + valid + ",\"type\":\"" + type + "\"}");
    }
}
