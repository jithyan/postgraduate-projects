import java.io.BufferedReader;

public class HotelMenu extends Menu {

   public HotelMenu(BufferedReader br, ClientHopp hopp, RootMenu previous, String city) {
      super(br, hopp, previous);
      try {
         super.setOptions(super.createMenuOptions(hopp.getHotels(city), false));
         super.setValidator(new MenuInputValidator(super.getOptions()));
      } catch (Exception e) {
         System.out.println(
               "Something went wrong communicating with the server: " + e.getMessage());
         System.exit(1);
         ;
      }
   }


   @Override
   public RootMenu go() {
      String input;
      MenuInputValidator validator = (MenuInputValidator) super.getValidator();
      UserInterface.displayMenu(super.getOptions(), "Browse Hotels");

      while (true) {
         input = getUserInput("Please enter a hotel number you would like to book: ");

         if (validator.validateInput(input) == true) {
            if (input.equals(MENU_EXIT)) {
               return null;
            } else if ((input.equals(MENU_MAIN)) || (input.equals(MENU_BACK))) {
               return super.getPrevious();
            } else {
               return new HotelSpecificMenu(super.getInputReader(), super.getHopp(), this,
                     super.getOptions().get(input));
            }
         } else {
            System.out.println("Invalid input!");
         }
      }
   }
}
