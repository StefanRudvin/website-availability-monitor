#!/usr/bin/env python3

import sys

from src.service.website_monitor_service import WebsiteMonitorService
from environs import Env
import os
import argparse


def main():
    """ Derived from https://github.com/aiven/aiven-examples/blob/master/kafka/python/main.py """

    parser = argparse.ArgumentParser()
    parser.add_argument('--service-uri', help="Service URI in the form host:port",
                        required=True)
    parser.add_argument('--ca-path', help="Path to project CA certificate",
                        required=True)
    parser.add_argument('--key-path', help="Path to the Kafka Access Key (obtained from Aiven Console)",
                        required=True)
    parser.add_argument('--cert-path', help="Path to the Kafka Certificate Key (obtained from Aiven Console)",
                        required=True)

    parser.add_argument('--consumer', action='store_true', default=False, help="Run Kafka consumer for the "
                                                                               "availability monitor")
    parser.add_argument('--producer', action='store_true', default=False, help="Run Kafka producer for the "
                                                                               "availability monitor")
    env = Env()
    env.read_env()
    validate_env(env)

    args = parser.parse_args()
    # validate_args(args)

    monitor_service = WebsiteMonitorService(
        args.service_uri,
        args.ca_path,
        args.cert_path,
        args.key_path,
        env.str("WEBSITE_MONITOR_AVAILABILITY_TOPIC"),
        env.int("PING_INTERVAL_SECONDS"),
        env.str("WEBSITE_MONITOR_TABLE_NAME"))

    if args.producer:
        monitor_service.run_producer()
    elif args.consumer:
        monitor_service.run_consumer()


def validate_env(env):
    for env_param in ("WEBSITE_MONITOR_AVAILABILITY_TOPIC", "PING_INTERVAL_SECONDS", "WEBSITE_MONITOR_TABLE_NAME"):
        try:
            env.str(env_param)
        except:
            fail(f"Failed to retrieve env_param :: {env_param} :: from env file.\n"
                 f"You can set these to your liking in the env file.")


def validate_args(args):
    for path_option in ("ca_path", "key_path", "cert_path"):
        path = getattr(args, path_option)
        if not os.path.isfile(path):
            fail(f"Failed to open --{path_option.replace('_', '-')} at path: {path}.\n"
                 f"You can retrieve these details from Overview tab in the Aiven Console")
    if args.producer and args.consumer:
        fail("--producer and --consumer are mutually exclusive")
    elif not args.producer and not args.consumer:
        fail("--producer or --consumer are required")


def fail(message):
    print(message, file=sys.stderr)
    exit(1)


if __name__ == '__main__':
    main()
