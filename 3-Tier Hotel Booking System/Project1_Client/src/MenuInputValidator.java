import java.util.HashMap;

/**
 * Validates user input for menu options
 * 
 * @author Moody
 *
 */
public class MenuInputValidator extends InputValidator {

   public MenuInputValidator(HashMap<String, String> validOptions) {
      super(validOptions);
   }


   public boolean validateInput(String input) {
      return super.getValidInput().containsKey(input);
   }
}
