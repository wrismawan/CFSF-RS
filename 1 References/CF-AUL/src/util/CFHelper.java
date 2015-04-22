package util;

import prediksi10.User;

public class CFHelper {

    public static double getRata2ratingUser(User u) {
        double totRating = 0;
//        System.out.println(u.getItemList().size());
        for (int i = 0; i < u.getItemList().size(); i++) {
            totRating = totRating + u.getItemList().get(u.getKey().get(i));
        }
        return totRating / u.getItemList().size();
    }
}
