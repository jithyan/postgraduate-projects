package monash.jithyan.fit5170.hotelserver;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import monash.jithyan.fit5170.hotelserver.database.HotelDb;
import monash.jithyan.fit5170.hotelserver.exception.InvalidBookingException;
import monash.jithyan.fit5170.hotelserver.exception.QueryInvalidResultException;

/**
 * Initializes the hotel server's database, the lock for managing concurrent
 * updates to the database and listens for and handles incoming connections.
 * 
 * @author Moody
 *
 */


public class HotelServer {
   private static HashSet<String> bookingProtocolKeywords;
   private static HashSet<String> vacancyProtocolKeywords;
   private HotelDb db;
   private static Object lock;
   private int serverPort;


   public HotelServer() {
      try {
         this.serverPort = 5889;
         db = HotelDb.createHotelDb();
         lock = new Object();
         initializeProtocolWords();
      } catch (ClassNotFoundException e) {
         System.out.println("Error: Unable to load Sqlite class: " + e.getMessage());
         System.exit(1);
      } catch (SQLException e) {
         System.out.println("Error: Something went wrong creating new Hotel database: "
               + e.getMessage());
         System.exit(1);
      }
   }


   public HotelServer(int port) {
      try {
         this.serverPort = port;
         db = HotelDb.createHotelDb();
         lock = new Object();
         initializeProtocolWords();
      } catch (ClassNotFoundException e) {
         System.out.println("Error: Unable to load Sqlite class: " + e.getMessage());
         System.exit(1);
         
      } catch (SQLException e) {
         System.out.println("Error: Something went wrong creating new Hotel database: "
               + e.getMessage());
         System.exit(1);
      }
   }


   /**
    * Loads the keywords of a protocol from file stored on the server.
    */
   private void initializeProtocolWords() {
      Path path = Paths.get("protocol.txt");
      List<String> lines;
      String[] keyWords;
      HashSet<String> keyWordSet = new HashSet<String>();

      try {
         lines = Files.readAllLines(path, StandardCharsets.UTF_8);
         for (String line : lines) {
            line = line.replaceAll("\\r\\n", "");
            keyWords = line.split(" ");
            for (int i = 1; i < keyWords.length; i++) {
               keyWordSet.add(keyWords[i]);
            }

            if (line.startsWith("BOOK")) {
               HotelServer.bookingProtocolKeywords = keyWordSet;
            } else if (line.startsWith("VACANCY")) {
               HotelServer.vacancyProtocolKeywords = keyWordSet;
            }
         }
      } catch (Exception e) {
         e.printStackTrace();
         System.exit(1);
      }
   }


   /**
    * Start listening for and handling incoming connections.
    */
   public void start() {
      try {
         @SuppressWarnings("resource")
         ServerSocket serverSock = new ServerSocket(this.serverPort);

         System.out.println("Server has started listening...");
         while (true) {
            Socket clientSocket = serverSock.accept();
            Thread t = new Thread(new HotelServerClientHandler(clientSocket, db, lock));
            t.start();
         }
      } catch (Exception ex) {
         ex.printStackTrace();
      }
   }

   /**
    * Handles incoming connections according to the protocol followed by the
    * server.
    * 
    * @author Moody
    *
    */
   private class HotelServerClientHandler implements Runnable {
      private PrintWriter writer;
      private BufferedReader reader;
      private Socket sock;
      private HotelDb db;
      private HotelServerHopp hopp;


      public HotelServerClientHandler(Socket clientSocket, HotelDb db, Object lock) {
         try {
            this.sock = clientSocket;
            this.db = db;
            this.hopp = new HotelServerHopp(lock);
            System.out.println("Client " + sock.getInetAddress() + "is being serviced");
         } catch (Exception ex) {
            ex.printStackTrace();
            System.exit(1);
         }
      }


      /**
       * Processes the client request and uses the hopp to determine the
       * response. Requests must conform to the hotel server protcol.
       * 
       * @param line
       */
      public void processRequest(String line) {
         String[] rawData;
         HashMap<String, String> data = new HashMap<String, String>();

         if (line.startsWith("BOOK")) {
            line = line.replaceAll("^BOOK ", "");
            rawData = line.split(",");

            for (int i = 0; i < rawData.length; i++) {
               String[] temp = rawData[i].split("=");
               String keyWord = temp[0];
               String value = temp[1];

               if (HotelServer.bookingProtocolKeywords.contains(keyWord)) {
                  data.put(keyWord, value);
               } else {
                  this.writer.print("ERROR unrecognized format or protocol\r\n");
                  this.writer.flush();
                  System.out.println("Error: unrecognized booking format or word");
                  return;
               }
            }

            try {
               hopp.registerBooking(data, db);
               this.writer.print("BOOK SUCCESS\r\n");
               this.writer.flush();
               System.out.println("added new booking");

            } catch (SQLException | QueryInvalidResultException e) {
               System.out.println(e.getMessage());
               this.writer.print("BOOK ERROR\r\n");
               this.writer.flush();

            } catch (InvalidBookingException e) {
               this.writer.print("BOOK FAIL\r\n");
               this.writer.flush();
               System.out.println(e.getMessage());
            }

         } else if (line.startsWith("VACANCY")) {
            String[] request = line.split(" ");
            rawData = request[1].split(",");

            for (int i = 0; i < rawData.length; i++) {
               String[] temp = rawData[i].split("=");
               String keyWord = temp[0];
               String value = temp[1];

               if (HotelServer.vacancyProtocolKeywords.contains(keyWord)) {
                  data.put(keyWord, value);
               } else {
                  this.writer.print("VACANCY ERROR\r\n");
                  this.writer.flush();
                  System.out.println("Error: unrecognized vacancy format or word");
                  return;
               }
            }

            try {
               if (hopp.checkVacancy(data.get("checkin_date"), data.get("checkout_date"),
                     db)) {
                  this.writer.print("VACANCY SUCCESS\r\n");
                  this.writer.flush();
                  System.out.println("dates are vacant");
               } else {
                  this.writer.print("VACANCY FAIL\r\n");
                  this.writer.flush();
                  System.out.println("dates are not vacant");
               }
            } catch (SQLException | QueryInvalidResultException e) {
               System.out.println(e.getMessage());
               this.writer.print("VACANCY ERROR\r\n");
               this.writer.flush();
               return;
            }
         } else {
            // Request line starts with an unrecognized term
            System.out.println("Error: unrecognized request");
            this.writer.print("ERROR unrecognized protocol\r\n");
            this.writer.flush();
            return;
         }
      }


      @Override
	public void run() {
         try {
            String line = null;
            writer = new PrintWriter(sock.getOutputStream());
            reader = new BufferedReader(new InputStreamReader(sock.getInputStream()));

            while ((line = reader.readLine()) != null) {
               System.out.println(sock.getInetAddress() + " sent: " + line);
               processRequest(line);
            }
         } catch (IOException e) {
            System.out.println("IO error");
            System.exit(1);
         } finally {
            if (writer != null) writer.close();

            try {
               if (reader != null) reader.close();
               if (sock != null) sock.close();
            } catch (IOException e) {
               System.out.println(e.getMessage());
            }
         }
      }


      @Override
	protected void finalize() {
         if (writer != null) writer.close();

         try {
            if (reader != null) reader.close();
            if (sock != null) sock.close();
         } catch (IOException e) {
            System.out.println(e.getMessage());
         }
      }
   }
}
