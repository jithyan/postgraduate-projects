import java.io.BufferedReader;
import java.util.HashMap;

public abstract class InputFormMenu extends HotelSpecificMenu {
   private HashMap<String, String> entryFields;
   private String[] inputFieldsOrdered;


   public InputFormMenu(BufferedReader br, ClientHopp hopp, RootMenu previous,
         String hotelName) {
      super(br, hopp, previous, hotelName);
   }


   public HashMap<String, String> getEntryFields() {
      return entryFields;
   }


   public void setEntryFields(HashMap<String, String> entryFields) {
      this.entryFields = entryFields;
   }


   public String[] getInputFieldsOrdered() {
      return inputFieldsOrdered;
   }


   public void setInputFieldsOrdered(String[] inputFieldsOrdered) {
      this.inputFieldsOrdered = inputFieldsOrdered;
   }

}
