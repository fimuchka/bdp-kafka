# bdp-kafka

## Quick resources:
 * [Github desktop](https://desktop.github.com/) -- easy source control via a GUa
 * [Docker for Windows Pro](https://store.docker.com/editions/community/docker-ce-desktop-windows)
 * [Docker for Windows Home](https://www.docker.com/products/docker-toolbox)
 * [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)
 * [Kafka Docker](https://hub.docker.com/r/wurstmeister/kafka/) Docker images with instructions on how to install
 * [Miniconda](https://conda.io/miniconda.html) If you need to install Python on your system
 * [Kafka Docker Repository](https://github.com/wurstmeister/kafka-docker) -- Repository for up to date kafka docker images
 * [Kafka project page](https://kafka.apache.org/)

## Dataset 
 * The dataset contains transactions made by credit cards in September 2013 by european cardholders. This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. Features V1, V2, ... V28 are principal components obtained with PCA. The features which have not been transformed with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first transaction in the dataset. The feature 'Amount' is the transaction amount. Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise. 
 * We added three fake columns to the Kaggle dataset using R studio: unique user ID, user type (international or domestic) and unique account number
 * Columns appended could be used in furture processing (i.e., aggregation) in application.
 * We split the processed dataset into training and test sets.
 * [Kaggle Dataset "Credit Card Transaction"](https://www.kaggle.com/dalpozz/creditcardfraud) 
 * [Download the processed datasets](https://drive.google.com/open?id=1QIeiHcDd0JGeK8jWN-GQskRY-3lvG9R8)
 
## Model
 * Fraud detection model using logistics regression
 
## Kafka Stories and Introduction
Apache Kafka is a high-throughput distributed streaming platform and messaging system developed by the Apache Software Foundation written in Scala and Java. 

Kafka is implemented as a commit log for a distributed system. In a database context, a "commit" is the application of a single transaction to the database. A commit log is a record of transactions. It's used to keep track of what's happening and help with disaster recovery. In general, all commits are written to the log before being applied. Therefore, transactions that are in flight when the server goes down can be recovered and re-applied by checking the log. 
Apache Kafka was originally developed by LinkedIn to process activity stream data from their website. Kafka was subsequently open sourced in early 2011. In November 2014, several engineers who worked on Kafka at LinkedIn created a new company named Confluent with a focus on Kafka. According to a Quora post from 2014, Jay Kreps seems to have named it after the author Franz Kafka. Kreps chose to name the system after an author because it is "a system optimized for writing", and he liked Kafka's work. 

Kafka aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds. Kafka could also connect to external systems for data import or export via Kafka Connect and provides Kafka Streams.

## Terminology
At a high level, producers send messages over the network to the Kafka cluster. Kafka cluster in turn serves them up to consumers. There are many subscribers to a message. Subscribers or clients store the state of their reads. All the messages in Kafka are real-time and are retained for a specific time period. It is easy to replay messages.

 * Message: A datum to send
 * Topic: Kafka maintains messages in categories called "topic"
 * Partition: A logical division of a topic; each partition is an ordered, immutable sequence of messages; a partition log is maintained for each topic
 * Producer: An API to publish messages to Kafka topics
 * Broker: A server
 * Cluster: A Kafka cluster comprises one or more brokers
 * Consumer: A Kafka cluster comprises one or more brokers; a consumer is an API to consume messages from topics
 * Replication: Kafka replicates log for earch partition across servers
 
## Kafka's Advantages in Messaging
 * In comparison to most messaging systems Kafka has better throughput, built-in partitioning, replication, and fault-tolerance which makes it a good solution for large scale message processing applications.
 * Each message in partition is assigned a sequential ID number called "offset".

## Metric - Application
Kafka is often used for operational monitoring data. This involves aggregating statistics from distributed applications to produce centralized feeds of operational data. 

## Stream Processing
 * Concept: Many users of Kafka process data in processing pipelines consisting of multiple stages, where raw input data is consumed from Kafka topics and then aggregated, enriched, or otherwise transformed into new topics for further consumption or follow-up processing.
 * Library: stream processing library called Kafka Streams is available in Apache Kafka

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
 * Now let's see one of the messages
 ```bash
  docker exec bdpkafka_kafka_1 bash -c 'kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic raw  --property print.key=true --property key.separator="|--|" --from-beginning --max-messages 1'
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

#### Kafka streaming
 * Get the address of one of the brokers so we can interact with it
 ```bash
 docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bdpkafka_kafka_1
 ```
 * Use the result of the above as the <container_ip> in the following commands. Start the preprocessing stream
 ```bash
 docker exec -it bdpkafka_kafka_2 bash -c 'KAFKA_DEBUG=t /opt/kafka/bin/kafka-run-class.sh com.bdpkafka.KafkaStreaming <container_ip>:9092'
 ```
