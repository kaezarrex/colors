import json

import pika

EXCHANGE = 'colors'
TASKS_QUEUE = 'colors.tasks'
TASKS_ROUTING_KEY = TASKS_QUEUE
NOTIFICATION_ROUTING_KEY = 'colors.notifications'

class MQ(object):
    '''A class for managing communication with the message queue.'''

    def __init__(self, host='localhost', virtual_host=None, username=None, password=None):

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                virtual_host=virtual_host,
                credentials=pika.PlainCredentials(username=username, password=password)
                )
            )

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

    def publish_notification(self, notification_type, notification):
        '''Publish a notification.

        @param notification_type: unicode
            The type of notification to publish
        @param notification: dict
            Additional data to pass along.'''

        notification['type'] = notification_type
        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=NOTIFICATION_ROUTING_KEY,
            body=json.dumps(notification)
        )

    def publish_color_changed(self, block_id, color):
        '''Publish that a block's color has successfully been changed.

        @param block_id: bson.ObjectId
            The id of the block whose color will be changed.
        @param color: str
            The new 6 hex digit color.'''

        notification = {
            'block_id': str(block_id),
            'color': color,
        }

        self.publish_notification('change-color', notification)

    def publish_frequency_changed(self, block_id, frequency):
        '''Publish that a block's frequency has successfully been changed.

        @param block_id: bson.ObjectId
            The id of the block whose color will be changed.
        @param frequency: float
            The color change frequency.'''

        notification = {
            'block_id': str(block_id),
            'frequency': frequency,
        }

        self.publish_notification('change-frequency', notification)

    def publish_block_created(self, block_id):
        '''Publish that a block has been created.

        @param block_id: bson.ObjectId
            The id of the added block.'''

        notification = {
            'block_id': str(block_id),
        }

        self.publish_notification('block-created', notification)


    def publish_block_deleted(self, block_id):
        '''Publish that a block has been deleted.

        @param block_id: bson.ObjectId
            The id of the removed block.'''

        notification = {
            'block_id': str(block_id),
        }

        self.publish_notification('block-deleted', notification)

