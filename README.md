# bdp-kafka

## Quick resources:
 * [Github desktop](https://desktop.github.com/) -- easy source control via a GUI
 * [Docker for Windows Pro](https://store.docker.com/editions/community/docker-ce-desktop-windows)
 * [Docker for Windows Home](https://www.docker.com/products/docker-toolbox)
 * [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)
 * [Kafka Docker](https://hub.docker.com/r/wurstmeister/kafka/) Docker images with instructions on how to install
 * [Kafka Docker Repository](https://github.com/wurstmeister/kafka-docker) -- Repository for up to date kafka docker images
 * [Kafka project page](https://kafka.apache.org/)

## Credit Analyst - Model
 * Credit analysts could use machine learning techniques to train transaction data to identify fraudulent.
  * [Logistic Regression](https://github.com/fimuchka/bdp-kafka/blob/feature/intallation/Fraud%20Detection.ipynb)
  * [Random Forest](https://github.com/fimuchka/bdp-kafka/blob/feature/Lizzy1/creditcard%20fraud%20detection%20model.ipynb)
  * [Decision Tree](https://github.com/fimuchka/bdp-kafka/blob/feature/jfan33/fraudDetect1-Jessie.py)

## Dataset - Credit Card Transactions
 * The dataset contains transactions made by credit cards in September 2013 by european cardholders. This dataset presents transactions that occurred in two days, where we have 492 frauds out of 284,807 transactions. Features V1, V2, ... V28 are principal components obtained with PCA. The features which have not been transformed with PCA are 'Time' and 'Amount'. Feature 'Time' contains the seconds elapsed between each transaction and the first transaction in the dataset. The feature 'Amount' is the transaction amount. Feature 'Class' is the response variable and it takes value 1 in case of fraud and 0 otherwise.
 * We added three fake columns to the Kaggle dataset using R studio: unique user ID, user type (international or domestic) and unique account number
 * Columns appended could be used in future processing (i.e., aggregation) in application.
 * We split the processed dataset into training and test sets. Test set is split into two partitions. The screenshot shows a sample from the partitions.
 ![](./pics/data.png)
 * [Kaggle Dataset "Credit Card Transaction"](https://www.kaggle.com/dalpozz/creditcardfraud)
 * [Download the processed datasets](https://drive.google.com/open?id=1PldjXboPsbWmAhjWxlDUPwLF8_J5i_ka)