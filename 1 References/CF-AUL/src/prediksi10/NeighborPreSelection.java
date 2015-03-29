package prediksi10;

import java.util.ArrayList;
import util.CFHelper;

public class NeighborPreSelection {

    private ArrayList<Integer> cluster;
    private ArrayList<User> user;
    private ArrayList<User> ListUserOfCluster;
    private User userY;
    private int userP;
    private int itemN;
    private int selectedCluster;
    private double data_table[][];
    private double rua;

    public void setUserY(int userY) {
        User user = this.user.get(userY - 1);
        this.userY = user;
        if (userY != this.userP) {
            this.rua = CFHelper.getRata2ratingUser(this.userY);
        }
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

    public NeighborPreSelection() {
        this.ListUserOfCluster = new ArrayList<>();
    }

    public void setUser(ArrayList<User> user) {
        this.user = user;
    }

    public void setData_table(double[][] data_table) {
        this.data_table = data_table;
    }

    public void setCluster(ArrayList<Integer> cluster) {
        this.cluster = cluster;
    }

    public ArrayList<User> getListUserOfCluster() {
        return ListUserOfCluster;
    }

    public User getUser(int c) {
        User u;
        int i = 0;
        while (user.get(i).getUser_id() != c) {
            i++;
        }
        return user.get(i);
    }

    public double sim(User user, int clust) {
        double sumA = 0;
        double sumB = 0;
        double sumC = 0;
        double rata2Ru = this.rua;
        for (int i = 0; i < user.getKey().size(); i++) {
            int itemKey = user.getKey().get(i);
            double deltaRCt = getDeltaRCu(user, itemKey, clust);
            double Rua_Rbar = user.getItemList().get(itemKey) - rata2Ru;
            sumA += deltaRCt * (user.getItemList().get(itemKey) - rata2Ru);
            sumB += Math.pow(deltaRCt, 2);
            sumC += Math.pow(user.getItemList().get(itemKey) - rata2Ru, 2);
        }
        double multiAB = Math.sqrt(sumB) * Math.sqrt(sumC);
        return sumA / multiAB;
    }

    public double getDeltaRCu(User u, int t, int clust) {
        double sumA = 0;
        double sizeC = 0;
        for (int i = 0; i < user.size(); i++) {
            User user1 = user.get(i);
            if (user1.getCluster() == clust && user1.getKey().contains(t)) {
                double ru = user1.getItemList().get(t) - CFHelper.getRata2ratingUser(user1);
                sumA += ru;
                sizeC++;
            }
        }
        if (sizeC == 0) {
            return 0;
        } else {
            return sumA / sizeC;
        }
    }

    public ArrayList<User> getUserInClusterC(int c) {
        ArrayList<User> ListUserOfCluster = new ArrayList<>();
        for (int i = 0; i < user.size(); i++) {
            User user1 = user.get(i);
            if (user1.getCluster() == c) {
                ListUserOfCluster.add(user1);
            }
        }
        return ListUserOfCluster;
    }

    public void getClusterSimilar(User u) {
        double min = 10000;
        int c = 0;
        for (int i = 0; i < cluster.size(); i++) {
            Integer clust = cluster.get(i);
            double sim = sim(u, clust);
            if (sim < min) {
                min = sim;
                c = clust;
            }
        }
        this.selectedCluster = c;
        this.ListUserOfCluster = getUserInClusterC(c);
    }

    public int getClusterSim(User u) {
        double min = 10000;
        int c = 0;
        for (int i = 0; i < cluster.size(); i++) {
            Integer clust = cluster.get(i);
            double sim = sim(u, clust);
            if (sim < min) {
                min = sim;
                c = clust;
            }
        }
        return c;
    }

    public ArrayList<User> play() {
        if (userY.getUser_id() != userP) {
            getClusterSimilar(userY);
            return this.ListUserOfCluster;
        } else {
            return this.ListUserOfCluster;
        }
    }

    public ArrayList<User> play(int c) {
        if (userY.getUser_id() != userP) {
            this.ListUserOfCluster = getUserInClusterC(c);
            return this.ListUserOfCluster;
        } else {
            return this.ListUserOfCluster;
        }
    }
}
