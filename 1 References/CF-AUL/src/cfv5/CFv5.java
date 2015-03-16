package cfv5;

public class CFv5 {

    public static void main(String[] args) throws Exception {
        /**
         * Proses Trainnging :
         * -Clustering
         * -Data Smoothing
         */
        //Proses Custering
        Kmeans K=new Kmeans(1);
        K.play();
        
        //Proses Data Smoothing
        DataSmoothing D=new DataSmoothing();
        D.play();
        D.setCluster(K.getHasilCluster());
        
        /**
         * Proses Testing
         * -Proses Neighbor Pre-Selection
         * -Proses Neihbor Selection
         * -Proses Prediksi
         * -Proses Evaluasi Sistem
         */
        //Proses Neighbor Pre-Selection
        NeighborPreSelection N1=new NeighborPreSelection();
        N1.setCluster(D.getCluster());
        N1.setData_table(D.getData_table());
        N1.setUser(D.getUser());
        //Proses Neihbor Selection
        //Proses Prediksi
        //Proses Evaluasi Sistem
    }
    
}
