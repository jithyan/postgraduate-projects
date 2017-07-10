import java.io.BufferedReader;

public class MainMenu extends RootMenu {


   public MainMenu(BufferedReader br, ClientHopp hopp) {
      super(br, hopp);
      try {
         super.setOptions(
               super.createMenuOptions(super.getHopp().getCitiesServed(), true));
         super.setValidator(new MenuInputValidator(super.getOptions()));
      } catch (Exception e1) {
         System.out.println("Error communicating with Broker: " + e1.getMessage());
         System.exit(1);
      }

   }


   public RootMenu go() {
      String input;
      UserInterface.displayMenu(super.getOptions(), "Main Menu");
      MenuInputValidator validator = (MenuInputValidator) super.getValidator();

      while (true) {
         input = getUserInput(
               "Please enter a city number you would like to browse for hotels: ");

         if (validator.validateInput(input) == true) {
            if (input.equals(MENU_EXIT)) {
               return null;

            } else {
               try {
                  return new HotelMenu(super.getInputReader(), super.getHopp(), this,
                        super.getOptions().get(input));
               } catch (Exception e) {
                  System.out.println("Something went wrong: " + e.getMessage());
                  return this;
               }
            }

         } else {
            System.out.println("Invalid input!");
         }
      }
   }
}
