package prediksi10;

public class Centroid {
    private User center;
    private double rating[];

    public Centroid(User center) {
        this.center = center;
    }
    
    public User getCenteroid() {
        return center;
    }

    public double[] getRating() {
        return rating;
    }

    public void setRating(double t[]) {
        this.rating = t;
    }
}
