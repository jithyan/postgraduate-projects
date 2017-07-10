import java.io.BufferedReader;
import java.util.HashMap;

/**
 * Displays the options the user can make with their chosen hotel, such as
 * making a booking or checking its vacancy.
 * 
 * @author Moody
 *
 */
public class HotelSpecificMenu extends Menu {
   private final static String BOOKING_OPTION = "Make a booking";
   private final static String CHECK_VACANCY_OPTION = "Check vacancy";
   private String hotelName;


   public String getHotelName() {
      return hotelName;
   }


   public HotelSpecificMenu(BufferedReader br, ClientHopp hopp, RootMenu previous,
         String hotelName) {
      super(br, hopp, previous);
      this.hotelName = hotelName;

      String[] displayOptions = { BOOKING_OPTION, CHECK_VACANCY_OPTION };
      HashMap<String, String> menuOptions = new HashMap<String, String>(
            displayOptions.length + 3, 1);
      int i = 1;
      for (String s : displayOptions) {
         menuOptions.put(String.valueOf(i), s);
         i++;
      }
      menuOptions.put(MENU_EXIT, "Exit");
      menuOptions.put(MENU_BACK, "Back");
      menuOptions.put(MENU_MAIN, "Main");

      super.setOptions(menuOptions);
      super.setValidator(new MenuInputValidator(menuOptions));
   }


   @Override
   public RootMenu go() {
      String input;
      MenuInputValidator validator = (MenuInputValidator) super.getValidator();
      UserInterface.displayMenu(super.getOptions(), this.hotelName);

      while (true) {
         input = getUserInput("Enter your choice: ");

         if (validator.validateInput(input) == true) {
            if (input.equals(MENU_EXIT)) {
               return null;
            } else if (input.equals(MENU_BACK)) {
               return super.getPrevious();
            } else if (input.equals(MENU_MAIN)) {
               return new MainMenu(super.getInputReader(), super.getHopp());
            } else if (super.getOptions().get(input).equals(BOOKING_OPTION)) {
               return new BookingMenu(super.getInputReader(), super.getHopp(), this,
                     this.hotelName);
            } else {
               return new VacancyMenu(super.getInputReader(), super.getHopp(), this,
                     this.hotelName);
            }
         } else {
            System.out.println("Invalid input!");
         }
      }
   }

}
