
/**
 * This exception is thrown when a booking cannot be completed as the given
 * dates are not vacant.
 * 
 * @author Moody
 *
 */
package monash.jithyan.fit5170.hotelserver.exception;

public class InvalidBookingException extends Exception {
   private static final long serialVersionUID = 4627529768238987625L;


   public InvalidBookingException(String message) {
      super(message);
   }

}
