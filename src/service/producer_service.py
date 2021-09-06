import time

from src.kafka.availability_producer import AvailabilityProducer
from src.processing.website_availability_processor import website_availability_processor


def producer_service(service_uri, ca_path, cert_path, key_path, topic, ping_interval):
    producer = AvailabilityProducer(service_uri, ca_path, cert_path, key_path, topic)
    print("---> Starting website monitor service producer <---")
    while True:
        run(producer, ping_interval)


def run(producer, ping_interval):
    website_availability_items = website_availability_processor()

    print("Sending [" + str(len(website_availability_items)) + "] website processing events to Kafka.")
    producer.send(website_availability_items)
    print("Waiting for " + str(ping_interval) + " seconds...")
    time.sleep(ping_interval)
