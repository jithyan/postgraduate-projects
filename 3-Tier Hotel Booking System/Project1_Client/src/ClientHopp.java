import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.text.MessageFormat;
import java.util.HashMap;

/**
 * Handles communcation with the broker server.
 * 
 * @author Moody
 *
 */
public class ClientHopp {
   private BufferedReader reader;
   private PrintWriter writer;
   private Socket sock;

   /* Names of the fields used in the protocol when communicating with the
    * broker */
   public final static String SEND_FIELD_GUEST_NAME = "guest_name";
   public final static String SEND_FIELD_CHECKIN_YEAR = "checkin_year";
   public final static String SEND_FIELD_CHECKIN_MONTH = "checkin_month";
   public final static String SEND_FIELD_CHECKIN_DAY = "checkin_day";
   public final static String SEND_FIELD_CHECKOUT_YEAR = "checkout_year";
   public final static String SEND_FIELD_CHECKOUT_MONTH = "checkout_month";
   public final static String SEND_FIELD_CHECKOUT_DAY = "checkout_day";
   public final static String SEND_FIELD_PHONE = "phone";
   public final static String SEND_FIELD_EMAIL = "email";
   public final static String SEND_FIELD_CREDIT_CARD = "credit_card";
   public final static String SEND_FIELD_HOTEL = "hotel";


   /**
    * Connects to the broker server.
    * 
    * @param port
    *           - port number of the broker server.
    */
   public ClientHopp(int port) {
      try {
         sock = new Socket("127.0.0.1", port);
         InputStreamReader streamReader = new InputStreamReader(sock.getInputStream());
         reader = new BufferedReader(streamReader);
         writer = new PrintWriter(sock.getOutputStream());
         System.out.println("Successfully connected to broker...\n\n");

      } catch (IOException ex) {
         System.out.println("Failed to establish connection, system exiting.");
         System.exit(1);
      }
   }


   /**
    * Connects to the broker server.
    */
   public ClientHopp() {
      try {
         sock = new Socket("127.0.0.1", 5589);
         InputStreamReader streamReader = new InputStreamReader(sock.getInputStream());
         reader = new BufferedReader(streamReader);
         writer = new PrintWriter(sock.getOutputStream());
         System.out.println("Successfully connected to broker...\n\n");

      } catch (IOException ex) {
         System.out.println("Failed to establish connection, system exiting.");
         System.exit(1);
      }
   }


   /**
    * Asks the broker for a list of hotels it services belonging to the given
    * city.
    * 
    * @param city
    *           - Name of the city.
    * @return A list of hotels located in the given city.
    * @throws Exception
    *            - Communication with the broker failed somewhere.
    */
   public String[] getHotels(String city) throws Exception {
      this.writer.print("GET city=" + city + "\r\n");
      this.writer.flush();

      String reply = this.reader.readLine();
      String[] words = reply.split(" ");

      if (words[0].equals("SUCCESS")) {
         words = (reply.substring("SUCCESS ".length(), reply.length())).trim().split(",");
         return words;
      } else {
         throw new Exception("Broker failed to process request.");
      }
   }


   public void closeResources() {
      try {
         if (reader != null) reader.close();
         if (writer != null) writer.close();
         if (sock != null) sock.close();

      } catch (IOException e) {
         e.printStackTrace();
      }
   }


   /**
    * Ask the broker for all the cities it services.
    * 
    * @return A list of all the cities serviced.
    * @throws Exception
    */
   public String[] getCitiesServed() throws Exception {
      return getHotels("ANY");
   }


   /**
    * Send a booking request to the broker.
    * 
    * @param bookingDetails
    *           A mapping of field names to values of details required for a
    *           booking.
    * @param hotelName
    *           The name of the hotel being booked.
    * @return True - the booking was successfully completed False - The booking
    *         could not be done as the dates are not vacant.
    * @throws Exception
    *            Something went wrong communicating with the broker, or between
    *            the broker and the hotels.
    */
   public boolean sendBooking(HashMap<String, String> bookingDetails, String hotelName)
         throws Exception {
      String request = "SEND BOOKING ";
      String details = MessageFormat.format(
            "{0}={1},{2}={3},{4}={5},{6}={7},{8}={9},{10}={11},{12}={13},{14}={15},{16}={17},{18}={19},{20}={21}",
            ClientHopp.SEND_FIELD_GUEST_NAME,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_GUEST_NAME),
            ClientHopp.SEND_FIELD_CHECKIN_YEAR,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR),
            ClientHopp.SEND_FIELD_CHECKIN_MONTH,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH),
            ClientHopp.SEND_FIELD_CHECKIN_DAY,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CHECKIN_DAY),
            ClientHopp.SEND_FIELD_CHECKOUT_YEAR,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR),
            ClientHopp.SEND_FIELD_CHECKOUT_MONTH,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH),
            ClientHopp.SEND_FIELD_CHECKOUT_DAY,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY),
            ClientHopp.SEND_FIELD_PHONE,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_PHONE),
            ClientHopp.SEND_FIELD_EMAIL,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_EMAIL),
            ClientHopp.SEND_FIELD_CREDIT_CARD,
            bookingDetails.get(UserInterface.FORM_FIELDNAME_CREDIT_CARD),
            ClientHopp.SEND_FIELD_HOTEL, hotelName);

      request = request.concat(details);
      request = request.trim();
      this.writer.print(request + "\r\n");
      this.writer.flush();

      String reply;
      try {
         reply = this.reader.readLine();
      } catch (IOException e) {
         System.out.println("Error getting response from broker");
         return false;
      }
      String[] words = reply.split(" ");

      if (words[0].equals("SUCCESS")) {
         return true;
      } else if (words[0].equals("FAIL")) {
         return false;
      } else {
         throw new Exception("Error: Broker failed to process request.");
      }
   }


   /**
    * Send a request to the broker to check if the specified dates are vacant
    * for a particular hotel.
    * 
    * @param vacancyDetails
    *           - Checkin and checkout dates.
    * @param hotelName
    *           - The name of the hotel you are checking the vacancy in.
    * @return true - The given dates are vacant. false - some or all the days
    *         between the given dates are NOT vacant.
    * @throws Exception
    *            - Something went wrong communicating with the broker, or
    *            between the broker and the hotels.
    */
   public boolean sendCheckVacancy(HashMap<String, String> vacancyDetails,
         String hotelName) throws Exception {
      String request = "SEND VACANCY ";
      String details = MessageFormat.format(
            "{0}={1},{2}={3},{4}={5},{6}={7},{8}={9},{10}={11},{12}={13}",
            ClientHopp.SEND_FIELD_CHECKIN_YEAR,
            vacancyDetails.get(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR),
            ClientHopp.SEND_FIELD_CHECKIN_MONTH,
            vacancyDetails.get(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH),
            ClientHopp.SEND_FIELD_CHECKIN_DAY,
            vacancyDetails.get(UserInterface.FORM_FIELDNAME_CHECKIN_DAY),
            ClientHopp.SEND_FIELD_CHECKOUT_YEAR,
            vacancyDetails.get(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR),
            ClientHopp.SEND_FIELD_CHECKOUT_MONTH,
            vacancyDetails.get(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH),
            ClientHopp.SEND_FIELD_CHECKOUT_DAY,
            vacancyDetails.get(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY),
            ClientHopp.SEND_FIELD_HOTEL, hotelName);

      request = request.concat(details);
      request = request.trim();
      this.writer.print(request + "\r\n");
      this.writer.flush();

      String reply;
      reply = this.reader.readLine();
      String[] words = reply.split(" ");

      if (words[0].equals("SUCCESS")) {
         return true;
      } else if (words[0].equals("FAIL")) {
         return false;
      } else {
         throw new Exception("Error: Broker failed to process request.");
      }
   }
}
