package cfv5;

import java.util.ArrayList;

public class NeighborPreSelection {
    private ArrayList<Integer> cluster;
    private ArrayList<User> user;
    private ArrayList<User> ListUserOfCluster;
    private double data_table[][];

    public NeighborPreSelection() {
        this.ListUserOfCluster=new ArrayList<>();
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
    
    public double sim(User u, int c,int t){
        double sumA=0;
        double sumB=0;
        double sumC=0;
        for (int i = 0; i < user.size(); i++) {
            User user1 = user.get(i);
            
        }
        return 0;
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
    
    public ArrayList<User> getUserInClusterC(int c) {
        ArrayList<User> ListUserOfCluster=new ArrayList<>();
        for (int i = 0; i < user.size(); i++) {
            User user1 = user.get(i);
            if(user1.getCluster()==c){
                ListUserOfCluster.add(user1);
            }
        }
        return ListUserOfCluster;
    }
    
    public void getClusterSimilar(User u, int t){
        double min=10000;
        int c=0;
        for (int i = 0; i < cluster.size(); i++) {
            Integer integer = cluster.get(i);
            double sim=sim(u,integer,t);
            if(sim<min){
                min=sim;
                c=integer;
            }
        }
        this.ListUserOfCluster=getUserInClusterC(c);
    }
    
    public void play(){
        
    }
}
