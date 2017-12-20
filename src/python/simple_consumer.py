#!/bin/python3
"""
This script
"""
import argparse
import json
import logging
import sys
import multiprocessing
import random
import os


from sklearn.externals import joblib
from kafka import KafkaConsumer, KafkaProducer
# from kafka.errors import KafkaError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def analyzer(kafka_broker, read_topic, write_topic, model_path):
    """Continuously read from a Kafka topic, use a model to predict
    a value and then write that value to another Kafka topic"""
    consumer = KafkaConsumer(read_topic,
                             auto_offset_reset='earliest',
                             key_deserializer= lambda x: x.decode("utf-8"),
                             value_deserializer=lambda x: json.loads(x),
                             bootstrap_servers=[kafka_broker])
    producer = KafkaProducer(bootstrap_servers=kafka_broker,
                             key_serializer=lambda x: x.encode("utf-8"),
                             value_serializer=lambda x: json.dumps(x).encode(
                                 "utf-8"))
    try:
        for msg in consumer:
            features = {k: v for k,v in msg.value.items() if k not in
                        ['Time', 'AccntNum', 'Class', 'UserType', 'UserID']}
            # do stuff with it and then pass to model
            if msg.key == None:
                producer.send(write_topic, key=value["UserID"], value={"flag": bool(random.getrandbits(1))})
            else:
                producer.send(write_topic, key=msg.key, value={"flag": bool(random.getrandbits(1))})
            producer.flush()
    except (KeyboardInterrupt, SystemExit):
        logger.info("KeyboardInterrupt")
    finally:
        logger.info("Closing producer and consumer")
        consumer.close()
        producer.close()


def main(kafka_broker, read_topic, write_topic, folder_path):
    """Launch as many processes to read from a Kafka topic as we
    have models in the folder_path"""
    analyzers = []
    for i, name in enumerate(os.listdir(folder_path)):
        p = multiprocessing.Process(target=analyzer, name="Consumer {}".format(i),
                                    args=(kafka_broker, read_topic, write_topic,
                                          os.path.join(folder_path, name)))
        analyzers.append(p)
        logger.info("Starting worker {}".format(i))
        p.start()
    for a in analyzers:
        a.join()
        logger.info("Consumer finished with code {}".format(c.exitcode))


if __name__ == "__main__":
    # pylint: disable=C0103
    arg_parser = argparse.ArgumentParser(
        description=""" Kafka topic""")
    arg_parser.add_argument("--broker",
                            dest="kafka_broker",
                            default="kafka:9092",
                            help="""The url:port of the kafka broker
                                 (default is localhost:)""")
    arg_parser.add_argument("--read_topic",
                            dest="kafka_read_topic",
                            default="preprocessed",
                            help="""The name of the Kafka topic to read data from
                                 (default is 'preprocessed')""")
    arg_parser.add_argument("--write_topic",
                            dest="kafka_write_topic",
                            default="decision",
                            help="""The name of the Kafka topic to write data to
                                 (default is 'decision')""")
    arg_parser.add_argument("folder_path", help="""Path to the folder of the pickled models""")
    args = arg_parser.parse_args()
    main(args.kafka_broker, args.kafka_read_topic, args.kafka_write_topic, args.folder_path)

