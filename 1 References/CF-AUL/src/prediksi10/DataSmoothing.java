package prediksi10;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import util.CFHelper;

public class DataSmoothing {

    private double data_table[][];
    private ArrayList<User> user;
    private final double percentOfData;

    public DataSmoothing(double percentOfData) {
        this.percentOfData = percentOfData;
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
            for (int j = 1; j < ds.length - 2; j++) {
                double d = ds[j];
                if (d > 0) {
                    temp.get(i).getItemList().put(j, d);
                    temp.get(i).getKey().add(j);
                }
            }
            temp.get(i).setCluster((int) ds[ds.length - 2]);
            temp.get(i).setRua(ds[ds.length - 1]);
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
            //Baca File Database
            String sCurrentLine;
            br = new BufferedReader(new FileReader(
                    "E://TA SUKSES/COLLABORATIVE FILTERING/Program/HASIL/Result_Cluster_"+(int)percentOfData+".txt"));
            int i = 0;
            while ((sCurrentLine = br.readLine()) != null) {
                String data[] = sCurrentLine.split("\t");
                dataS.add(data);
                i++;
            }
        } catch (IOException e) {
            System.out.println("Gagal membaca file");
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
            } catch (IOException ex) {
            }
        }
        int jumUser = dataS.size();
        int jumItem = dataS.get(0).length;
        double datatable[][] = new double[jumUser][jumItem];
        for (int i = 0; i < datatable.length; i++) {
            for (int j = 0; j < datatable[i].length; j++) {
                datatable[i][j] = Double.parseDouble(dataS.get(i)[j]);
            }
        }
        this.data_table = datatable;
    }

    public double getDeltaRCu(User u, int t) {
        double sumA = 0;
        double sizeC = 0;
        for (User user1 : user) {
            if (user1.getCluster() == u.getCluster() && user1.getKey().contains(t)) {
                sumA += user1.getItemList().get(t) - CFHelper.getRata2ratingUser(user1);
                sizeC++;
            }
        }
        if (sizeC == 0) {
            return 0;
        }else{
            return sumA / sizeC;
        }
    }

    public double Rut(User u, int t) {
        double Ru = CFHelper.getRata2ratingUser(u);
        double deltaRCu = getDeltaRCu(u, t);
        return Ru + deltaRCu;
    }

    public void smoothTwo() {
        for (int i = 1; i < data_table.length; i++) {
            for (int j = 1; j < data_table[i].length - 2; j++) {
                if (data_table[i][j] == 0) {
                    double rating = Rut(this.user.get(i - 1), j);
                    data_table[i][j] = rating;
                }
            }
        }
    }
    
    public void saveResultSmoothing() {
        String tempResult = "";
        ArrayList<String> Result = new ArrayList<>();

        for (double[] data_table1 : this.data_table) {
            for (int j = 0; j < this.data_table[0].length; j++) {
                tempResult += Double.toString(data_table1[j]) + "\t";
            }
            Result.add(tempResult);
            tempResult = "";
        }

        //Write Result Cluster
        try {
            File F_Result_Smoothing = new File("E://TA SUKSES/COLLABORATIVE FILTERING/Program/HASIL/Result_Smoothing_"+(int)percentOfData+".txt");
            FileOutputStream Fos_Result_Smoothing = new FileOutputStream(F_Result_Smoothing);
            BufferedWriter Bw_Result_Smoothing = new BufferedWriter(new OutputStreamWriter(Fos_Result_Smoothing));
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
        saveResultSmoothing();
    }
}
