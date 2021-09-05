import json

from kafka import KafkaConsumer

from src.data.availability_dao import AvailabilityDao
from src.models.website_availability_item import WebsiteAvailabilityItem


def consumer_service(service_uri, ca_path, cert_path, key_path, topic, table_name, db_service_uri):
    """ Derived from https://github.com/aiven/aiven-examples/blob/master/kafka/python/consumer_example.py"""

    consumer = KafkaConsumer(
        bootstrap_servers=service_uri,
        auto_offset_reset='earliest',
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        consumer_timeout_ms=1000,
        group_id='website-availability-monitor-consumer-1'
    )

    dao = AvailabilityDao(db_service_uri, table_name)

    print("Starting website monitor service consumer...")
    while True:
        availability_items = []
        consumer.subscribe([topic])

        for message in consumer:
            json_item = json.loads(message.value.decode('utf-8'))
            availability_items.append(WebsiteAvailabilityItem(json_item['website_url'],
                                                              json_item['status_code'],
                                                              json_item['response_time'],
                                                              json_item['regex_pattern_matches']))
        if availability_items:
            dao.save(availability_items)
        consumer.commitAsync()
