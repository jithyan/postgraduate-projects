package monash.jithyan.fit5170.hotelbroker;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;

/**
 * Manages the information about hotels stored on the server. The information is
 * loaded from a text file on the server.
 * 
 * @author Moody
 *
 */
public class HotelManager {
   public final static int HOTEL_NAME = 0;
   public final static int HOTEL_CITY = 1;
   public final static int HOTEL_IP = 2;
   public final static int HOTEL_PORT = 3;

   private static HotelManager hotelManager = null;

   private ArrayList<String[]> hotelDetails;
   private HashSet<String> hotelNames;
   private HashSet<String> citiesServed;
   private String filename;


   private HotelManager(String filename) {
      this.filename = filename;
      Path path = Paths.get(filename);
      List<String> lines;
      String[] details;
      this.hotelDetails = new ArrayList<String[]>();
      this.citiesServed = new HashSet<String>();
      this.hotelNames = new HashSet<String>();

      try {
         lines = Files.readAllLines(path, StandardCharsets.UTF_8);
         for (String line : lines) {
            details = line.split(",");
            this.hotelDetails.add(details);
            hotelNames.add(details[HOTEL_NAME]);
            citiesServed.add(details[HOTEL_CITY]);
         }
      } catch (Exception e) {
         e.printStackTrace();
         System.exit(1);
      }
   }


   public HashSet<String> getCitiesServed() {
      return citiesServed;
   }


   @Override
   protected void finalize() throws Throwable {
      HotelManager.hotelManager = null;
      super.finalize();
   }


   public static synchronized HotelManager createHotelManager(String filename) {
      if (HotelManager.hotelManager == null) {
         return new HotelManager(filename);
      } else {
         return HotelManager.hotelManager;
      }
   }


   /**
    *
    * @param hotelName
    *           Name of the hotel
    * @return Details about the given hotel. The field names for the hashmap are
    *         defined as constants in HotelManager.
    * @throws Exception
    *            Hotel does not exist
    */
   public HashMap<Integer, String> getHotelInformation(String hotelName)
         throws Exception {
      HashMap<Integer, String> hotelInfo = new HashMap<Integer, String>(4, 1);

      for (String[] hotelRow : hotelDetails) {
         if (hotelRow[HOTEL_NAME].equals(hotelName)) {
            hotelInfo.put(HOTEL_NAME, hotelRow[HOTEL_NAME]);
            hotelInfo.put(HOTEL_CITY, hotelRow[HOTEL_CITY]);
            hotelInfo.put(HOTEL_IP, hotelRow[HOTEL_IP]);
            hotelInfo.put(HOTEL_PORT, hotelRow[HOTEL_PORT]);

            return hotelInfo;
         }
      }

      throw new Exception("Given hotel name does not exist!");
   }


   public LinkedList<String> hotelsInCity(String city) {
      LinkedList<String> hotelsInCity = new LinkedList<String>();

      for (String[] hotelRow : hotelDetails) {
         if (city.equals(hotelRow[HotelManager.HOTEL_CITY])) {
            hotelsInCity.add(hotelRow[HotelManager.HOTEL_NAME]);
         }
      }

      return hotelsInCity;

   }


   public boolean hotelExists(String hotelName) {
      return hotelNames.contains(hotelName);
   }


   public boolean cityExists(String cityName) {
      return citiesServed.contains(cityName);
   }


   public synchronized void reloadHotelDetails() {
      Path path = Paths.get(filename);
      List<String> lines;
      String[] details;
      this.hotelDetails = new ArrayList<String[]>();

      try {
         lines = Files.readAllLines(path, StandardCharsets.UTF_8);
         for (String line : lines) {
            details = line.split(",");
            this.hotelDetails.add(details);
            hotelNames.add(details[HOTEL_NAME]);
         }
      } catch (IOException e) {
         System.out.println("Reloading hotel info from file failed: " + e.getMessage());
      }
   }
}
