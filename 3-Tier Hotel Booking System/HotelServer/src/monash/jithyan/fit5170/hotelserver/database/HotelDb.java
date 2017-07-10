package monash.jithyan.fit5170.hotelserver.database;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

/**
 * Manages the database containing booking and vacancy details.
 * 
 * @author Moody
 *
 */


public class HotelDb {
   /* Filename of the sql script containing the database scheman */
   private final static String SQL_CREATE_TABLE_FILENAME = "db_create_tables.sql";
   /* Filename of the database */
   private final static String SQL_DATABASE_FILENAME = "hotelbooking.db";
   private final static String JDBC_NAME = "jdbc:sqlite:" + SQL_DATABASE_FILENAME;
   /* Filename of the sql script that would populate the database with default
    * values */
   private final static String SQL_POPULATE_DB = "db_populate_tables.sql";
   private final static String SQLITE_PACKAGENAME = "org.sqlite.JDBC";

   private static HotelDb hotelDb = null;


   private HotelDb() throws ClassNotFoundException, SQLException {
      File file = new File("hotelbooking.db");
      Class.forName(SQLITE_PACKAGENAME);

      if (file.exists() != true) {
         System.out.println("Database not found, creating database.. ");
         setupDbTables();
         System.out.println(
               "Database successfully created and populated with initial values.");
      } else {
         System.out.println("Database found and ready to use.");
      }

   }


   /**
    * Loads the SQLite database for the hotel. In the event it does not exist, a
    * new database is created with default values.
    * 
    * @return A singleton instance of HotelDb
    * @throws ClassNotFoundException
    *            - The SQLite driver could not be loaded.
    * @throws SQLException
    *            - The SQL scripts on the hotel server could not be executed
    *            successfully.
    */
   public synchronized static HotelDb createHotelDb()
         throws ClassNotFoundException, SQLException {
      if (HotelDb.hotelDb == null) {
         return new HotelDb();
      } else {
         return HotelDb.hotelDb;
      }
   }


   /**
    * Create a new database and populate with default values.
    * 
    * @throws SQLException
    *            - The SQL scripts on the hotel server could not be executed
    *            successfully.
    */
   private void setupDbTables() throws SQLException {
      Connection conn = null;
      Statement stmt = null;
      try {
         String sqlScript;
         conn = DriverManager.getConnection(JDBC_NAME);
         stmt = conn.createStatement();
         sqlScript = loadSqlScript(SQL_CREATE_TABLE_FILENAME);
         stmt.executeUpdate(sqlScript);
         sqlScript = loadSqlScript(SQL_POPULATE_DB);
         stmt.executeUpdate(sqlScript);
      } finally {
         if (stmt != null) stmt.close();
         if (conn != null) conn.close();
      }
   }


   /**
    * Executes an update on the database.
    * 
    * @param sqlScript
    *           - A sql script that modifies the database.
    * @throws SQLException
    *            - The given sql script is invalid.
    */
   public synchronized void runUpdate(String sqlScript) throws SQLException {
      Connection conn = null;
      Statement stmt = null;

      try {
         conn = DriverManager.getConnection(JDBC_NAME);
         stmt = conn.createStatement();
         stmt.executeUpdate(sqlScript);
      } finally {
         if (stmt != null) stmt.close();
         if (conn != null) conn.close();
      }
   }


   /**
    * Executes a select sql query.
    * 
    * @param sqlScript
    *           - A SELECT sql script.
    * @return - The rows from running the given sql script.
    * @throws SQLException-
    *            The given sql script is invalid.
    */
   public LinkedList<HashMap<String, String>> runQuery(String sqlScript)
         throws SQLException {
      Connection conn = null;
      Statement stmt = null;
      ResultSet rs = null;
      LinkedList<HashMap<String, String>> results = new LinkedList<HashMap<String, String>>();

      try {
         conn = DriverManager.getConnection(JDBC_NAME);
         stmt = conn.createStatement();
         rs = stmt.executeQuery(sqlScript);

         while (rs.next()) {
            HashMap<String, String> row = new HashMap<String, String>(2, 1);
            row.put("date", rs.getString("date"));
            row.put("vacant", rs.getString("vacant"));
            results.add(row);
         }
         return results;

      } finally {
         if (stmt != null) stmt.close();
         if (conn != null) conn.close();
         if (rs != null) rs.close();
      }
   }


   /**
    * Loads a sql script from a file and returns it as a single string.
    * 
    * @param filename
    *           - Filename of the sql script to load.
    * @return A String containing the sql script as a single line.
    */
   private static String loadSqlScript(final String filename) {
      String sqlScript = new String("");
      Path path = Paths.get(filename);

      try {
         List<String> strings = Files.readAllLines(path, StandardCharsets.UTF_8);

         for (String s : strings) {
            sqlScript = sqlScript.concat(s);
         }
      } catch (IOException e) {
         e.printStackTrace();
         System.out.println("Couldn't open file!");
      }

      return sqlScript;
   }


   @Override
protected void finalize() throws Throwable {
      HotelDb.hotelDb = null;
   }
}
