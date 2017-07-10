import java.io.BufferedReader;
import java.io.IOException;
import java.util.HashMap;

public abstract class RootMenu {
   public final static String MENU_EXIT = "e";
   public final static String MENU_MAIN = "m";
   public final static String MENU_BACK = "b";

   /* Read input from the user */
   private BufferedReader inputReader;
   /* Handles communication with the broker */
   private ClientHopp hopp;
   /* The list of options available to the user. It is hash mapping of name of
    * option displayed to the user, to the keyboard input */
   private HashMap<String, String> options;
   /* Validates the user input */
   private InputValidator validator;


   public RootMenu(BufferedReader br, ClientHopp hopp) {
      this.inputReader = br;
      this.hopp = hopp;
   }


   public BufferedReader getInputReader() {
      return inputReader;
   }


   public ClientHopp getHopp() {
      return hopp;
   }


   public HashMap<String, String> getOptions() {
      return options;
   }


   public void setOptions(HashMap<String, String> options) {
      this.options = options;
   }


   /* Display the menu options and process and respond to user input. Returns
    * the next menu to display. */
   public abstract RootMenu go();


   public InputValidator getValidator() {
      return validator;
   }


   public void setValidator(InputValidator validator) {
      this.validator = validator;
   }


   /**
    * Displays a message and gets keyboard input from the user.
    * 
    * @param message
    *           - A message to be displayed to the user describing what kind of
    *           input is required.
    * @return The user's keyboard input.
    */
   public String getUserInput(String message) {
      String input = null;
      System.out.println(message);
      try {
         input = inputReader.readLine();
      } catch (IOException e) {
         e.printStackTrace();
         System.exit(1);
      }

      return input;
   }


   /**
    * Creates a hashmapping of menu options to display with their corresponding
    * keyboard presses.
    * 
    * @param displayOptions
    *           - The names of the menu options.
    * @param isMainMenu
    *           - If it is the main menu, a different submenu is displayed.
    * @return The next menu to be displayed
    */
   public static HashMap<String, String> createMenuOptions(String[] displayOptions,
         boolean isMainMenu) {

      HashMap<String, String> menuOptions = new HashMap<String, String>(
            displayOptions.length + 3, 1);

      int i = 1;
      for (String s : displayOptions) {
         menuOptions.put(String.valueOf(i), s);
         i++;
      }

      menuOptions.put(MENU_EXIT, "Exit");

      if (isMainMenu == false) {
         menuOptions.put(MENU_BACK, "Back");
         menuOptions.put(MENU_MAIN, "Main");
      }
      return menuOptions;
   }
}
