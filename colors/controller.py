import logging

from colors.db import ColorsAPI
from colors.mq import MQ

class ColorsController(object):
    '''A class for grouping together database transactions and notifications.'''

    def __init__(self, host='localhost'):
        '''Create the ColorsController.

        @param host: str
            The location of the database AND message queue.'''

        self.api = ColorsAPI(host=host)
        self.mq = MQ(host=host)

    def create_block(self, color, frequency=None):
        '''Create a block with the supplied color.

        @param color: str
            A 6 hex digit color.'''

        _id = self.api.blocks.create(color, frequency=frequency)
        self.mq.publish_block_created(_id)

        return _id

    def delete_block(self, block_id):
        '''Delete the block with the given id.

        @param block_id: bson.objectid.ObjectId
            The id of the block to delete.'''

        self.api.blocks.remove(block_id)
        self.mq.publish_block_deleted(block_id)

    def change_block_color(self, block_id, color):
        '''Change a block color, then notify listeners on the message queue.

        @param block_id: bson.objectid.ObjectId
            The id of the block whose color will be changed.
        @param color: str
            A 6 hex digit color.'''

        try:
            self.api.blocks.update(block_id, color=color)
            self.mq.publish_color_changed(block_id, color)
        except Exception as e:
            logging.exception(e)

    def change_block_frequency(self, block_id, frequency):
        '''Change a block color, then notify listeners on the message queue.

        @param block_id: bson.objectid.ObjectId
            The id of the block whose color will be changed.
        @param frequency: float
            The number of seconds in between color changes.'''

        try:
            self.api.blocks.update(block_id, frequency=frequency)
            self.mq.publish_frequency_changed(block_id, frequency)
        except Exception as e:
            logging.exception(e)

    
