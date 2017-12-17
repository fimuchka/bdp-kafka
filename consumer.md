## Kafka Consumers
  * In Groups
      * Consumer grouped by use case or function
      * e.g. one responsible for delivering records to high speed in memory micro-services, while another does streaming to Hadoop.
    * Each consumer group has a unique id, each one is subscriber to one or more Kafka topics, maintains its offset per topic partition
    * Multiple subscribers—>multiple consumer groups
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
     * Offset data stored in topic “__consumer_offset”
      * Use log compaction, saves only the most recent value per key
      * When processed data, must commit offsets.
      * Even when it dies, still able to read from where it left off in “__consumer_offset” and lets another consumer takeover
  * What can Kafka consumers read?
     * data with replicates
     * Messages beyond the last record that was replicated successfully to all the partition’s followers.
     * Log end offset is last record’s offset written to log partition and where producers writes to next
  * Load sharing redux
     * Only a single consumer from same consumer group can access a single partition
     * If number of consumer groups > partition count, extra consumers stay idle and available for failover
     * If number of consumer groups < partition count, reassign partition
  * Multi-threaded consumers
     * Using threads to run more than one consumers
      * Harder to manage offset for thread coordination
     * Always make sure that each consumer runs their own thread

