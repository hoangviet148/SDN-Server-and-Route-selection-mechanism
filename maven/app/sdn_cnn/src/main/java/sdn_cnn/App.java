package sdn_cnn;

import java.util.Arrays;

import org.tensorflow.SavedModelBundle;

public class App {

    private final static String[] labels = new String[] {
            "FileTransfer",
            "Music",
            "VoIP",
            "Youtube"
    };

    public static void main(String[] args) {
        // get path to model folder
        String modelPath = "/root/sdn_cnn/model";
        // load saved model
        SavedModelBundle model = SavedModelBundle.load(modelPath, "serve");

        // Read data
        String test_dir = "/root/sdn_cnn/dataset/GQUIC_small/Test/GQUIC_test_512.feather";
        
    }

    private int most_frequent(int[] list) {
        if (list == null || list.length == 0) {
            return 0;
        }
        Arrays.sort(list);

        int previous = list[0];
        int popular = list[0];
        int count = 1;
        int maxCount = 1;

        for (int i = 1; i < list.length; i++) {
            if (list[i] == previous)
                count++;
            else {
                if (count > maxCount) {
                    popular = list[i - 1];
                    maxCount = count;
                }
                previous = list[i];
                count = 1;
            }
        }

        return count > maxCount ? list[list.length - 1] : popular;
    }
}
