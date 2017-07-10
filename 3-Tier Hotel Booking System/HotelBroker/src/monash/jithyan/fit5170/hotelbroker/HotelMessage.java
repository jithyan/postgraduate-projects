package monash.jithyan.fit5170.hotelbroker;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashSet;
import java.util.List;

/**
 * Formats values into the protocol to communicate with hotel servers.
 * 
 * @author Moody
 *
 */
public abstract class HotelMessage {
   public static HashSet<String> bookingProtocolKeywords;
   public static HashSet<String> vacancyProtocolKeywords;


   public abstract String getRequest();


   /**
    * Load the fields in the protocol from the file.
    */
   public static void initializeProtocolWords() {
      Path path = Paths.get("protocol.txt");
      List<String> lines;
      String[] keyWords;
      HashSet<String> keyWordSet = new HashSet<String>();

      try {
         lines = Files.readAllLines(path, StandardCharsets.UTF_8);
         for (String line : lines) {
            line = line.replaceAll("\\r\\n", "");
            keyWords = line.split(" ");
            for (int i = 1; i < keyWords.length; i++) {
               keyWordSet.add(keyWords[i]);
            }

            if (line.startsWith("BOOK")) {
               HotelMessage.bookingProtocolKeywords = keyWordSet;
            } else if (line.startsWith("VACANCY")) {
               HotelMessage.vacancyProtocolKeywords = keyWordSet;
            }

            keyWordSet = new HashSet<String>();
         }
      } catch (Exception e) {
         System.out.println(
               "Something went wrong reading the protocol file: " + e.getMessage());
         System.exit(1);
      }
   }
}
