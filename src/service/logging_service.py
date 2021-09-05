import time

from src.data.availability_dao import AvailabilityDao


class LoggingService:
    def __init__(self, service_uri, table_name):
        self.dao = AvailabilityDao(service_uri, table_name)

    def run(self):
        while True:
            self.dao.get_recent_updates(10)
            time.sleep(5)
