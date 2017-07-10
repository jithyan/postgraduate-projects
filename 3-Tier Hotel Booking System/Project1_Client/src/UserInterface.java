import java.util.HashMap;

public final class UserInterface {
   public final static String FORM_FIELDNAME_GUEST_NAME = "Guest Name";
   public final static String FORM_FIELDNAME_CHECKIN_YEAR = "Checkin Year";
   public final static String FORM_FIELDNAME_CHECKIN_MONTH = "Checkin Month";
   public final static String FORM_FIELDNAME_CHECKIN_DAY = "Checkin Day";
   public final static String FORM_FIELDNAME_CHECKOUT_YEAR = "Checkout Year";
   public final static String FORM_FIELDNAME_CHECKOUT_MONTH = "Checkout Month";
   public final static String FORM_FIELDNAME_CHECKOUT_DAY = "Checkout Day";
   public final static String FORM_FIELDNAME_PHONE = "Phone";
   public final static String FORM_FIELDNAME_EMAIL = "E-mail";
   public final static String FORM_FIELDNAME_CREDIT_CARD = "Credit Card Number";


   /**
    * Prints to screen the list of user options.
    * 
    * @param options
    *           - the options the user can select on screen.
    * @param title
    *           - The title of the menu
    */
   public static void displayMenu(HashMap<String, String> options, String title) {
      printMenuHeader(title);
      boolean isMainMenu = true;
      int i = 1;
      for (String key : options.keySet()) {
         String opt = String.valueOf(i);
         if ((key.equals(RootMenu.MENU_EXIT) == false)
               && (key.equals(RootMenu.MENU_BACK) == false)
               && (key.equals(RootMenu.MENU_MAIN) == false)) {
            System.out.println(opt + ": " + options.get(opt));
            i++;
         } else if (key.equals(RootMenu.MENU_BACK)) {
            isMainMenu = false;
         }
      }
      printSubMenu(isMainMenu);
   }


   /**
    * Prints a header with the given menu title name.
    * 
    * @param menuName
    */
   public static void printMenuHeader(final String menuName) {
      System.out.println("\n\n================================");
      System.out.println("|   " + menuName);
      System.out.println("================================");
      System.out.println("\n" + "--------------------------");
   }


   /** Prints a message to the user, surrounded by a banner */
   public static void printMessageBanner(final String message) {
      System.out.println("\n\n*********************************************");
      System.out.println("   " + message);
      System.out.println("\n\n*********************************************");
   }


   /**
    * Prints the following submenu options: Main Menu, Exit
    */
   private static void printSubMenu(boolean isMainMenu) {
      if (isMainMenu) {
         System.out.println("\n--------------------------");
         System.out.println("[e] Exit");
         System.out.println("--------------------------\n");
      } else {
         System.out.println("\n--------------------------");
         System.out.println("[e] Exit");
         System.out.println("[b] Back");
         System.out.println("[m] Main");
         System.out.println("--------------------------\n");
      }
   }
}
