from flask import Blueprint, request
import tensorflow as tf
import numpy as np

PATH_ABSOLUTE = "/app"

predict = Blueprint('predict', __name__)

@predict.route('/predict', methods=['POST'])
def flow_predict():
    if request.method == 'POST':
        request_data = request.get_json()
        x_test = request_data["flow"]

        model = tf.keras.models.load_model(PATH_ABSOLUTE + "/api/pre_trained_model/model.h5")

        predictions_1flow = model.predict(x_test)
        one_flow_pred = int(np.argmax(predictions_1flow, axis=-1))

        return str(one_flow_pred)