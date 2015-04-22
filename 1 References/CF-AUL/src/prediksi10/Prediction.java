package prediksi10;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.HashMap;

public class Prediction {

    private ArrayList<User> ListNeighbor;
    private ArrayList<User> ListUserTest;
    private ArrayList<Integer> ListUid = new ArrayList<Integer>();
    private ArrayList<Integer> ListIid = new ArrayList<Integer>();
    private ArrayList<Double> ListRating = new ArrayList<Double>();
    private ArrayList<Double> ListPrediksi = new ArrayList<Double>();
    private ArrayList<Integer> cluster;
    private HashMap<Integer, Integer> clusterUser;
    private HashMap<Integer, ArrayList<User>> ListUserInCluster = new HashMap<Integer, ArrayList<User>>();
    private ArrayList<User> user;
    private int userY;
    private int itemN;
    private int numNeighbor;
    private int NIC;
    private int iterasi;
    private double simThreshold;
    private double lamda;
    private final double percentOfData;
    private double[][] data_tableS;
    private double[][] data_table;
    private double mae = 0, rmse = 0;

    public Prediction(int numNeighbor, int NIC, double simThreshold, double lamda, double percentOfData, int iterasi) {
        this.numNeighbor = numNeighbor;
        this.NIC = NIC;
        this.simThreshold = simThreshold;
        this.lamda = lamda;
        this.percentOfData = percentOfData;
        this.iterasi = iterasi;
    }

    public void setData_table() {
        BufferedReader br = null;
        ArrayList<String[]> dataS = new ArrayList<>();

        //Open File
        try {
            //Baca File Data Hasil Smoothing
            String sCurrentLine;
            br = new BufferedReader(new FileReader(
                    "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Trainning/Result_Cluster_" + (int) percentOfData + ".txt"));
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

    public void setData_tableS() {
        BufferedReader br = null;
        ArrayList<String[]> dataS = new ArrayList<>();

        //Open File
        try {
            //Baca File Data Hasil Smoothing
            String sCurrentLine;
            br = new BufferedReader(new FileReader(
                    "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Trainning/Result_Smoothing_" + (int) percentOfData + ".txt"));
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
        this.data_tableS = data_table;
    }

    public void setUser() {
        HashMap<Integer, User> temp = new HashMap<>();
        ArrayList<User> userList = new ArrayList<>();
        //Bikin list user
        for (int i = 1; i < data_tableS.length; i++) {
            User u = new User(i);
            temp.put(i, u);
        }

        //Masukin rating item ke list user
        for (int i = 1; i < data_tableS.length; i++) {
            double[] ds = data_tableS[i];
            for (int j = 1; j < ds.length - 2; j++) {
                double d = ds[j];
                if (d > 0) {
                    temp.get(i).getItemList().put(j, d);
                    temp.get(i).getKey().add(j);
                }
            }
            temp.get(i).setCluster((int) ds[ds.length - 2]);
            temp.get(i).setRua(ds[ds.length - 1]);

            this.ListUserInCluster.get(temp.get(i).getCluster()).add(temp.get(i));
        }

        for (int i = 1; i <= temp.size(); i++) {
            userList.add(temp.get(i));
        }

        this.user = userList;
    }

    public void setCluster() {
        BufferedReader br = null;
        ArrayList<Integer> dataCluster = new ArrayList<>();

        //Open File
        try {
            //Baca File Data Hasil Smoothing
            String sCurrentLine;
            br = new BufferedReader(new FileReader(
                    "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Trainning/Cluster_" + (int) percentOfData + ".txt"));
            while ((sCurrentLine = br.readLine()) != null) {
                int data = Integer.parseInt(sCurrentLine);
                dataCluster.add(data);
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
        this.cluster = dataCluster;

        for (int i = 0; i < dataCluster.size(); i++) {
            Integer integer = dataCluster.get(i);
            ListUserInCluster.put(integer, new ArrayList<User>());
        }
    }

    public void setClusterUser() {
        BufferedReader br = null;
        HashMap<Integer, Integer> dataClusterUser = new HashMap<>();

        //Open File
        try {
            //Baca File Data Hasil Smoothing
            String sCurrentLine;
            br = new BufferedReader(new FileReader(
                    "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Hasil_PreSelection_"+(int)percentOfData+".txt"));
            int i = 0;
            while ((sCurrentLine = br.readLine()) != null) {
                int data = Integer.parseInt(sCurrentLine);
                dataClusterUser.put(i, data);
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
        this.clusterUser = dataClusterUser;
    }

    public void setListUserTest() throws Exception {
        ArrayList<User> ListUserTest = new ArrayList<>();
        HashMap<Integer, Double> itemList = new HashMap<>();
        HashMap<Integer, User> temp = new HashMap<>();
        Koneksi db = new Koneksi();
        String sql = "SELECT * FROM user";
        ResultSet rs = db.getAll(sql);
        //Bikin list user
        while (rs.next()) {
            User u = new User(Integer.parseInt(rs.getString("user_id")));
            temp.put(Integer.parseInt(rs.getString("user_id")), u);
        }

        //Masukin rating item ke list user
        sql = "SELECT * FROM rating_test";
        rs = db.getAll(sql);
        while (rs.next()) {
            temp.get(Integer.parseInt(rs.getString("user_id"))).getItemList().put(
                    Integer.parseInt(rs.getString("movie_id")),
                    Double.parseDouble(rs.getString("rating_value")));
            temp.get(Integer.parseInt(rs.getString("user_id"))).getKey().add(
                    Integer.parseInt(rs.getString("movie_id")));
            ListUid.add(Integer.parseInt(rs.getString("user_id")));
            ListIid.add(Integer.parseInt(rs.getString("movie_id")));
            ListRating.add(Double.parseDouble(rs.getString("rating_value")));
        }

        for (int i = 1; i <= temp.size(); i++) {
            ListUserTest.add(temp.get(i));
        }
        this.ListUserTest = ListUserTest;
    }

    public void play() throws Exception {
        setListUserTest();
        setData_tableS();
        setData_table();
        setCluster();
        setUser();
//        setClusterUser();
        double sumRMSE = 0, sumMAE = 0;
        int user = 0, item = 0, userP = 0;
        NeighborSelection N = new NeighborSelection(numNeighbor, NIC, simThreshold, lamda);
        NeighborPreSelection N2 = new NeighborPreSelection();
        for (int i = 0; i < ListUid.size(); i++) {
//        for (int i = 0; i < 5; i++) {
            if (i > 0) {
                user = ListUid.get(i);
                item = ListIid.get(i);
                userP = ListUid.get(i - 1);
            } else {
                user = ListUid.get(i);
                item = ListIid.get(i);
                userP = 0;
            }

            N.setUser(this.user);
            N.setCluster(cluster);
            N.setUserY(user);
            N.setItemN(item);
            N.setUserP(userP);
            N.setData_tableS(data_tableS);
            N.setData_table(data_table);
            N.setListUserOfCluster(this.ListUserInCluster.get(this.user.get(user-1).getCluster()));

            double pred = N.play();
            String Tabel_A1 = iterasi + "\t" + percentOfData + "\t" + simThreshold + "\t" + numNeighbor + "\t" + NIC + "\t" + lamda + "\t" + user + "\t" + item + "\t" + pred + "\t" + ListRating.get(i) + "\t" + N.getListNeighbor().size() + "\t" + this.user.get(user-1).getRua();
//            System.out.println(Tabel_A1);
            //Write Tabel A1
            try {
                OutputStreamWriter writer = new OutputStreamWriter(
                        new FileOutputStream(
                                "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Testing/Tabel_1/Prediksi_Tabel_A1_" + iterasi + "_" + percentOfData + "_" + simThreshold + "_" + numNeighbor + "_" + NIC + "_" + lamda + ".txt",
                                true), "UTF-8");
                BufferedWriter fbw = new BufferedWriter(writer);
                fbw.write(Tabel_A1);
                fbw.newLine();
                fbw.close();
            } catch (IOException e) {
                System.out.println("Gagal menulis file");
                e.printStackTrace();
            }
            ListPrediksi.add(pred);
            sumMAE += Math.abs(ListRating.get(i) - pred);
            sumRMSE += Math.pow(Math.abs(ListRating.get(i) - pred), 2);
        }
        this.mae = (double) sumMAE / ListUid.size();
        this.rmse = Math.sqrt((double) sumRMSE / ListUid.size());

        String Tabel_A2 = iterasi + "\t" + percentOfData + "\t" + simThreshold + "\t" + numNeighbor + "\t" + NIC + "\t" + lamda + "\t" + mae + "\t" + rmse;
        //Write Tabel A2
        try {
            OutputStreamWriter writer = new OutputStreamWriter(
                    new FileOutputStream(
                            "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Testing/Tabel_2/Prediksi_Tabel_A2_" + iterasi + ".txt",
                            true), "UTF-8");
            BufferedWriter fbw = new BufferedWriter(writer);
            fbw.write(Tabel_A2);
            fbw.newLine();
            fbw.close();
        } catch (IOException e) {
            System.out.println("Gagal menulis file");
            e.printStackTrace();
        }
    }

    public void play2() throws Exception {
        setListUserTest();
        setData_tableS();
        setData_table();
        setUser();
        setCluster();
        double sumRMSE = 0, sumMAE = 0;
        int user = 0, item = 0, userP = 0;
        NeighborSelection N = new NeighborSelection(numNeighbor, NIC, simThreshold, lamda);
        NeighborPreSelection N2 = new NeighborPreSelection();
        N.setUser(this.user);
        N.setCluster(cluster);
        N.setUserY(user);
        N.setItemN(item);
        N.setUserP(userP);
        N.setData_tableS(data_tableS);
        N.setData_table(data_table);
        N.setSimCluster();
    }
}
