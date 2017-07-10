import java.util.HashMap;

/** Does validation checking for the fields in the check vacancy menu */
public class CheckVacancyInputValidator extends FormInputValidator {

   public CheckVacancyInputValidator(HashMap<String, String> vInput) {
      super(null);
      HashMap<String, String> validInput = new HashMap<String, String>(8, 1);

      validInput.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, "^\\d{4}");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, "^\\d{1,2}");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY, "^\\d{1,2}");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, "^\\d{4}");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, "^\\d{1,2}");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, "^\\d{1,2}");

      super.setValidInput(validInput);
   }

}
