package monash.jithyan.fit5170.hotelbroker;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Listen for incoming connections and process requests for the hotel
 * reservation system.
 * 
 * @author Moody
 *
 */
public class BrokerServer {
   HotelManager hotels;


   public BrokerServer() {
      hotels = HotelManager.createHotelManager("hotel_server_info.txt");
   }


   /**
    * Start listening for connections.
    */
   public void start() {
      try {
         @SuppressWarnings("resource")
         ServerSocket serverSock = new ServerSocket(5589);
         Class.forName("HotelMessage");
         HotelMessage.initializeProtocolWords();
         System.out.println("Broker Server has started listening...");

         while (true) {
            Socket clientSocket = serverSock.accept();
            Thread t = new Thread(new BrokerServerClientHandler(clientSocket));
            t.start();
         }
      } catch (Exception ex) {
         System.out.println("Something went wrong in handling incoming connections");
         System.exit(1);
      }
   }


   private class BrokerServerClientHandler implements Runnable {
      /* Client socket */
      private Socket sock;
      /* Read requests from client */
      private BufferedReader clientReader;
      /* Write response to client */
      private PrintWriter clientWriter;
      /* Processs and answers the client request */
      private BrokerServerHopp serverHopp;


      public BrokerServerClientHandler(Socket clientSock) {
         this.sock = clientSock;
         this.serverHopp = new BrokerServerHopp();
         new BrokerClientHopp();
      }


      @Override
      public void run() {
         try {
            System.out.println("Client " + sock.getInetAddress()
                  + " is being serviced, thread id: " + Thread.currentThread().getId());

            String line = null;
            clientWriter = new PrintWriter(sock.getOutputStream());
            clientReader = new BufferedReader(
                  new InputStreamReader(sock.getInputStream()));

            while ((line = clientReader.readLine()) != null) {
               System.out.println(sock.getInetAddress() + " sent: " + line);
               processRequest(line);
            }
         } catch (IOException e) {
            System.out.println("Connection closed closed by client, thread id: "
                  + Thread.currentThread().getId());
         } finally {
            System.out.println("Exiting thread id " + Thread.currentThread().getId()
                  + ", closing resources.");
            if (clientWriter != null) clientWriter.close();

            try {
               if (clientReader != null) clientReader.close();
               if (sock != null) sock.close();
            } catch (IOException e) {
               System.out.println(e.getMessage());
            }
         }

      }


      /** Calls the appropriate HOPP methods for client requests */
      public void processRequest(String line) {
         String response;

         if (line.startsWith("GET")) {
            response = serverHopp.processGetRequest(line, hotels);
            System.out.println("Response (thread id: " + Thread.currentThread().getId()
                  + "): " + response);
            this.clientWriter.print(response + "\r\n");
            this.clientWriter.flush();

         } else if (line.startsWith("SEND")) {
            response = serverHopp.processSendRequest(line, hotels);
            System.out.println("Response (thread id: " + Thread.currentThread().getId()
                  + "): " + response);
            this.clientWriter.print(response + "\r\n");
            this.clientWriter.flush();
         } else {
            this.clientWriter.print("ERROR\r\n");
            System.out.println("Response (thread id: " + Thread.currentThread().getId()
                  + "): ERROR\r\n");
            this.clientWriter.flush();
         }
      }
   }
}

