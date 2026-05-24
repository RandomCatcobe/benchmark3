import com.google.gson.Gson;

public class Probe {
  enum Sample {
    VALUE;
    @Override public String toString() {
      return "wire-value";
    }
  }

  public static void main(String[] args) {
    Sample parsed = new Gson().fromJson(""wire-value"", Sample.class);
    System.out.println(parsed);
  }
}
