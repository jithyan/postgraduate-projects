import java.util.HashMap;

/**
 * Class for validating user input
 * 
 * @author Moody
 *
 */
public abstract class InputValidator {
   /** A mapping of the input to be validated and the validation rule */
   private HashMap<String, String> validInput;


   public InputValidator(HashMap<String, String> validInput) {
      this.validInput = validInput;
   }


   public HashMap<String, String> getValidInput() {
      return validInput;
   }


   public void setValidInput(HashMap<String, String> validInput) {
      this.validInput = validInput;
   }
}
