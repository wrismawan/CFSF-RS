package cfv5;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;

public class DataSmoothing {

    private double data_table[][];
    private ArrayList<User> user;
    private ArrayList<Integer> cluster;

    public void setCluster(ArrayList<Integer> cluster) {
        this.cluster = cluster;
    }

    public ArrayList<Integer> getCluster() {
        return cluster;
    }

    public double[][] getData_table() {
        return data_table;
    }

    public ArrayList<User> getUser() {
        return user;
    }

    public void setUser() {
        HashMap<Integer, User> temp = new HashMap<>();
        ArrayList<User> userList = new ArrayList<>();
        //Bikin list user
        for (int i = 1; i < data_table.length; i++) {
            User u = new User(i);
            temp.put(i, u);
        }

        //Masukin rating item ke list user
        for (int i = 1; i < data_table.length; i++) {
            double[] ds = data_table[i];
            for (int j = 1; j < ds.length - 1; j++) {
                double d = ds[j];
                if (d > 0) {
                    temp.get(i).getItemList().put(j, d);
                    temp.get(i).getKey().add(j);
                }
            }
            temp.get(i).setCluster((int) ds[ds.length - 1]);
        }

        for (int i = 1; i <= temp.size(); i++) {
            userList.add(temp.get(i));
        }

        this.user = userList;
    }

    public void setData_table() {
        BufferedReader br = null;
        ArrayList<String[]> dataS = new ArrayList<>();

        //Open File
        try {
            //Baca File Database RNA
            String sCurrentLine;
            br = new BufferedReader(new FileReader(
                    "E://TA SUKSES/COLLABORATIVE FILTERING/Program/HASIL/Result_Cluster.txt"));
            int i = 0;
            while ((sCurrentLine = br.readLine()) != null) {
                String data[] = sCurrentLine.split("\t");
                dataS.add(data);
                i++;
            }
        } catch (IOException e) {
            System.out.println("Gagal membaca file");
            e.printStackTrace();
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
        int jumUser = dataS.size();
        int jumItem = dataS.get(0).length;
        double data_table[][] = new double[jumUser][jumItem];
        for (int i = 0; i < data_table.length; i++) {
            for (int j = 0; j < data_table[i].length; j++) {
                data_table[i][j] = Double.parseDouble(dataS.get(i)[j]);
            }
        }
        this.data_table = data_table;
    }

    public double getRata2ratingUser(User u) {
        double totRating = 0;
        for (int i = 0; i < u.getItemList().size(); i++) {
            totRating = totRating + u.getItemList().get(u.getKey().get(i));
        }
        return totRating / u.getItemList().size();
    }

    public double getDeltaRCu(User u, int t) {
        double sumA = 0;
        double sizeC = 0;
        for (int i = 0; i < user.size(); i++) {
            User user1 = user.get(i);
            if (user1.getCluster() == u.getCluster() && user1.getKey().contains(t)) {
//                System.out.println("ada");
                sumA += user1.getItemList().get(t) - getRata2ratingUser(user1);
                sizeC++;
            }
        }
        if (sizeC == 0) {
            return 0;
        }else{
            return sumA / sizeC;
        }
//        System.out.print(sizeC + " " + u.getUser_id() + " " + t + " ");
    }

    public double Rut(User u, int t) {
        double Ru = getRata2ratingUser(u);
        double deltaRCu = getDeltaRCu(u, t);
//        System.out.println(Ru + " " + deltaRCu);
        return Ru + deltaRCu;
    }

    public void smoothTwo() {
        for (int i = 1; i < data_table.length; i++) {
            for (int j = 1; j < data_table[i].length - 1; j++) {
                if (data_table[i][j] == 0) {
                    double rating = Rut(this.user.get(i - 1), j);
                    data_table[i][j] = rating;
                }
                System.out.print(data_table[i][j] + "\t");
            }
            System.out.println();
        }
    }
    
    public void saveCluster() {
        String tempResult = "";
        ArrayList<String> Result = new ArrayList<>();

        for (int i = 0; i < this.data_table.length; i++) {
            for (int j = 0; j < this.data_table[0].length; j++) {
                tempResult += Double.toString(data_table[i][j]) + "\t";
            }
            Result.add(tempResult);
            tempResult = "";
        }
        tempResult = "";

        //Write Result Cluster
        try {
            File F_Result_Smoothing = new File("E://TA SUKSES/COLLABORATIVE FILTERING/Program/HASIL/Result_Smoothing.txt");
            FileOutputStream Fos_Result_Smoothing = new FileOutputStream(F_Result_Smoothing);
            BufferedWriter Bw_Result_Smoothing = new BufferedWriter(new OutputStreamWriter(Fos_Result_Smoothing));
//            int i = 1;
//            tempResult = Result.get(0) + "-1";
//            Result.set(0, tempResult);
//            for (User user1 : this.user) {
//                tempResult = Result.get(i) + Integer.toString(user1.getCluster());
//                Result.set(i, tempResult);
//                i++;
//            }
            for (String Result1 : Result) {
                Bw_Result_Smoothing.write(Result1);
                Bw_Result_Smoothing.newLine();
            }
            Bw_Result_Smoothing.close();
        } catch (IOException e) {
            System.out.println("Gagal menulis file");
            e.printStackTrace();
        }
    }

    public void play() {
        setData_table();
        setUser();
        smoothTwo();
        saveCluster();
    }
}
