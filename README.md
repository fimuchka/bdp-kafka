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
 * Now we'll install the python requirements. If on Windows and you installed Miniconda for python, start the Miniconda prompt, and navigate to the bdf-kafka directory where the `requirements.txt` file is
 ```bash
 pip install -r requirements.txt
 ``` 
 * Run the script to push data to the Kafka brokers
 ```bash
 python src/activity_producer.py <path_to_downloaded_and_unzipped_dataset>
 ```
 * Lets verify the messages are there. This involves once again going into the docker container.
 ```bash
 docker exec -it bdpkafka_kafka_1 bash
 # Now you're in the container:
 kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic raw
 ```
 * You should see the number of messages in the topic, which should be one less than the number of lines in your csv file(i.e. minus the header)
 * To stop the docker containers:
 ```bash
 docker compose down
 ```
