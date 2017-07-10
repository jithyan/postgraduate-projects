import java.util.HashMap;

public class SoloTester {
   public static void main(String[] args) {
      Thread[] t = new Thread[72];
      t[0] = new Thread(new SoloTester().new HolidayInnTestBooking("01", "04"));
      t[1] = new Thread(new SoloTester().new HolidayInnTestBooking("03", "04"));
      t[2] = new Thread(new SoloTester().new HolidayInnTestBooking("30", "31"));
      t[3] = new Thread(new SoloTester().new HolidayInnTestBooking("28", "28"));
      t[4] = new Thread(new SoloTester().new HolidayInnTestBooking("03", "07"));
      t[5] = new Thread(new SoloTester().new HolidayInnTestBooking("09", "10"));
      t[6] = new Thread(new SoloTester().new HolidayInnTestBooking("13", "14"));
      t[7] = new Thread(new SoloTester().new HolidayInnTestBooking("12", "15"));
      t[8] = new Thread(new SoloTester().new HolidayInnTestBooking("11", "11"));
      t[9] = new Thread(new SoloTester().new HolidayInnTestBooking("19", "20"));
      t[10] = new Thread(new SoloTester().new HolidayInnTestBooking("21", "22"));
      t[11] = new Thread(new SoloTester().new HolidayInnTestBooking("23", "24"));
      t[12] = new Thread(new SoloTester().new HolidayInnTestBooking("25", "26"));
      t[13] = new Thread(new SoloTester().new HolidayInnTestBooking("20", "22"));
      t[14] = new Thread(new SoloTester().new HolidayInnTestBooking("29", "30"));
      t[15] = new Thread(new SoloTester().new HolidayInnTestBooking("07", "09"));
      t[16] = new Thread(new SoloTester().new HolidayInnTestBooking("12", "13"));
      t[17] = new Thread(new SoloTester().new HolidayInnTestBooking("14", "15"));
      t[18] = new Thread(new SoloTester().new HolidayInnTestBooking("29", "30"));
      t[19] = new Thread(new SoloTester().new HolidayInnTestBooking("16", "16"));
      t[20] = new Thread(new SoloTester().new HolidayInnTestBooking("18", "20"));
      t[21] = new Thread(new SoloTester().new HolidayInnTestBooking("19", "22"));
      t[22] = new Thread(new SoloTester().new HolidayInnTestBooking("26", "27"));
      t[23] = new Thread(new SoloTester().new HolidayInnTestBooking("25", "27"));

      t[24] = new Thread(new SoloTester().new GrandHyattTestBooking("01", "04"));
      t[25] = new Thread(new SoloTester().new GrandHyattTestBooking("03", "04"));
      t[26] = new Thread(new SoloTester().new GrandHyattTestBooking("30", "31"));
      t[27] = new Thread(new SoloTester().new GrandHyattTestBooking("28", "28"));
      t[28] = new Thread(new SoloTester().new GrandHyattTestBooking("03", "07"));
      t[29] = new Thread(new SoloTester().new GrandHyattTestBooking("09", "10"));
      t[30] = new Thread(new SoloTester().new GrandHyattTestBooking("13", "14"));
      t[31] = new Thread(new SoloTester().new GrandHyattTestBooking("12", "15"));
      t[32] = new Thread(new SoloTester().new GrandHyattTestBooking("11", "11"));
      t[33] = new Thread(new SoloTester().new GrandHyattTestBooking("19", "20"));
      t[34] = new Thread(new SoloTester().new GrandHyattTestBooking("21", "22"));
      t[35] = new Thread(new SoloTester().new GrandHyattTestBooking("23", "24"));
      t[36] = new Thread(new SoloTester().new GrandHyattTestBooking("25", "26"));
      t[37] = new Thread(new SoloTester().new GrandHyattTestBooking("20", "22"));
      t[38] = new Thread(new SoloTester().new GrandHyattTestBooking("29", "30"));
      t[39] = new Thread(new SoloTester().new GrandHyattTestBooking("07", "09"));
      t[40] = new Thread(new SoloTester().new GrandHyattTestBooking("12", "13"));
      t[41] = new Thread(new SoloTester().new GrandHyattTestBooking("14", "15"));
      t[42] = new Thread(new SoloTester().new GrandHyattTestBooking("29", "30"));
      t[43] = new Thread(new SoloTester().new GrandHyattTestBooking("16", "16"));
      t[44] = new Thread(new SoloTester().new GrandHyattTestBooking("18", "20"));
      t[45] = new Thread(new SoloTester().new GrandHyattTestBooking("19", "22"));
      t[46] = new Thread(new SoloTester().new GrandHyattTestBooking("26", "27"));
      t[47] = new Thread(new SoloTester().new GrandHyattTestBooking("25", "27"));

      t[48] = new Thread(new SoloTester().new RitzCarltonTestBooking("01", "04"));
      t[49] = new Thread(new SoloTester().new RitzCarltonTestBooking("03", "04"));
      t[50] = new Thread(new SoloTester().new RitzCarltonTestBooking("30", "31"));
      t[51] = new Thread(new SoloTester().new RitzCarltonTestBooking("28", "28"));
      t[52] = new Thread(new SoloTester().new RitzCarltonTestBooking("03", "07"));
      t[53] = new Thread(new SoloTester().new RitzCarltonTestBooking("09", "10"));
      t[54] = new Thread(new SoloTester().new RitzCarltonTestBooking("13", "14"));
      t[55] = new Thread(new SoloTester().new RitzCarltonTestBooking("12", "15"));
      t[56] = new Thread(new SoloTester().new RitzCarltonTestBooking("11", "11"));
      t[57] = new Thread(new SoloTester().new RitzCarltonTestBooking("19", "20"));
      t[58] = new Thread(new SoloTester().new RitzCarltonTestBooking("21", "22"));
      t[59] = new Thread(new SoloTester().new RitzCarltonTestBooking("23", "24"));
      t[60] = new Thread(new SoloTester().new RitzCarltonTestBooking("25", "26"));
      t[61] = new Thread(new SoloTester().new RitzCarltonTestBooking("20", "22"));
      t[62] = new Thread(new SoloTester().new RitzCarltonTestBooking("29", "30"));
      t[63] = new Thread(new SoloTester().new RitzCarltonTestBooking("07", "09"));
      t[64] = new Thread(new SoloTester().new RitzCarltonTestBooking("12", "13"));
      t[65] = new Thread(new SoloTester().new RitzCarltonTestBooking("14", "15"));
      t[66] = new Thread(new SoloTester().new RitzCarltonTestBooking("29", "30"));
      t[67] = new Thread(new SoloTester().new RitzCarltonTestBooking("16", "16"));
      t[68] = new Thread(new SoloTester().new RitzCarltonTestBooking("18", "20"));
      t[69] = new Thread(new SoloTester().new RitzCarltonTestBooking("19", "22"));
      t[70] = new Thread(new SoloTester().new RitzCarltonTestBooking("26", "27"));
      t[71] = new Thread(new SoloTester().new RitzCarltonTestBooking("25", "27"));

      for (int i = 0; i < 10; i++) {
         int j = (int) (Math.random() * 23.0);

         if ((t[j].isAlive()) || t[j].getState().equals(Thread.State.TERMINATED)) {
            i--;
         } else {
            System.out.println(j);
            t[j].start();
         }
      }

      for (int i = 0; i < 10; i++) {
         int j = (int) (Math.random() * 23.0) + 23;
         if ((t[j].isAlive()) || t[j].getState().equals(Thread.State.TERMINATED)) {
            i--;
         } else {
            System.out.println(j);
            t[j].start();
         }
      }

      for (int i = 0; i < 10; i++) {
         int j = (int) (Math.random() * 23.0) + 46;
         if ((t[j].isAlive()) || t[j].getState().equals(Thread.State.TERMINATED)) {
            i--;
         } else {
            System.out.println(j);
            t[j].start();
         }
      }


   }


   public class GrandHyattTestBooking implements Runnable {
      private HashMap<String, String> entryFields;


      public GrandHyattTestBooking(String checkinDay, String checkoutDay) {
         this.entryFields = new HashMap<String, String>(12, 1);
         entryFields.put(UserInterface.FORM_FIELDNAME_GUEST_NAME,
               "dweebjohn " + checkinDay + checkoutDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, "2016");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, "07");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY, checkinDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, "2016");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, "07");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, checkoutDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_PHONE, "1234567890");
         entryFields.put(UserInterface.FORM_FIELDNAME_EMAIL, "1234567890@bub.com");
         entryFields.put(UserInterface.FORM_FIELDNAME_CREDIT_CARD, "1234567889");
      }


      @Override
      public void run() {
         ClientHopp hopp = new ClientHopp();
         try {
            Thread.sleep((long) (Math.random() * 1000));
         } catch (InterruptedException e1) {
            e1.printStackTrace();
         }
         try {
            if (hopp.sendCheckVacancy(entryFields, "Grand Hyatt Hotel")) {
               System.out.print(hopp.sendBooking(entryFields, "Grand Hyatt Hotel")
                     + " (Grand Hyatt Hotel) \n");
            } else {
               System.out.println("Didn't bother booking, not vacant.");
            }
         } catch (Exception e) {
            System.out.println(e.getMessage());
         }
      }
   }


   public class RitzCarltonTestBooking implements Runnable {
      private HashMap<String, String> entryFields;


      public RitzCarltonTestBooking(String checkinDay, String checkoutDay) {
         this.entryFields = new HashMap<String, String>(12, 1);
         entryFields.put(UserInterface.FORM_FIELDNAME_GUEST_NAME,
               "dweebjohn " + checkinDay + checkoutDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, "2016");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, "07");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY, checkinDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, "2016");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, "07");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, checkoutDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_PHONE, "1234567890");
         entryFields.put(UserInterface.FORM_FIELDNAME_EMAIL, "1234567890@bub.com");
         entryFields.put(UserInterface.FORM_FIELDNAME_CREDIT_CARD, "1234567889");
      }


      @Override
      public void run() {
         ClientHopp hopp = new ClientHopp();
         try {
            Thread.sleep((long) (Math.random() * 1000));
         } catch (InterruptedException e1) {
            e1.printStackTrace();
         }
         try {
            if (hopp.sendCheckVacancy(entryFields, "Ritz Carlton")) {
               System.out.print(hopp.sendBooking(entryFields, "Ritz Carlton")
                     + " (Ritz Carlton) \n");
            } else {
               System.out.println("Didn't bother booking, not vacant.");
            }
         } catch (Exception e) {
            System.out.println(e.getMessage());
         }
      }
   }


   public class HolidayInnTestBooking implements Runnable {
      private HashMap<String, String> entryFields;


      public HolidayInnTestBooking(String checkinDay, String checkoutDay) {
         this.entryFields = new HashMap<String, String>(12, 1);
         entryFields.put(UserInterface.FORM_FIELDNAME_GUEST_NAME,
               "dweebjohn " + checkinDay + checkoutDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_YEAR, "2016");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_MONTH, "07");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKIN_DAY, checkinDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_YEAR, "2016");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_MONTH, "07");
         entryFields.put(UserInterface.FORM_FIELDNAME_CHECKOUT_DAY, checkoutDay);
         entryFields.put(UserInterface.FORM_FIELDNAME_PHONE, "1234567890");
         entryFields.put(UserInterface.FORM_FIELDNAME_EMAIL, "1234567890@bub.com");
         entryFields.put(UserInterface.FORM_FIELDNAME_CREDIT_CARD, "1234567889");
      }


      @Override
      public void run() {
         ClientHopp hopp = new ClientHopp();
         try {
            Thread.sleep((long) (Math.random() * 1000));
         } catch (InterruptedException e1) {
            e1.printStackTrace();
         }
         try {
            if (hopp.sendCheckVacancy(entryFields, "Holiday Inn")) {
               System.out.print(
                     hopp.sendBooking(entryFields, "Holiday Inn") + " (Holiday Inn) \n");
            } else {
               System.out.println("Didn't bother booking, not vacant.");
            }
         } catch (Exception e) {
            System.out.println(e.getMessage());
         }
      }
   }
}
