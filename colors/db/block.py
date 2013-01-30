import os
import shutil

from bson.objectid import ObjectId

from colors.db.base import APIBase

class BlockAPI(APIBase):

    COLLECTION_NAME = 'blocks'

    def create(self, color, frequency=None):
        '''Create a color block.

        Returns the id of the newly created dataset document.

        @param color: str
            The six (hex) digit value for a color.
        @param frequency: optional, float
            The frequency at which the color should change'''

        block = dict(
            color=color,
            frequency=frequency,
        )
        _id = super(BlockAPI, self).create(block)

        return _id
