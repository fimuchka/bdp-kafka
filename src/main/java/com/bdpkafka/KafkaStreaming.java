package com.bdpkafka;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.streams.Consumed;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.connect.json.JsonSerializer;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.streams.kstream.Produced;

import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.util.stream.Stream;

/**
 *
 */
public class KafkaStreaming {

    private static final String DEFAULT_BOOTSTRAP_SERVER = "localhost:9092";

    /**
     *
     * @param args
     * @throws Exception
     */
    public static void main(String[] args) throws Exception {

        final String bootstrapServer = args.length == 1 ? args[0] : DEFAULT_BOOTSTRAP_SERVER;
        System.out.println(bootstrapServer);
        // Create all the serializers/deserializers we're going to use
        final Serializer<JsonNode> jsonSerializer = new JsonSerializer();
        final Deserializer<JsonNode> jsonDeserializer = new JsonDeserializer();
        final Serde<String> stringSerde = Serdes.String();
        final Serde<JsonNode> jsonSerde = Serdes.serdeFrom(jsonSerializer, jsonDeserializer);

        // Create an empty stream builder
        StreamsBuilder builder = new StreamsBuilder();

        // Set the source from which we're going to read
        KStream<JsonNode, JsonNode> rawTransactionsSource = builder.stream("raw",
                Consumed.with(jsonSerde, jsonSerde));

        // Pre-process the raw stream to obfuscate it and create a key from the UserID
        KStream<String, JsonNode> obfuscatedTransactions = rawTransactionsSource
                // Obfuscate the account number
                .mapValues(value -> {
                    ObjectNode test = (ObjectNode) value;
                    String accountNum = test.get("AccntNum").asText();
                    test.put("AccntNum", "xxxx-" + accountNum.substring(2));
                    // need to cast to JsonNode to help compiler id the type
                    return (JsonNode) test;
                })
                //Need to generate a key for each message and so we select a UserID
                .selectKey((key, value) ->  value.get("UserID").asText())
                // The output has changed to key:String value:Json
                .through("logged_transactions", Produced.with(stringSerde, jsonSerde));

        // Read the table of flagged users
        KTable<String, JsonNode> flaggedAccounts = builder.table("flagged",
                Consumed.with(stringSerde, jsonSerde));
        // Join the flagged accounts on the incoming transactions to filter
        // out any transactions from users that have been already flagged
        // Those do not get written to the
        KStream<String, JsonNode> preprocessedTransactions = obfuscatedTransactions
                .leftJoin(flaggedAccounts, (trans, flagged) -> {
                    if (flagged == null) {
                        return trans;
                    }
                    // return a null node so we can filter out on it
                    return null;
                }).filter((key, value) -> value != null);

        // Output the filtered transactions to the preprocessed topic
        preprocessedTransactions.to("preprocessed", Produced.with(stringSerde, jsonSerde));

        // Set the properties of the stream container
        Properties streamsConf = KafkaStreaming.createStreamsConf(bootstrapServer);
        // Create the streams object to run; This is equivalent to Topology
        final KafkaStreams allStreams = new KafkaStreams(builder.build(), streamsConf);

        // This is for shutdown hook logic
        final CountDownLatch latch = new CountDownLatch(1);
        //Runtime.getRuntime().addShutdownHook(new Thread(allStreams::close));
        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread("bdp_streams") {
            @Override
            public void run() {
                allStreams.close();
                latch.countDown();
            }
        });

        try {
            allStreams.cleanUp();
            allStreams.start();
            latch.await();
        } catch (Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }

    /**
     *
     * @param bootstrapServer
     * @return
     * @throws Exception
     */
    public static Properties createStreamsConf(String bootstrapServer) throws Exception {
        Properties streamsConf = new Properties();
        streamsConf.put(StreamsConfig.APPLICATION_ID_CONFIG, "bdp_streaming1");
        streamsConf.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServer);
        streamsConf.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 10 * 1000);
        streamsConf.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        return streamsConf;
    }
}
