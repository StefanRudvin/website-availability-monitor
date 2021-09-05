import time

from src.data.availability_dao import AvailabilityDao


def logging_service(service_uri, table_name):
    dao = AvailabilityDao(service_uri, table_name)
    while True:
        [print(x) for x in dao.get_recent_updates(10)]
        time.sleep(5)
