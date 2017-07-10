package monash.jithyan.fit5170.hotelserver.test;

import monash.jithyan.fit5170.hotelserver.HotelServer;

public class Tester {

   public static void main(String[] args) {
      try {
         int serverPort = Integer.valueOf(args[0]);

         if (serverPort < 1024) {
            System.out.println("Invalid server port");
            System.exit(1);
         } else {
            HotelServer server = new HotelServer(serverPort);
            server.start();
         }
      } catch (Exception e) {
         System.out.println("Server port needs to be an integer greater than 1024");
         System.exit(1);
      }
   }
}
