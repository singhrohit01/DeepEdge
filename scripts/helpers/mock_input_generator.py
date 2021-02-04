
from helpers.util import read_JSON, echo
from helpers.db_connector import Connection


class MockInputGenerator:
    """
        This class currently fetches images from the database as input
        TODO : make this an interface; create a new concrete class (say DBImageReader) which performs the actual jobs
    """

    def __init__(self, limit=100):
        self.con = None
        self.offset = 0
        self.limit = limit
        self.counter = 0
        self.results = []

        config_file = "config.json"
        config = read_JSON(config_file)

        self.db_credentials = config["credentials"]["database"][config["db_provider"]]
        self.table = "datasets"

    def __get_connection(self):
        if (self.con is None):
            self.con = Connection(self.db_credentials["host"], self.db_credentials["username"], self.db_credentials["password"], self.db_credentials["db"])

        return self.con

    def next_input(self):
        """ Returns the name of the image file fetched from the database """

        self.counter += 1
        if len(self.results) < self.counter:
            query = "SELECT * FROM {} LIMIT {} OFFSET {}".format(self.table, self.limit, self.offset)
            c = self.__get_connection().execute_query(query)
            self.results = c.fetchall()
            self.offset += self.limit

        if self.results is not None or len(self.results) > 0:
            image_data = self.results[self.counter][1]

            filename = "result_file"

            with open(filename, 'wb') as f:
                f.write(image_data)

            return { "id" : self.counter, "data_file" : filename }

        return None
