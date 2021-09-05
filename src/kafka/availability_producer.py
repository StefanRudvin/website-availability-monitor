import json

from kafka import KafkaProducer


class AvailabilityProducer:
    """ Derived from https://github.com/aiven/aiven-examples/blob/master/kafka/python/producer_example.py """

    def __init__(self, service_uri, ca_path, cert_path, key_path, topic):
        print("Starting Availability Producer...")
        self.producer = KafkaProducer(
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            ssl_cafile=ca_path,
            ssl_certfile=cert_path,
            ssl_keyfile=key_path
        )
        self.topic = topic

    def send(self, website_availability_items):
        for website_availability_item in website_availability_items:
            self.producer.send(self.topic, json.dumps(website_availability_item.__dict__).encode('utf-8'))

        # Wait for all messages to be sent
        self.producer.flush()
