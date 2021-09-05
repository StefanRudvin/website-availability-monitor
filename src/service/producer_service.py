from src.availability.website_availability_checker import website_availability_processor
import time

from src.kafka.availability_producer import AvailabilityProducer


class ProducerService:

    def __init__(self, service_uri, ca_path, cert_path, key_path, topic, ping_interval):
        self.producer = AvailabilityProducer(service_uri, ca_path, cert_path, key_path, topic)
        self.ping_interval = ping_interval

    def run(self):
        print(">> --- Starting website monitor service producer --- <<")
        while True:
            website_availability_items = website_availability_processor()

            print("Sending [" + str(len(website_availability_items)) + "] website availability events to Kafka.")
            self.producer.send(website_availability_items)
            print("Waiting for " + str(self.ping_interval) + " seconds...")
            time.sleep(self.ping_interval)
