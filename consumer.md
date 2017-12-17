## Kafka Consumers
Kafka consumers are grouped by use case or function. For example, we could hold one Kafka consumer group responsible for delivering records to high speed in memory micro-services, while another for streaming to Hadoop. 

Also, each consumer group has a unique id, and each one is a subscriber to one or more Kafka topics, which maintains its offset per topic partition. Therefore multiple subscribers are usually assigned to multiple consumer groups.
_____________________________________________________________________________________________________

Traditional messaging systems keep metadata on the broker either locally, or wait for acknowledgement from consumer
  * Works on a single machine server where many messaging systems don’t scale well
  * Broker deletes what’s consumed to keep data size small
  * Some adds an acknowledgement feature meaning messages are marked only as sent not consumed
  * Doesn’t lose information but problematic around performance
_____________________________________________________________________________________________________ 
 Design of Kafka Consumer
  * Load Share
     * Load balancing is achieved by having each consumer in consumer groups as an exclusive consumer of a fair share of partitions.
     * Consumer membership within a consumer group is handled by Kafka protocol dynamically
     * Each new consumer gets a share of partitions
     * If a consumer dies its partitions split among remaining living consumers.
  * Fail over
     * Consumers reports to Kafka broker when they successfully processed a record, advances the offset
     * Consumer fails before sending commit offset, a different consumer continues from the last committed offset.
     * Consumer fails after processing record but before sending commit,  then some records could be reprocessed
  * Offset management
     * Offset data stored in topic “__consumer_offset” which uses log compaction (which means it saves only the most recent value per key). Compacted logs are useful for restoring state after crash or system failure.
     * When data is processed, offsets must be committed. If it gets intervened, another consumer is still able to read from where it left off in “__consumer_offset” and takeover
  * Kafka consumers could only read messages beyond the last record that was replicated successfully to all the partition’s followers.
  * Load sharing redux
     * Only a single consumer from same consumer group can access a single partition
     * If number of consumer groups > partition count, extra consumers stay idle and available for failover
     * If number of consumer groups < partition count, reassign partition
  * Multi-threaded consumers
     * Using threads to run more than one consumers
      * Harder to manage offset for thread coordination
     * Always make sure that each consumer runs their own thread

