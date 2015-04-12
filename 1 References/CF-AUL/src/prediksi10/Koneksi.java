package prediksi10;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Koneksi {
    private Statement statement = null;
    private Connection con = null;
    private ResultSet rs= null;

    public Koneksi() throws Exception {
        try{
            Class.forName("com.mysql.jdbc.Driver");
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
        try{
            con = DriverManager.getConnection("jdbc:mysql://localhost/cf_db", "root", "");
            statement = con.createStatement();
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
    }

    public ResultSet getAll(String query) throws SQLException {
        try{
            rs=statement.executeQuery(query);
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
        return rs;
    }

    public void save(String query) throws SQLException {
        statement.executeUpdate(query);
    }
}
