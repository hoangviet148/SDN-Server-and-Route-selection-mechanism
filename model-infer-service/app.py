from flask import Flask, request, jsonify
import sys, json
import tensorflow as tf
import numpy as np

# init
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        request_data = request.get_json()
        x_test = request_data["flow"]

        model = tf.keras.models.load_model("/app/model/model.h5")

        predictions_1flow = model.predict(x_test)
        one_flow_pred = int(np.argmax(predictions_1flow, axis=-1))

        return str(one_flow_pred)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)