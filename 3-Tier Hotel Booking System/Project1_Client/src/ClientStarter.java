
public class ClientStarter {
   public static void main(String[] args) {
      try {
         Controller controller;
         controller = Controller.createController();
         controller.displayMenu();
      } catch (Exception e) {
         System.out
               .println("Failed to communicate with broker server: " + e.getMessage());
         System.out.println("Client terminated.");
         System.exit(1);
      }
   }
}
