import json

import pika

EXCHANGE = 'colors'
TASKS_QUEUE = 'colors.tasks'
TASKS_ROUTING_KEY = TASKS_QUEUE
NOTIFICATION_ROUTING_KEY = 'colors.notifications'

class MQ(object):
    '''A class for managing communication with the message queue.'''

    def __init__(self, host='localhost'):

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))

        channel = self.get_channel()

        # Set up the exchange for routing messages through. It will be a topic
        # exchange, which means that the routing keys can be wildcard matched.
        channel.exchange_declare(exchange=EXCHANGE)

        # Set up the tasks queue
        channel.queue_declare(queue=TASKS_QUEUE)
        # Bind the queue to the exchange with a specific routing key
        channel.queue_bind(exchange=EXCHANGE, 
            queue=TASKS_QUEUE, 
            routing_key=TASKS_ROUTING_KEY)

        self.channel = channel

    def get_channel(self):
        '''Return a channel.'''

        return self.connection.channel()

    def queue_color_change(self, block_id):
        '''Add a color change task to the work queue.

        @param block_id: bson.ObjectId
            The id of the block whose color will be changed.'''

        task = {
            'type': 'change-color',
            'block_id': str(block_id)
        }

        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=TASKS_ROUTING_KEY,
            body=json.dumps(task)
        )

    def publish_color_change(self, block_id, color):
        '''Publish that a block's color has successfully been changed.

        @param block_id: bson.ObjectId
            The id of the block whose color will be changed.
        @param color: str
            The new 6 hex digit color.'''

        notification = {
            'type': 'change-color',
            'block_id': str(block_id),
            'color': color,
        }

        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=NOTIFICATION_ROUTING_KEY,
            body=json.dumps(notification)
        )
