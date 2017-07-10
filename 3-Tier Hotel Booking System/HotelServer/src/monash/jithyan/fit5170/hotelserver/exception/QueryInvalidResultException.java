
/**
 * An exception thrown when there is an issue with provided date values for a
 * sql script.
 * 
 * @author Moody
 *
 */

package monash.jithyan.fit5170.hotelserver.exception;

public class QueryInvalidResultException extends Exception {
   private static final long serialVersionUID = -156196647354749190L;


   public QueryInvalidResultException(String message) {
      super(message);
   }

}
