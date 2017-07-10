import java.util.HashMap;

/**
 * Validates user input against validation rules for the fields in a booking
 * form.
 * 
 * @author Moody
 *
 */
public class BookingInputValidator extends FormInputValidator {


   public BookingInputValidator(HashMap<String, String> vInput) {
      super(null);
      HashMap<String, String> validInput = new HashMap<String, String>(12, 1);

      validInput.put(UserInterface.FORM_FIELDNAME_GUEST_NAME, "^[\\w ]{3,50}");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, "^2016");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, "^07");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY,
            "^(([0][1-9])|([1-2][0-9])|([3][0-1]))");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, "^2016");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, "^07");
      validInput.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY,
            "^(([0][1-9])|([1-2][0-9])|([3][0-1]))");
      validInput.put(UserInterface.FORM_FIELDNAME_PHONE, "\\d{10,12}");
      validInput.put(UserInterface.FORM_FIELDNAME_EMAIL,
            "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?");
      validInput.put(UserInterface.FORM_FIELDNAME_CREDIT_CARD, "\\d{11,15}");

      super.setValidInput(validInput);
   }


   @Override
   public boolean validateInput(String input, String fieldName) {
      if (fieldName != UserInterface.FORM_FIELDNAME_CREDIT_CARD) {
         return input.matches(super.getValidInput().get(fieldName));
      } else {
         if (input.matches(
               super.getValidInput().get(UserInterface.FORM_FIELDNAME_CREDIT_CARD))) {
            return luhnTest(input);
         } else {
            return false;
         }
      }
   }


   /* Taken from:
    * https://www.rosettacode.org/wiki/Luhn_test_of_credit_card_numbers#Java */
   private static boolean luhnTest(String number) {
      int s1 = 0, s2 = 0;
      String reverse = new StringBuffer(number).reverse().toString();

      for (int i = 0; i < reverse.length(); i++) {
         int digit = Character.digit(reverse.charAt(i), 10);
         if (i % 2 == 0) {
            s1 += digit;
         } else {
            s2 += 2 * digit;
            if (digit >= 5) {
               s2 -= 9;
            }
         }
      }

      return (s1 + s2) % 10 == 0;
   }

}
