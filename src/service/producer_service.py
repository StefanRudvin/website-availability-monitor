from src.availability.website_availability_checker import website_availability_processor
import time

from src.kafka.availability_producer import AvailabilityProducer


def producer_service(service_uri, ca_path, cert_path, key_path, topic, ping_interval):
    producer = AvailabilityProducer(service_uri, ca_path, cert_path, key_path, topic)
    print("---> Starting website monitor service producer <---")
    while True:
        website_availability_items = website_availability_processor()

        print("Sending [" + str(len(website_availability_items)) + "] website availability events to Kafka.")
        producer.send(website_availability_items)
        print("Waiting for " + str(ping_interval) + " seconds...")
        time.sleep(ping_interval)
