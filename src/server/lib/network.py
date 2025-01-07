import common.random
import requests

class Client:
    def __init__(self):
        self.connection_ID = common.random.generate_random_uuid()
        self.connection_KEY = common.random.generate_random_string(32)

    def prepare_connection(self):
        pass

    
