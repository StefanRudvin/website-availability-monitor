from kafka import KafkaConsumer


def availability_consumer(service_uri, ca_path, cert_path, key_path, topic):
    """ Derived from https://github.com/aiven/aiven-examples/blob/master/kafka/python/consumer_example.py"""
    print("Starting Availability Consumer...")
    consumer = KafkaConsumer(
        bootstrap_servers=service_uri,
        auto_offset_reset='earliest',
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        consumer_timeout_ms=1000,
    )

    consumer.subscribe([topic])
    for message in consumer:
        print(message.value.decode('utf-8'))

    """
    Validate 
    """
    consumer.close()