package cfv5;

import java.util.ArrayList;
import java.util.HashMap;

public class User {
    private int user_id;
    private int cluster=-1;
    private ArrayList<Integer> key;
    private HashMap<Integer,Double> itemList;

    public User(int user_id, ArrayList<Integer> key, HashMap<Integer, Double> itemList) {
        this.user_id = user_id;
        this.key = key;
        this.itemList = itemList;
    }
    
    public User(int user_id) {
        this.user_id = user_id;
        this.itemList=new HashMap<>();
        this.key=new ArrayList<>();
    }

    public HashMap<Integer,Double> getItemList() {
        return itemList;
    }

    public void setItemList(HashMap<Integer,Double> itemList) {
        this.itemList = itemList;
    }

    public int getUser_id() {
        return user_id;
    }

    public void setUser_id(int user_id) {
        this.user_id = user_id;
    }

    public void setCluster(int cluster) {
        this.cluster = cluster;
    }

    public int getCluster() {
        return cluster;
    }

    public ArrayList<Integer> getKey() {
        return key;
    }

    public void setKey(ArrayList<Integer> key) {
        this.key = key;
    }
}
