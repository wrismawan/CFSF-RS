package prediksi10;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;
import util.CFHelper;

public class NeighborSelection {

    private ArrayList<User> user;
    private ArrayList<User> ListUserOfCluster;
    private ArrayList<User> ListNeighbor;
    private ArrayList<Integer> ListTabu;
    private ArrayList<Integer> cluster;
    private int userY;
    private int userP;
    private int itemN;
    private int numNeighbor;
    private int NIC;
    private double simThreshold;
    private int selectedCluster;
    private double lamda;
    private double data_table[][];
    private double data_tableS[][];
    private double rua;

    public NeighborSelection(int numNeighbor, int NIC, double simThreshold, double lamda) {
        this.numNeighbor = numNeighbor;
        this.NIC = NIC;
        this.simThreshold = simThreshold;
        this.lamda = lamda;
        this.ListNeighbor = new ArrayList<>();
        this.ListTabu = new ArrayList<>();
    }

    public ArrayList<User> getListUserOfCluster() {
        return ListUserOfCluster;
    }

    public ArrayList<User> getListNeighbor() {
        return ListNeighbor;
    }

    public void setUserY(int userY) {
        this.userY = userY - 1;
        if (userY != this.userP) {
            this.rua = this.user.get(this.userY).getRua();
        }
    }

    public void setUser(ArrayList<User> user) {
        this.user = user;
    }

    public void setItemN(int itemN) {
        this.itemN = itemN;
    }

    public int getUserP() {
        return userP;
    }

    public void setUserP(int userP) {
        this.userP = userP;
    }

    public void setData_table(int user, int item) {
        double data[][] = new double[user + 1][item + 1];
        this.data_table = data;
    }

    public void setData_tableS(double[][] data_tableS) {
        this.data_tableS = data_tableS;
    }

    public void setData_table(double[][] data_table) {
        this.data_table = data_table;
    }

    public void setCluster(ArrayList<Integer> cluster) {
        this.cluster = cluster;
    }

    public void setListUserOfCluster(ArrayList<User> ListUserOfCluster) {
        this.ListUserOfCluster = ListUserOfCluster;
    }

    public void setListTopK() throws Exception {
        NeighborPreSelection N2 = new NeighborPreSelection();
        N2.setData_table(this.data_tableS);
        N2.setUser(this.user);
        N2.setCluster(this.cluster);
        N2.setUserY(userY + 1);
        N2.setUserP(userP);
        N2.setItemN(itemN);
        this.ListUserOfCluster = N2.play();
        System.out.println(ListUserOfCluster.get(0).getCluster());
    }

    public void setSimCluster() throws Exception {
        NeighborPreSelection N2 = new NeighborPreSelection();
        N2.setData_table(this.data_tableS);
        N2.setUser(this.user);
        N2.setCluster(this.cluster);
        for (int i = 0; i < user.size(); i++) {
//        for (int i = 0; i < 5; i++) {
            User user1 = user.get(i);
            N2.setUserY(user1.getUser_id());
            N2.setUserP(user1.getUser_id() - 1);
//            System.out.println(N2.getClusterSim(user1) + "\t" + user1.getCluster());
            //Write Hasil Neighbor Pre-Selection
            try {
                OutputStreamWriter writer = new OutputStreamWriter(
                        new FileOutputStream(
                                "/home/whr/Documents/COLLABORATIVE FILTERING/Program/HASIL/Result_PreSelection.txt",
                                true), "UTF-8");
                BufferedWriter fbw = new BufferedWriter(writer);
                fbw.write(N2.getClusterSim(user1));
                fbw.newLine();
                fbw.close();
            } catch (IOException e) {
                System.out.println("Gagal menulis file");
                e.printStackTrace();
            }
        }
    }

    public double Pearson(User u, User v) {
        Set keyU = u.getItemList().keySet();
        Integer[] kU = (Integer[]) keyU.toArray(new Integer[keyU.size()]);
        double sumA = 0;  //sum((Rut-Ru^)*(Ru't-Ru'^))
        double tot_Rating_ItemU = 0;
        double rata2_Rating_U = u.getRua();    //Ru^
        double tot_Rat_ItemC = 0;
        double rata2_Rating_V = this.rua;    //Ru'^
        double sumB = 0;  //sum(Rut-Ru^)2
        double sumC = 0;  //sum(Ru't-Ru'^)2
        int count = 0;
        for (Integer kU1 : kU) {
            if (v.getItemList().containsKey(kU1)) {
                double wut = 0;
                if (data_table[u.getUser_id()][kU1] > 0) {
                    wut = 1 - lamda;
                } else {
                    wut = lamda;
                }
                double ru = (u.getItemList().get(kU1) - rata2_Rating_U);
                double rua = (v.getItemList().get(kU1) - rata2_Rating_V);
                double wut_ru_rua = wut * ru * rua;
                sumA += wut_ru_rua;
                if (data_table[u.getUser_id()][kU1] > 0) {
                    wut = 1 - lamda;
                } else {
                    wut = lamda;
                }
                sumB += Math.pow(wut, 2) * Math.pow((u.getItemList().get(kU1) - rata2_Rating_U), 2);
                sumC += Math.pow((v.getItemList().get(kU1) - rata2_Rating_V), 2);
                count++;
            }
        }

        double multiAB = (Math.sqrt(sumB) * Math.sqrt(sumC));
        if (count > NIC) {
            return sumA / multiAB;
        } else {
            return -1;
        }
    }

    public double Prediksi() {
        double sumA = 0; //sum(simUA*Rut-Rua)
        double sumB = 0;
        double Rua = this.rua;
        for (int i = 0; i < ListNeighbor.size(); i++) {
            double simXY = Pearson(ListNeighbor.get(i), user.get(userY));
            double wut = 0;
            if (data_table[ListNeighbor.get(i).getUser_id()][itemN] > 0) {
                wut = 1 - lamda;
            } else {
                wut = lamda;
            }
            sumA += wut * simXY * (ListNeighbor.get(i).getItemList().get(itemN) - ListNeighbor.get(i).getRua());
            sumB += wut * simXY;
        }
        double prediksi = Rua + (sumA / sumB);
        if (ListNeighbor.size() == 0 || Double.isNaN(prediksi) || prediksi>5) {
            prediksi = Rua;
//            prediksi = data_tableS[user.get(userY).getUser_id()][itemN];
        }
        return prediksi;
    }

    public double getTopK() {
        ListNeighbor.clear();
        ListTabu.clear();
        while (ListNeighbor.size() < numNeighbor && ListTabu.size() < ListUserOfCluster.size()) {
            int numData = (int) (Math.random() * ListUserOfCluster.size());
            if (!ListTabu.contains(numData)) {
                ListTabu.add(numData);
                double simXY = Pearson(ListUserOfCluster.get(numData), this.user.get(userY));
                if (simXY >= simThreshold && data_tableS[ListUserOfCluster.get(numData).getUser_id()][itemN] > 0) {
                    ListNeighbor.add(ListUserOfCluster.get(numData));
                }
            }
        }

        //Prediksi
        double rating_pred = Prediksi();
        return rating_pred;
    }

    public double play() throws Exception {
        return getTopK();
    }
}
