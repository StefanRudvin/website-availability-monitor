from src.availability.website_availability_checker import website_availability_processor
import time

from src.data.availability_dao import AvailabilityDao


class WebsiteMonitorService:

    def __init__(self, service_uri, ca_path, cert_path, key_path, topic, ping_interval, table_name):
        #self.producer = AvailabilityProducer(service_uri, ca_path, cert_path, key_path, topic)
        self.dao = AvailabilityDao(service_uri, table_name)
        self.ping_interval = ping_interval
        pass

    def run_producer(self):
        print("Starting website monitor service producer...")

        while True:
            website_availability_items = website_availability_processor()

            print("Sending [" + str(len(website_availability_items)) + "] website availability events to Kafka.")
            #self.producer.send()
            # First just create the DB and call it
            self.dao.save(website_availability_items)
            self.dao.fetch_all_test()
            time.sleep(self.ping_interval)

    def run_consumer(self):
        print("Starting website monitor service consumer...")
        pass