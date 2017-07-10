package monash.jithyan.fit5170.hotelserver;

import java.sql.SQLException;
import java.text.MessageFormat;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;

import monash.jithyan.fit5170.hotelserver.database.HotelDb;
import monash.jithyan.fit5170.hotelserver.exception.InvalidBookingException;
import monash.jithyan.fit5170.hotelserver.exception.QueryInvalidResultException;


/**
 * Handles the logic of the services offered by the hotel server.
 * 
 * @author Moody
 *
 */

public class HotelServerHopp {
   private Object lock;


   public HotelServerHopp(Object lock) {
      this.lock = lock;
   }


   /**
    * Determines if all the days between the specified dates are vacant.
    * 
    * @param checkinDate
    * @param checkoutDate
    * @param db
    *           - The database manager for the hotel server
    * @return true - The given dates are vacant and can be booked. false - Some
    *         or all the days between the given dates are not vacant.
    * @throws QueryInvalidResultException
    *            - The query brought no results, indicating the dates specified
    *            are not in the database.
    * @throws SQLException
    *            - Invalid values in the SQL script.
    */
   public boolean checkVacancy(String checkinDate, String checkoutDate, HotelDb db)
         throws QueryInvalidResultException, SQLException {
      String sqlScript = MessageFormat.format(
            "SELECT * FROM vacancy WHERE date BETWEEN {0} AND {1};", checkinDate,
            checkoutDate);
      LinkedList<HashMap<String, String>> results = null;

      results = db.runQuery(sqlScript);

      if (results.isEmpty() != true) {
         Iterator<HashMap<String, String>> rows = results.iterator();
         while (rows.hasNext()) {
            HashMap<String, String> row = rows.next();
            if (row.get("vacant").equals("0")) {
               return false;
            }
         }
         return true;
      } else {
         throw new QueryInvalidResultException(
               "Query didn't return any results. Dates are probably invalid.");
      }

   }


   /**
    * Register a customer's booking details.
    * 
    * @param booking_details
    *           - A mapping of field names to values, which are required for a
    *           booking.
    * @param db
    *           - The database manager for the hotel server
    * @throws InvalidBookingException
    *            - The given dates are not vacant. Booking cannot be done.
    * @throws QueryInvalidResultException
    *            - The query brought no results, indicating the dates specified
    *            are not in the database.
    * @throws SQLException-
    *            Invalid values in the SQL script.
    */
   public void registerBooking(HashMap<String, String> booking_details, HotelDb db)
         throws InvalidBookingException, QueryInvalidResultException, SQLException {
      String sqlScript = "UPDATE vacancy SET vacant=0 WHERE date BETWEEN "
            + booking_details.get("checkin_date") + " AND "
            + booking_details.get("checkout_date") + ";";
      boolean isVacant = false;

      synchronized (lock) {
         isVacant = checkVacancy(booking_details.get("checkin_date"),
               booking_details.get("checkout_date"), db);
         if (isVacant) {
            db.runUpdate(sqlScript);
            sqlScript = MessageFormat.format(
                  "INSERT INTO booking (booking_id, checkin_date, checkout_date, phone, email, credit_card, guest_name) VALUES(NULL, date({0}), date({1}), {2}, {3}, {4}, {5});",
                  booking_details.get("checkin_date"),
                  booking_details.get("checkout_date"), booking_details.get("phone"),
                  booking_details.get("email"), booking_details.get("credit_card"),
                  booking_details.get("guest_name"));
            db.runUpdate(sqlScript);
         }
      }

      if (!isVacant) throw new InvalidBookingException(
            "Booking failed. Specified dates have been booked.");
   }

}
