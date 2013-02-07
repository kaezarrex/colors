import pymongo

from colors.db.block import BlockAPI

class ColorsAPI(object):
    '''A class for abstracting away the database connection''' 

    def __init__(self, host='localhost', database='color'):
        '''Create a connection to mongoDB

           @param host : optional, str
               The host of the mongoDB server, defaults to localhost
           @param port : optional, int
               The port of the mongoDB server, defaults to 27017
           @param user : optional, str
               The user to connect to mongoDB as, defaults to None
           @param password : optional, str
               The password for the user, defaults to None
           @param database : optional, str
               The name of the database to connect to, defaults to "colors"'''

        connection = pymongo.Connection(host=host)
        db = pymongo.database.Database(connection, database)

        #if user and password:
        #    success = db.authenticate(user, password)
        #    if not success:
        #        raise Exception('could not authenticate with the db')

        self.blocks = BlockAPI(self, db)
