package monash.jithyan.fit5170.hotelbroker;

import java.util.HashMap;

public class BrokerServerHopp {
   private final static String RESPONSE_SUCCESS = "SUCCESS ";
   private final static String RESPONSE_FAIL = "FAIL ";
   private final static String RESPONSE_ERROR = "ERROR ";


   /**
    * Processes a GET request, which is a request for information that is stored
    * on the broker.
    * 
    * @param getLine
    *           The client request.
    * @param hotels
    *           Information about hotels serviced by the broker.
    * @return On Success: A list of hotels or cities. A fail response is sent if
    *         there is something goes wrong.
    */
   public String processGetRequest(String getLine, HotelManager hotels) {
      String[] request = getLine.split(" ");
      String response;

      if (request[1].startsWith("city")) {
         request = request[1].split("=");

         if (request[1].equals("ANY")) {
            response = BrokerServerHopp.RESPONSE_SUCCESS;

            for (String hotelName : hotels.getCitiesServed()) {
               response = response.concat(hotelName.concat(","));
            }

            return response.replaceAll(",$", "");

         } else if (hotels.cityExists(request[1])) {
            response = BrokerServerHopp.RESPONSE_SUCCESS;

            for (String hotelName : hotels.hotelsInCity(request[1])) {
               response = response.concat(hotelName.concat(","));
            }

            return response.replaceAll(",$", "");

         } else {
            return BrokerServerHopp.RESPONSE_FAIL
                  + "city is not served or unrecognized value";
         }
      } else {
         return BrokerServerHopp.RESPONSE_FAIL + "unrecognized GET request";
      }
   }


   /**
    * Processes a SEND request, which needs to be forwarded to a specific hotel
    * server. on the broker. It either checks for vacancy or makes a booking
    * between specified dates.
    * 
    * @param sendLine
    *           The client request.
    * @param hotels
    *           Information about hotels serviced by the broker.
    * @return Response from the hotel: Success if booking is made or days are
    *         vacant. Fail if dates for booking or vacancy check are not vacant.
    *         Error if something went wrong.
    */
   public String processSendRequest(String sendLine, HotelManager hotels) {
      HashMap<String, String> messageValues = new HashMap<String, String>(11, 1);
      String[] request = sendLine.split(" ");
      String[] requestDetails;
      String[] fieldNameAndValue;
      HashMap<Integer, String> hotelInfo = null;
      String hotelResponse = null;

      if ((request[1].startsWith("BOOKING")) || (request[1].startsWith("VACANCY"))) {
         sendLine = sendLine.replaceAll("^SEND (BOOKING|VACANCY)? ", "");
         requestDetails = sendLine.split(",");

         for (String s : requestDetails) {
            fieldNameAndValue = s.split("=");
            messageValues.put(fieldNameAndValue[0], fieldNameAndValue[1]);
         }

         if (hotels.hotelExists(messageValues.get("hotel"))) {
            try {
               hotelInfo = hotels.getHotelInformation(messageValues.get("hotel"));
            } catch (Exception e) {
               return BrokerServerHopp.RESPONSE_FAIL + " " + e.getMessage();
            }
         }

      } else {
         return BrokerServerHopp.RESPONSE_FAIL + " unrecognized SEND request";
      }

      if (request[1].startsWith("BOOKING")) {
         try {
            hotelResponse = BrokerClientHopp.sendRequestToHotelServer(
                  hotelInfo.get(HotelManager.HOTEL_IP),
                  hotelInfo.get(HotelManager.HOTEL_PORT),
                  new BookingRequestMessage(messageValues));
         } catch (Exception e) {
            System.out.println("i got here");
            return BrokerServerHopp.RESPONSE_FAIL + " Failed to get response from hotel: "
                  + e.getMessage();
         }

      } else if (request[1].startsWith("VACANCY")) {
         try {
            System.out.println(hotelInfo.get(HotelManager.HOTEL_PORT) + ","
                  + hotelInfo.get(HotelManager.HOTEL_IP));

            hotelResponse = BrokerClientHopp.sendRequestToHotelServer(
                  hotelInfo.get(HotelManager.HOTEL_IP),
                  hotelInfo.get(HotelManager.HOTEL_PORT),
                  new VacancyRequestMessage(messageValues));
         } catch (Exception e) {
            return BrokerServerHopp.RESPONSE_FAIL + " Failed to get response from hotel: "
                  + e.getMessage();
         }
      }

      for (String s : hotelResponse.split(" ")) {
         if (s.equals("SUCCESS")) {
            return BrokerServerHopp.RESPONSE_SUCCESS;
         } else if (s.equals("FAIL")) {
            return BrokerServerHopp.RESPONSE_FAIL;
         } else if (s.equals("ERROR")) {
            return BrokerServerHopp.RESPONSE_ERROR;
         }
      }

      return BrokerServerHopp.RESPONSE_ERROR;

   }
}
