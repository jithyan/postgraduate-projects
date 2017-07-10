package monash.jithyan.fit5170.hotelbroker;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class BrokerClientHopp {

   /**
    * 
    * @param ipAddress
    *           IPv4 address of hotel server
    * @param port
    *           Port of hotel server
    * @param message
    *           The protocol formatted message to server
    * @return
    * @throws UnknownHostException
    * @throws IOException
    */
   public static String sendRequestToHotelServer(String ipAddress, String port,
         HotelMessage message) throws UnknownHostException, IOException {
      Socket sock = null;
      InputStreamReader inputStream = null;
      BufferedReader reader = null;
      PrintWriter writer = null;
      System.out.println("opening connection to hotel: " + ipAddress + ":" + port);

      try {

         sock = new Socket(ipAddress, Integer.valueOf(port));
         inputStream = new InputStreamReader(sock.getInputStream());
         reader = new BufferedReader(inputStream);
         writer = new PrintWriter(sock.getOutputStream());

         writer.print(message.getRequest());
         writer.flush();

         return reader.readLine();

      } finally {
         try {
            if (writer != null) writer.close();
            if (reader != null) reader.close();
            if (inputStream != null) inputStream.close();
            if (sock != null) sock.close();
         } catch (IOException e) {
         }
      }
   }
}
