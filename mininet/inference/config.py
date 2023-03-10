# package capture
RABBIT_URL="rabbitmq"

CONSUMER_QUEUE= 'raw_data'
CONSUMER_ROUTING_KEY = 'raw_data'

PRODUCER_QUEUE = 'predict_data'
PRODUCER_ROUTING_KEY = 'predict_data'

# debug result by using mongo
DEBUG = "true"
MONGO_URL = 'mongodb://admin:admin@mongodb:27017'

# tensorflow worker
EXCHANGE = 'events'
THREADS = 1
PREFETCH_COUNT = 2 * THREADS
PADDING = 1640
BYTES_PER_PACKET = 256