# bdp-kafka

## Quick resources:
 * [Github desktop](https://desktop.github.com/) -- easy source control via a GUI
 * [Docker for Windows Pro](https://store.docker.com/editions/community/docker-ce-desktop-windows)
 * [Docker for Windows Home](https://www.docker.com/products/docker-toolbox)
 * [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)
 * [Kafka Docker](https://hub.docker.com/r/wurstmeister/kafka/) Docker images with instructions on how to install
 * [Miniconda](https://conda.io/miniconda.html) If you need to install Python on your system
 * [Kafka Docker Repository](https://github.com/wurstmeister/kafka-docker) -- Repository for up to date kafka docker images
 * [Kafka project page](https://kafka.apache.org/)

## Dataset
 * [Credit card fraud](https://www.kaggle.com/dalpozz/creditcardfraud) 

## Instructions

 * Install git or the github desktop client
 * Install docker with docker-compose
 * If you need to install python 3, you can use Miniconda above
 * Clone this repository
 * Download the dataset and unzip it
 * Start the docker containers
  ```bash
  docker-compose up -d
   ```
 * Verify that the containers are up. Neither container should say `Exited`
 ```bash
  docker ps -a
 ```
 * To view that the topics were created successfully, we need to use the Kafka container to run the kafka scripts.
 ```bash
  docker exec bdpkafka_kafka_1 bash -c 'kafka-topics.sh  --list --zookeeper $KAFKA_ZOOKEEPER_CONNECT'
 ```
 * You should see 3 topics listed: `raw`, `preprocessed`, `decision`
 * Copy the dataset we're using to seed Kafka to the python container
 ```bash
 docker cp <path_to_downloaded_and_unzipped_dataset> bdpkafka_python_1:/tmp/creditcard.csv
 ```
 * Run the script to push data to the Kafka brokers
 ```bash
 docker exec bdpkafka_python_1 python /bdp/activity_producer.py /tmp/creditcard.csv
 ```
 * Lets verify the messages are there. This involves once again running a command with the kafka  docker container.
 ```bash
 docker exec bdpkafka_kafka_1 bash -c 'kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list kafka:9092 --topic raw'
 ```
 * You should see the number of messages in the topic, which should be one less than the number of lines in your csv file(i.e. minus the header)
 * To stop the docker containers:
 ```bash
 docker-compose down
 ```

#### Multi-broker and topic partitions
 * Now let's create 2 brokers and multiple partitions for topics.
 ```bash
  docker-compose up --scale kafka=2 -d
 ```
 * Verify that 3 docker images are up, two kafka and one zookeeper
 ```bash
  docker ps -a
 ```
 * Now let's verify that the partitions were created as we expected
 ```bash
  docker exec bdpkafka_kafka_1 bash -c 'kafka-topics.sh  --describe --zookeeper $KAFKA_ZOOKEEPER_CONNECT --topic raw'
 ```
 * You should get an output of:

| *Topic raw* |*PartitionCount 2* | ReplicationFactor 2*| Configs | |
| ---:            | ---: | ---: | ---: | ---:|
|Topic - raw|Partition - 0|Leader - 1002|Replicas - 1002,1001|Isr - 1002,1001|
|Topic-  raw|Partition - 1|Leader- 1001|Replicas-1001,1002|Isr- 1001,1002|
 * Now run the same command changin the topic name and observe that topic `preprocessed` has 2 partitions but no replication and topic `decision` has 1 partition and a replication factor of 2
