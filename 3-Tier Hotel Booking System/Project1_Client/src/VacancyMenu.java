import java.io.BufferedReader;
import java.io.IOException;
import java.util.GregorianCalendar;
import java.util.HashMap;

/**
 * Displays a form for the user to input the dates for checking the vacancy of a
 * specific hotel. The details are validated and sent to the broker for
 * processing. The user is informed if the dates are vacant or not.
 * 
 * @author Moody
 *
 */
public class VacancyMenu extends InputFormMenu {

   public VacancyMenu(BufferedReader br, ClientHopp hopp, RootMenu previous,
         String hotelName) {
      super(br, hopp, previous, hotelName);

      HashMap<String, String> entryFields = new HashMap<String, String>(12, 1);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, null);
      super.setEntryFields(entryFields);

      String[] fieldsOrdered = { UserInterface.FORM_FIELDNAME_CHECKIN_YEAR,
            UserInterface.FORM_FIELDNAME_CHECKIN_MONTH,
            UserInterface.FORM_FIELDNAME_CHECKIN_DAY,
            UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR,
            UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH,
            UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, };
      super.setInputFieldsOrdered(fieldsOrdered);

      super.setValidator(new CheckVacancyInputValidator(null));

   }


   @Override
   public RootMenu go() {
      String input;
      CheckVacancyInputValidator validator = (CheckVacancyInputValidator) super.getValidator();
      UserInterface.printMenuHeader("Check Vacancy for " + super.getHotelName());

      for (String fieldName : super.getInputFieldsOrdered()) {
         while (true) {
            input = getUserInput(fieldName + ": ");

            if (validator.validateInput(input, fieldName) == true) {

               super.getEntryFields().put(fieldName, input);
               break;

            } else {
               System.out.println("Invalid input! Try again.");
            }
         }
      }

      int checkinDay = Integer.parseInt(
            super.getEntryFields().get(UserInterface.FORM_FIELDNAME_CHECKIN_DAY));
      int checkinMonth = Integer.parseInt(
            super.getEntryFields().get(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH)) - 1;
      int checkinYear = Integer.parseInt(
            super.getEntryFields().get(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR));
      int checkoutDay = Integer.parseInt(
            super.getEntryFields().get(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY));
      int checkoutMonth = Integer.parseInt(
            super.getEntryFields().get(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH)) - 1;
      int checkoutYear = Integer.parseInt(
            super.getEntryFields().get(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR));
      GregorianCalendar checkinDate = new GregorianCalendar(checkinDay, checkinMonth,
            checkinYear);
      GregorianCalendar checkoutDate = new GregorianCalendar(checkoutDay, checkoutMonth,
            checkoutYear);

      if (checkinDate.after(checkoutDate)) {
         System.out.println(
               "Your checkin date can't be after the checkout date. Redo everything.");
         return this;
      }

      try {
         if (super.getHopp().sendCheckVacancy(super.getEntryFields(),
               super.getHotelName()) == true) {
            UserInterface.printMessageBanner("The selected dates are vacant.");
            return super.getPrevious();
         } else {
            UserInterface.printMessageBanner("The selected dates are not vacant");
            return super.getPrevious();
         }
      } catch (IOException e) {
         System.out.println("Error getting response from broker");
         return this;
      } catch (Exception e) {
         System.out.println(e.getMessage());
         return super.getPrevious();
      }
   }

}
