package monash.jithyan.fit5170.hotelbroker;

import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Set;

/**
 * Formats a given HashMap of field names to values into a single line of text
 * compliant with the protocol of requesting a booking.
 * 
 * @author Moody
 *
 */
public class BookingRequestMessage extends HotelMessage {
   /* A single line consisting of given values formatted into the protocol for
    * requesting a booking with a hotel server. */
   String bookingMessage;


   /**
    * 
    * @param bookingDetails
    *           A Hash mapping of field names to values for a booking.
    * @throws Exception
    *            Insufficient or incorrect field names given in the keyset.
    */
   public BookingRequestMessage(HashMap<String, String> bookingDetails) throws Exception {
      Set<String> fields = bookingDetails.keySet();
      fields.remove("hotel");
      if (fields.containsAll(HotelMessage.bookingProtocolKeywords)) {
         this.bookingMessage = MessageFormat.format(
               "BOOK guest_name=''{0}'',checkin_date=''{1}-{2}-{3}'',checkout_date=''{4}-{5}-{6}'',phone=''{7}'',email=''{8}'',credit_card=''{9}''\r\n",
               bookingDetails.get("guest_name"), bookingDetails.get("checkin_year"),
               bookingDetails.get("checkin_month"), bookingDetails.get("checkin_day"),
               bookingDetails.get("checkout_year"), bookingDetails.get("checkout_month"),
               bookingDetails.get("checkout_day"), bookingDetails.get("phone"),
               bookingDetails.get("email"), bookingDetails.get("credit_card"));
      } else {
         throw new Exception("Unrecognized or insufficient protocol words present.");
      }
   }


   /**
    * A single line consisting of given values formatted into the protocol for
    * requesting a booking with a hotel server.
    */
   public String getRequest() {
      return this.bookingMessage;
   }
}
