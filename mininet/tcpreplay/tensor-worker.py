import pika
import json
import os, sys, threading
import time
import tensorflow as tf
import numpy as np
import config
# tensorflow
# import tensorflow as tf
# from keras.models import load_model

class ThreadedConsumer(threading.Thread):
    def __init__(self, thread_id=-1):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

        # parameters = pika.URLParameters(RABBIT_URL)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_URL))
        self.channel = connection.channel()
        # self.channel.queue_declare(queue=QUEUE_NAME, auto_delete=False)
        # self.channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=config.PREFETCH_COUNT)
        self.channel.basic_consume(config.PRODUCER_QUEUE, on_message_callback=self.callback, auto_ack=False)
        threading.Thread(target=self.channel.basic_consume(config.PRODUCER_QUEUE, on_message_callback=self.callback))

    def callback(self, channel, method, properties, body):
        message = json.loads(body)
        # time.sleep(5)
        self.predict(message)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def predict(self, message):
        # print(message)

        # request_data = request.get_json()
        # x_test = request_data["flow"]

        model = tf.keras.models.load_model("/app/api/model/model.h5")
        temp = next(iter(message.values()))
        print("=== data ===", temp['data'])
        my_array = np.asarray(temp['data'])
        # predictions_1flow = model.predict(my_array.reshape(-1, 20, 128, 1))
        # one_flow_pred = int(np.argmax(predictions_1flow, axis=-1))

        # return str(one_flow_pred)
        return 1

        # with open(f"{self.thread_id}.json", "w") as outfile:
            # outfile.write(message)
        # src (ip-port) - dst(ip=port) - label - protocol (4-7)
        # 

    def run(self):
        print ('starting thread to consume from rabbit...')
        self.channel.start_consuming()

def main():
    for thread_id in range(config.THREADS):
        print ('launch thread', thread_id)
        td = ThreadedConsumer(thread_id=thread_id)
        td.start()

if __name__ == '__main__':
    main()
    # ctrl + c to exit

