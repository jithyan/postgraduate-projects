import java.io.BufferedReader;
import java.util.GregorianCalendar;
import java.util.HashMap;

/**
 * Displays a form for the user to input booking details. The details are
 * validated and sent to the broker for processing. The user is informed if the
 * booking is successful or not.
 * 
 * @author Moody
 *
 */
public class BookingMenu extends InputFormMenu {

   public BookingMenu(BufferedReader br, ClientHopp hopp, RootMenu previous,
         String hotelName) {
      super(br, hopp, previous, hotelName);

      HashMap<String, String> entryFields = new HashMap<String, String>(12, 1);
      entryFields.put(UserInterface.FORM_FIELDNAME_GUEST_NAME, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_PHONE, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_EMAIL, null);
      entryFields.put(UserInterface.FORM_FIELDNAME_CREDIT_CARD, null);
      super.setEntryFields(entryFields);

      String[] fieldsOrdered = { UserInterface.FORM_FIELDNAME_GUEST_NAME,
            UserInterface.FORM_FIELDNAME_CHECKIN_YEAR,
            UserInterface.FORM_FIELDNAME_CHECKIN_MONTH,
            UserInterface.FORM_FIELDNAME_CHECKIN_DAY,
            UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR,
            UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH,
            UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, UserInterface.FORM_FIELDNAME_PHONE,
            UserInterface.FORM_FIELDNAME_EMAIL,
            UserInterface.FORM_FIELDNAME_CREDIT_CARD };
      super.setInputFieldsOrdered(fieldsOrdered);

      super.setValidator(new BookingInputValidator(null));
   }


   @Override
   public RootMenu go() {
      String input;
      BookingInputValidator validator = (BookingInputValidator) super.getValidator();

      UserInterface.printMenuHeader("Booking Form for " + super.getHotelName());

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
         if (super.getHopp().sendBooking(super.getEntryFields(),
               super.getHotelName()) == true) {
            UserInterface.printMessageBanner("Booking was a success, congratulations.");
            return new MainMenu(super.getInputReader(), super.getHopp());
         } else {
            UserInterface
                  .printMessageBanner("Booking failed, check vacancy for given dates.");
            return super.getPrevious();
         }
      } catch (Exception e) {
         System.out.println(e.getMessage());
         return super.getPrevious();
      }
   }
}
