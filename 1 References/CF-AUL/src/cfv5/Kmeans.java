package cfv5;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class Kmeans {

    private double num_cluster;
    private final double percentOfData;
    private ArrayList<User> user;
    private ArrayList<Centroid> centroid;
    private ArrayList<Integer> cluster;
    private double[][] data_tableS;
    private double data_table[][];

    public Kmeans(double percentOfData) {
        this.cluster=new ArrayList<>();
        this.percentOfData = percentOfData;
    }

    public double getNum_cluster() {
        return num_cluster;
    }

    public ArrayList<Integer> getHasilCluster() {
        return cluster;
    }

    public void setNum_cluster() {
//        this.num_cluster=Math.ceil(this.user.size()/(this.user.size()*(this.percentOfData/100)));
//        System.out.println(this.user.size());
//        System.out.println((this.user.size()*(this.percentOfData/100)));
        this.num_cluster = 2;
//        System.out.println(num_cluster);
    }

    public ArrayList<User> getUser() {
        return user;
    }

    public void setData_table(int user, int item) {
        double data1[][] = new double[user + 1][item + 1];
        double data2[][] = new double[user + 1][item + 1];
        this.data_table = data1;
        this.data_tableS = data2;
    }

    public void setUser() throws Exception {
        ArrayList<User> userList = new ArrayList<>();
        HashMap<Integer, Double> itemList = new HashMap<>();
        HashMap<Integer, User> temp = new HashMap<>();
        int jumUser = 0, jumItem;
        Koneksi db = new Koneksi();
        String sql = "SELECT * FROM user";
        ResultSet rs = db.getAll(sql);
        //Bikin list user
        while (rs.next()) {
            User u = new User(Integer.parseInt(rs.getString("user_id")));
            temp.put(Integer.parseInt(rs.getString("user_id")), u);
            jumUser++;
        }

        //Bikin matriks data user-rating
        sql = "SELECT * FROM item";
        rs = db.getAll(sql);
        rs.last();
        jumItem = rs.getRow();
        setData_table(jumUser, jumItem);

        //Masukin rating item ke list user
        sql = "SELECT * FROM data2";
        rs = db.getAll(sql);
        while (rs.next()) {
//            temp.get(Integer.parseInt(rs.getString("user_id"))).getItemList().put(Integer.parseInt(rs.getString("item_id")), Integer.parseInt(rs.getString("rating")));
//            temp.get(Integer.parseInt(rs.getString("user_id"))).getKey().add(Integer.parseInt(rs.getString("item_id")));
//            data_table[Integer.parseInt(rs.getString("user_id"))][Integer.parseInt(rs.getString("item_id"))] = Integer.parseInt(rs.getString("rating"));
            temp.get(Integer.parseInt(rs.getString("user_id"))).getItemList().put(Integer.parseInt(rs.getString("item_id")), Double.parseDouble(rs.getString("rating")));
            temp.get(Integer.parseInt(rs.getString("user_id"))).getKey().add(Integer.parseInt(rs.getString("item_id")));
            data_tableS[Integer.parseInt(rs.getString("user_id"))][Integer.parseInt(rs.getString("item_id"))] = Double.parseDouble(rs.getString("rating"));
            data_table[Integer.parseInt(rs.getString("user_id"))][Integer.parseInt(rs.getString("item_id"))] = Double.parseDouble(rs.getString("rating"));
        }

        for (int i = 1; i <= temp.size(); i++) {
            userList.add(temp.get(i));
        }

//        for(int i=1;i<=jumUser;i++){
//            for(int j=1;j<=jumItem;j++){
//                System.out.print(data_table[i][j]+" ");
//            }
//            System.out.println();
//        }
        this.user = userList;
    }

    public void setCentroid() {
        ArrayList<Centroid> centroids = new ArrayList<>();
        ArrayList<Integer> x = new ArrayList<>();
        int rand, i = 0, j = 0;
        while (i < num_cluster) {
            rand = (int) Math.ceil(Math.random() * this.user.size());
            if (!x.contains(rand)) {
                this.user.get(rand).setCluster(i);
                Centroid c = new Centroid(this.user.get(rand));
                c.setRating(data_tableS[this.user.get(rand).getUser_id()]);
                centroids.add(c);
                x.add(rand);
                i++;
            }
//            if(j>1000){
//                break;
//            }
//            j++;
        }
        this.centroid = centroids;
    }

    public void setMeanCluster(ArrayList<User> data) {
        double dataInCluster;
        for (Centroid c : this.centroid) {
            dataInCluster = 0;
            double sum[] = new double[c.getRating().length - 1];
            double mean[] = new double[c.getRating().length];
            for (User data1 : data) {
                if (data1.getCluster() == c.getCenteroid().getCluster()) {
                    for (int i = 0; i < sum.length; i++) {
                        sum[i] = sum[i] + data_tableS[data1.getUser_id()][i + 1];
                    }
                    dataInCluster++;
                }
            }
            for (int i = 0; i < sum.length; i++) {
                mean[i + 1] = sum[i] / dataInCluster;
            }
            if (dataInCluster > 0) {
                c.setRating(mean);
            }
        }
    }

    public void getCluster() throws Exception {
        double distUC;
        double bigNumber = Math.pow(10, 10);
        double min = bigNumber;
        int cluster = -1;
        boolean isStillMoving = true;
        ArrayList<User> tempDataset = new ArrayList<>();
        for (User user1 : this.user) {
            min = bigNumber;
            for (Centroid centroid1 : this.centroid) {
                distUC = Dist(user1, centroid1);
                if (distUC < min) {
                    min = distUC;
                    cluster = centroid1.getCenteroid().getCluster();
                }
            }
            user1.setCluster(cluster);
            User tempUser = new User(user1.getUser_id(), user1.getKey(), user1.getItemList());
            tempUser.setCluster(cluster);
            tempDataset.add(tempUser);
            setMeanCluster(tempDataset);
        }

        //cek  ulang
        while (isStillMoving) {
            for (User user1 : this.user) {
                min = bigNumber;
                tempDataset.add(user1);
                for (Centroid centroid1 : this.centroid) {
                    distUC = Dist(user1, centroid1);
                    if (distUC < min) {
                        min = distUC;
                        cluster = centroid1.getCenteroid().getCluster();
                    }
                }
                
                isStillMoving = false;
                if (user1.getCluster() != cluster) {
                    user1.setCluster(cluster);
                    isStillMoving = true;
                }
            }
        }
    }

    public double Pearson(User u, Centroid c) {
        Set keyU = u.getItemList().keySet();
        Integer[] kU = (Integer[]) keyU.toArray(new Integer[keyU.size()]);
        Set keyC = c.getCenteroid().getItemList().keySet();
        Integer[] kC = (Integer[]) keyC.toArray(new Integer[keyC.size()]);
        double sumA = 0;  //sum((Rut-Ru^)*(Ru't-Ru'^))
        double tot_Rating_ItemU = 0;
        double rata2_Rating_U;    //Ru^
        double tot_Rat_ItemC = 0;
        double rata2_Rating_C;    //Ru'^
        double sumB = 0;  //sum(Rut-Ru^)2
        double sumC = 0;  //sum(Ru't-Ru'^)2
        for (Integer kU1 : kU) {
            tot_Rating_ItemU = tot_Rating_ItemU + u.getItemList().get(kU1);
        }
        rata2_Rating_U = tot_Rating_ItemU / kU.length;

        for (Integer kC1 : kC) {
            tot_Rat_ItemC = tot_Rat_ItemC + c.getCenteroid().getItemList().get(kC1);
        }
        rata2_Rating_C = tot_Rat_ItemC / kC.length;
        for (Integer kU1 : kU) {
            if (c.getCenteroid().getItemList().containsKey(kU1)) {
                sumA = sumA + ((u.getItemList().get(kU1) - rata2_Rating_U) * (c.getCenteroid().getItemList().get(kU1) - rata2_Rating_C));
                sumB = sumB + ((u.getItemList().get(kU1) - rata2_Rating_U) * (u.getItemList().get(kU1) - rata2_Rating_U));
                sumC = sumC + ((c.getCenteroid().getItemList().get(kU1) - rata2_Rating_C) * (c.getCenteroid().getItemList().get(kU1) - rata2_Rating_C));
//                System.out.println("item sama");
//                System.out.print("item_id user ke-"+u.getUser_id()+" = "+kU[i]);
//                System.out.println("  rating = "+u.getItemList().get(kU[i]));
//                System.out.print("item_id centroid ke-"+c.getCenteroid().getUser_id()+" = "+kU[i]);
//                System.out.println("  rating = "+c.getCenteroid().getItemList().get(kU[i]));
            }
        }
        return sumA / (sumB * sumC);
    }

    public double Dist(User u, Centroid c) {
        double sum = 0, n, x, y, dist;
        n = data_tableS[u.getUser_id()].length;
        for (int i = 1; i < n; i++) {
            x = data_tableS[u.getUser_id()][i];
            y = c.getRating()[i];
            sum = sum + Math.pow((x - y), 2);
        }
        dist = Math.sqrt(sum);
        return dist;
    }

    public double getRata2ratingUser(User u) {
        double totRating = 0;
        for (int i = 0; i < u.getItemList().size(); i++) {
            totRating = totRating + u.getItemList().get(u.getKey().get(i));
        }
        return totRating / u.getItemList().size();
    }

    public void smoothOne() {
        for (int i = 1; i < data_tableS.length; i++) {
            double rating = getRata2ratingUser(this.user.get(i - 1));
            for (int j = 1; j < data_tableS[i].length; j++) {
                if (data_tableS[i][j] == 0) {
                    data_tableS[i][j] = rating;
                }
//                System.out.print(data_table[i][j] + " ");
            }
//            System.out.println();
        }
    }

    public void printDataset() {
        smoothOne();
    }

    public void saveCluster() {
        String tempResult = "";
        ArrayList<String> Result = new ArrayList<>();

        for (int i = 0; i < this.data_table.length; i++) {
            for (int j = 0; j < this.data_table[0].length; j++) {
                tempResult += Double.toString(data_table[i][j]) + "\t";
            }
//            System.out.println(tempResult);
            Result.add(tempResult);
            tempResult = "";
        }
        tempResult = "";

        //Write Result Cluster
        try {
            File F_Result_Cluster = new File("E://TA SUKSES/COLLABORATIVE FILTERING/Program/HASIL/Result_Cluster.txt");
            FileOutputStream Fos_Result_Cluster = new FileOutputStream(F_Result_Cluster);
            BufferedWriter Bw_Result_Cluster = new BufferedWriter(new OutputStreamWriter(Fos_Result_Cluster));
            int i = 1;
            tempResult = Result.get(0) + "-1";
            Result.set(0, tempResult);
            for (User user1 : this.user) {
                tempResult = Result.get(i) + Integer.toString(user1.getCluster());
                if(!cluster.contains(user1.getCluster())){
                    cluster.add(user1.getCluster());
                }
                Result.set(i, tempResult);
//                Bw_Result_Cluster.write(Integer.toString(user1.getCluster()));
//                Bw_Result_Cluster.write(Result.get(i));
//                Bw_Result_Cluster.newLine();
                i++;
            }
            for (String Result1 : Result) {
                Bw_Result_Cluster.write(Result1);
                Bw_Result_Cluster.newLine();
            }
            Bw_Result_Cluster.close();
        } catch (IOException e) {
            System.out.println("Gagal menulis file");
            e.printStackTrace();
        }
    }

    public void play() throws Exception {
        setUser();
        System.out.println("setUser done");
        setNum_cluster();
        System.out.println("setNum_cluster done");
        smoothOne();
        System.out.println("smoothOne done");
        setCentroid();
        System.out.println("setCentroid done");
        getCluster();
        System.out.println("getCluster done");
        saveCluster();
        System.out.println("saveCluster done");
    }
}
