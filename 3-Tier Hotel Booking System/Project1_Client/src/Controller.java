import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Controller {
   private RootMenu menu;
   private BufferedReader br;
   private ClientHopp hopp;
   private static Controller controller = null;


   private Controller() throws Exception {
      br = new BufferedReader(new InputStreamReader(System.in));
      hopp = new ClientHopp();
      this.menu = new MainMenu(br, hopp);
   }


   /**
    * 
    * @return A singleton instance of the client controller.
    * @throws Exception
    */
   public static Controller createController() throws Exception {
      if (Controller.controller == null) {
         return new Controller();
      } else {
         return Controller.controller;
      }
   }


   /**
    * Start displaying the menus of the application. The main menu is displayed
    * first.
    */
   public void displayMenu() {
      try {
         while (true) {
            menu = menu.go();
            if (menu == null) {
               return;
            }
         }
      } finally {
         hopp.closeResources();
         try {
            br.close();
         } catch (IOException e) {
         }
      }
   }
}
