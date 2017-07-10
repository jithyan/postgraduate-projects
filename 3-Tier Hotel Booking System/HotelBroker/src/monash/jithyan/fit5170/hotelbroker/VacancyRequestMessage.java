package monash.jithyan.fit5170.hotelbroker;
import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Set;

/**
 * Formats a given HashMap of field names to values into a single line of text
 * compliant with the protocol for checking a vacancy.
 * 
 * @author Moody
 *
 */
public class VacancyRequestMessage extends HotelMessage {
   /* A single line consisting of given values formatted into the protocol for
    * checking a vacancy with a hotel server. */
   private String vacancyMessage;


   public VacancyRequestMessage(HashMap<String, String> vacancyDetails) throws Exception {
      Set<String> fields = vacancyDetails.keySet();
      fields.remove("hotel");

      if (fields.containsAll(HotelMessage.vacancyProtocolKeywords))
         this.vacancyMessage = MessageFormat.format(
               "VACANCY checkin_date=''{0}-{1}-{2}'',checkout_date=''{3}-{4}-{5}''\r\n",
               vacancyDetails.get("checkin_year"), vacancyDetails.get("checkin_month"),
               vacancyDetails.get("checkin_day"), vacancyDetails.get("checkout_year"),
               vacancyDetails.get("checkout_month"), vacancyDetails.get("checkout_day"));
      else {
         throw new Exception("Unrecognized or insufficient protocol words present.");
      }
   }


   @Override
   /* * A single line consisting of given values formatted into the protocol for
    * checking a vacancy with a hotel server. */
   public String getRequest() {
      return this.vacancyMessage;
   }

}
