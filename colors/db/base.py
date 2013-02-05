import datetime

class APIBase(object):

    def __init__(self, root, db, *args):
        '''Create the APIBase object.

        @param root: iowho.db.IowhoAPI
            The top-level API object
        @param db: pymongo.Database
            The connection to the database
        @param args: additional arguments
            Additional arguments to pass to the subclass'''
            
        self.root = root
        self.db = db

        self.initialize(*args)

    def initialize(*args):
        '''Do nothing by default. Subclasses must implement this method.

        @param args: dict
            Additional initialization variables.'''

        pass

    @property
    def collection(self):
        '''Return a reference to the collection this APIBase represents.'''

        return self.db[self.COLLECTION_NAME]

    def create(self, data):
        '''Create a document for this collection.

        Return the id of the newly created document.

        @param data: dict
            The data to store in the document.'''

        data['created_at'] = datetime.datetime.utcnow()
        _id = self.collection.save(data)

        return _id

    def remove(self, _id):
        '''Delete the document with the given id.

        @param _id: bson.objectid.ObjectId
            The id of the document to delete.'''

        self.collection.remove({'_id': _id})

    def all(self):
        '''Return an iterator over all documents of this collection.'''

        return self.collection.find()

    def get(self, _id=None):
        '''Get an document by id.

        Returns the document, if it exists, otherwise raises an exception.

        @param _id: object
            The id of the document'''

        document = self.collection.find_one({'_id': _id})

        if document is None:
            raise Exception('%s document %s does not exist' %\
                (self.COLLECTION_NAME, _id))

        return document

    def update(self, _id, **kwargs):
        '''Update a document.

        @param _id: bson.objectid.ObjectId
            The id of the document to update.
        @param kwargs: key/value pairs
            the key/value pairs to set'''

        document = self.get(_id)

        if document is None:
            raise Exception('Document with id %s does not exist' % _id)

        for k,v in kwargs.iteritems():
            document[k] = v

        self.collection.save(document)
