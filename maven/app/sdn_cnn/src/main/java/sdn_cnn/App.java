package sdn_cnn;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import org.tensorflow.SavedModelBundle;
import org.tensorflow.Tensor;

import org.tensorflow.ndarray.DoubleNdArray;
import org.tensorflow.ndarray.NdArrays;
import org.tensorflow.ndarray.NdArray;
import org.tensorflow.ndarray.Shape;
import org.tensorflow.proto.framework.SignatureDef;
import org.tensorflow.types.TFloat64;

import tech.tablesaw.api.Table;

public class App {

    private final static String[] labels = new String[] {
        "FileTransfer",
        "Music",
        "VoIP",
        "Youtube"
    };


    public static void main(String[] args) {
        try {
            // get path to model folder
            String modelPath = "/root/sdn_cnn/model";
            // load saved model
            SavedModelBundle model = SavedModelBundle.load(modelPath, "serve");
            SignatureDef sig = model.metaGraphDef().getSignatureDefMap().get("serving_default");
            System.out.println(model.metaGraphDef().getSignatureDefMap());
            System.out.println(sig);

            // Read data
            // String test_dir = "/root/sdn_cnn/dataset/GQUIC_small/Test/GQUIC_test_10.csv";
            // Table t = Table.read().csv(test_dir);

            // IntNdArray input_matrix = NdArrays.ofInts(Shape.of(1, 20, 128, 1));
            DoubleNdArray input_matrix = NdArrays.ofDoubles(Shape.of(1, 9));
            Double[][] test = {
                {1.0}, {2.0}
            };

            input_matrix.set(NdArrays.vectorOf(1.0, 2.0, 3.0, 5.0, 7.0, 21.0, 23.0, 43.0, 123.0), 0);
            System.out.println(input_matrix.getDouble(0,1));
            Tensor input_tensor = TFloat64.tensorOf(input_matrix);
            // Tensor output = model.session()
            //     .runner()
            //     .feed("input_name", input_tensor)
            //     .fetch("output_name")
            //     .run()
            //     .expect(TFloat64.class);
            // System.out.println(input_matrix);
            Map<String, Tensor> feed_dict = new HashMap<>();
            feed_dict.put("context", input_tensor);

            System.out.println(model.function("serving_default").call(feed_dict));
        } catch (Exception e) {
            System.out.println("Something went wrong." + e);
        }
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
