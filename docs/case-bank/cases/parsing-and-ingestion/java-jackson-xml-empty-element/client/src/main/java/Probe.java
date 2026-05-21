import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;

public class Probe {
  public static void main(String[] args) throws Exception {
    JsonNode root = new XmlMapper().readTree("<root><value/></root>");
    JsonNode value = root.get("value");
    System.out.println(value.getNodeType() + ":" + value.toString());
  }
}
