import java.util.HashMap;

public abstract class FormInputValidator extends InputValidator {

   public FormInputValidator(HashMap<String, String> validInput) {
      super(validInput);
   }


   public boolean validateInput(String input, String fieldName) {
      return input.matches(super.getValidInput().get(fieldName));
   }
}
