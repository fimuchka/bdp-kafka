#!/bin/python3
"""
This script parses a csv and sends its data to a Kafka topic
"""
import argparse
import csv
import json
import pprint

from kafka import KafkaProducer
#from kafka.errors import KafkaError


def read_data(file_path):
    """Yield a dictionary of header/line for each line in csv"""
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for line in reader:
            yield dict(zip(header, line))


def main(kafka_broker, kafka_topic, file_path):
    """Parse the csv and send every line to the kafka topic"""
    producer = KafkaProducer(bootstrap_servers=kafka_broker,
                             value_serializer=lambda x: json.dumps(x).encode(
                                 "utf-8"))
    for item in read_data(file_path):
        producer.send(kafka_topic, item)
    producer.close()
    pprint.pprint(producer.metrics())


if __name__ == "__main__":
    # pylint: disable=C0103
    arg_parser = argparse.ArgumentParser(
        description="""This script reads in a csv(with header) and send each line
                      zipped with the header in json format to a Kafka topic""")
    arg_parser.add_argument("--broker",
                            dest="kafka_broker",
                            default="localhost:9092",
                            help="""The url:port of the kafka broker
                                 (default is localhost:)""")
    arg_parser.add_argument("--topic",
                            dest="kafka_topic",
                            default="raw",
                            help="""The name of the Kafka topic to send data to
                                 (default is 'rawdata')""")
    arg_parser.add_argument("file_path", help="Path to the csv file to read")
    args = arg_parser.parse_args()
    main(args.kafka_broker, args.kafka_topic, args.file_path)

