package rushhour;

import java.sql.*;

public class SQLiteJDBC
{
  public static void main( String args[] )
  {
    Connection c = null;
    Statement stmt = null;
    try {
      Class.forName("org.sqlite.JDBC");
      c = DriverManager.getConnection("jdbc:sqlite:C:\\Users\\cliff\\workspace\\rushHour\\Data Model and SQL\\Schema Definition and Bulk Load\\rush_hour.db");
      c.setAutoCommit(false);
      System.out.println("Opened database successfully");

      stmt = c.createStatement();
      ResultSet rs = stmt.executeQuery( "SELECT * from  game_state limit 3;" );
      while ( rs.next() ) {
         int game_number = rs.getInt(1);
//         String  name = rs.getString("name");
//         int age  = rs.getInt("age");
//         String  address = rs.getString("address");
//         float salary = rs.getFloat("salary");
//         System.out.println( "ID = " + id );
         System.out.println( "Game Number = " + game_number );
//         System.out.println( "AGE = " + age );
//         System.out.println( "ADDRESS = " + address );
//         System.out.println( "SALARY = " + salary );
         System.out.println();
      }
      rs.close();
      stmt.close();
      c.close();
    } catch ( Exception e ) {
      System.err.println( e.getClass().getName() + ": " + e.getMessage() );
      System.exit(0);
    }
    System.out.println("Operation done successfully");
  }
}