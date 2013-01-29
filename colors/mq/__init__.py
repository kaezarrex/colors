import pika

EXCHANGE = 'colors'

class MQ(object):
    '''A class for managing communication with the message queue.'''

    def __init__(self, host='localhost'):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))

        channel = connection.channel()

        # Set up the exchange for routing messages through. It will be a topic
        # exchange, which means that the routing keys can be wildcard matched.
        channel.exchange_declare(exchange=EXCHANGE)


