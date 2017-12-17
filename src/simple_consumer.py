#!/bin/python3
"""
This script
"""
import argparse
import json
import pprint
import logging
import sys
import time
import multiprocessing


from sklearn.externals import joblib
from kafka import KafkaConsumer, KafkaProducer
#from kafka.errors import KafkaError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def consumer(kafka_broker, read_topic, write_topic, model_path):
    """"""
    consumer = KafkaConsumer(read_topic,
                             auto_offset_reset='earliest',
                             value_deserializer=lambda x: json.dumps(x).encode(
                                 "utf-8"))
    producer = KafkaProducer(bootstrap_servers=kafka_broker,
                             value_serializer=lambda x: json.dumps(x).encode(
                                 "utf-8"))
    for msg in consumer:
        # do stuff with it and then pass to model
        time.sleep(1)

def main(kafka_broker, read_topic, write_topic, model_path):
    """"""
    consumers = []
    for i in range(1): 
        p = multiprocessing.Process(target=consumer, name="Consumer {}".format(i),
                                    args=(kafka_broker, read_topic, write_topic, model_path))
        consumers.append(p)
        logger.INFO("Starting worker {}".format(i))
        p.start()
    for c in consumers:
        c.join()
        logger.INFO("Consumer finished with code {}".format(c.exitcode)) 


if __name__ == "__main__":
    # pylint: disable=C0103
    arg_parser = argparse.ArgumentParser(
        description=""" Kafka topic""")
    arg_parser.add_argument("--broker",
                            dest="kafka_broker",
                            default="localhost:9092",
                            help="""The url:port of the kafka broker
                                 (default is localhost:)""")
    arg_parser.add_argument("--read_topic",
                            dest="kafka_read_topic",
                            default="raw",
                            help="""The name of the Kafka topic to read data from
                                 (default is 'rawdata')""")
    arg_parser.add_argument("--write_topic",
                            dest="kafka_write_topic",
                            default="decision",
                            help="""The name of the Kafka topic to write data to
                                 (default is 'decision')""")
    arg_parser.add_argument("model_path", help="""Path to the pickled model""")
    args = arg_parser.parse_args()
    consumer(args.kafka_broker, args.kafka_read_topic, args.kafka_write_topic, args.model_path)

