# bdp-kafka

## Quick resources:
 * [Github desktop](https://desktop.github.com/) -- easy source control via a GUI
 * [Docker for Windows Pro](https://store.docker.com/editions/community/docker-ce-desktop-windows)
 * [Docker for Windows Home](https://www.docker.com/products/docker-toolbox)
 * [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)
 * [Kafka Docker](https://hub.docker.com/r/wurstmeister/kafka/) Docker images with instructions on how to install
 * [Kafka Docker Repository](https://github.com/wurstmeister/kafka-docker) -- Repository for up to date kafka docker images
 * [Kafka project page](https://kafka.apache.org/)

## Dataset
 * [Credit card fraud](https://www.kaggle.com/dalpozz/creditcardfraud) 

## Instructions

 * Install git or the github desktop client
 * Install docker with docker-compose
 * Clone this repository
 * Download the dataset
 * Start the docker containers
  ```bash
  docker-compose up -d
   ```
 * Verify that the containers are up. Neither container should say `Exited`
 ```bash
  docker ps -a
 ```
 * To view that the topics were created successfully, we need to interact with Kafka from within one of the containers.
 ```bash
  docker exec -it bdpkafka_kafka_1 bash
 ```
 * Now you're inside the container. There you can run some install kafka scripts.
 ```bash
  kafka-topics.sh  --list --zookeeper $KAFKA_ZOOKEEPER_CONNECT
 ```
 * You should see 3 topics listed: `raw`, `preprocessed`, `decision`
 * To exit the docker container press Ctrl-D
 * To stop the docker containers:
 ```bash
 docker compose down
 ```
