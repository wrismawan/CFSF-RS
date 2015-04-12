package prediksi10;

public class Prediksi10 {

    public static void main(String[] args) throws Exception {
        /**
         * Proses Trainnging : -Clustering -Data Smoothing
         */
//        int maxPercentData=10;
//        int NIC=0;
//        for (int i = 1; i <= maxPercentData; i++) {
//            //Proses Custering
//            Kmeans K = new Kmeans(i,NIC);
//            K.play();
//            System.out.println("K-means ke-"+i+" Done");
//            
//            //Proses Data Smoothing
////            DataSmoothing D = new DataSmoothing(i);
////            D.play();
////            System.out.println("DataSmoothing ke-"+i+" Done");
////            System.out.println("=============================");
//        }
//        System.out.println(Math.ceil(943/(943*((double)1/100))));
//        Kmeans K = new Kmeans(1, 5);
//        K.play();
//        DataSmoothing D = new DataSmoothing(1);
//        D.play();

        /**
         * Proses Testing
         * Proses Neighbor PreSelection
         * Proses Neihbor Selection
         * Proses Prediksi
         * Proses Evaluasi Sistem
         */
        //Proses Prediksi & Evaluasi Sistem
        int maxPercentData = 10;
        int maxNumNeighbor = 21;
        double maxSimThreshold = 0.4;
        int maxNIC = 15;
        double maxLamda = 1.0;
        int maxIterasi = 6;
        for (int c = 6; c <= maxIterasi; c++) {
            for (int i = 10; i <= maxPercentData; i++) {  //PercentData
                for (double j = 0.1; j <= maxSimThreshold; j = (double) Math.round(
                        (j + 0.1) * 100) / 100) {    //simThreshold
                    for (int k = 5; k <= maxNumNeighbor; k = k + 2) {    //numNeighbour
                        for (int l = 5; l <= maxNIC; l = l + 5) {    //NIC
                            for (double m = 0; m <= maxLamda; m = (double) Math.round(
                                    (m + 0.1) * 100) / 100) {    //lamda
                                Prediction T = new Prediction(k, l, j, m, i, c);
                                T.play();
                                System.out.println("Iterasi " + c + " PercentData " + i + " Th " + j + " Neighbor " + k + " NIC " + l + " lamda " + m + " done");
                            }
                        }
                    }
                }
            }
        }

        //neigh, nic, simTH, lamda, data, iterasi
//        Prediction T = new Prediction(5, 5, 0.1, 0.3, 10, 1);
//        T.play();
//        System.out.println("===============================================");
    }
}
