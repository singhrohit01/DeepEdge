import MySQLdb
from helpers.util import echo

class Connection:
    """
        Helper class to perform database operations
    """

    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.__con = None
        self.__cursor = None

    def __enter__(self):
        return self
  
    def __exit__(self, exc_type, exc_value, traceback):
        if (self.__con is not None):
            self.__con.close()

    def connect(self):
        """ Returns a database connection with the specified credentials """
        if (self.__con is None):
            self.__con = MySQLdb.connect(host=self.host,  # your host 
                        # port=3306,
                        user=self.user,       # username
                        passwd=self.passwd,     # password
                        db=self.db)   # name of the database
            echo("Connection established")
        return self.__con

    def __getCursor(self):
        if (self.__cursor is None):
            self.__cursor = self.connect().cursor()
        return self.__cursor

    def execute_query(self, query):
        self.__getCursor().execute(query)
        return self.__getCursor()

    def commit(self):
        return self.connect().commit()
