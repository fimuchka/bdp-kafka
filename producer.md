## Kafka Producer
    * Picks partition to send records (messages) to topics based on the record’s key
    * Producers writes do not guarantee the order of records across partitions
    * Load balancing
        * Producer sends data directly to the broker (leader for partition)
            * To enable this  all nodes could answer which servers are alive and where leaders for the partitions of a top are at any given time
        * Client controls which partition it publishes message to
            * Random load balancing
            * Semantic partitioning function
                * User specifies key to partition and use this to hash to partition
                * Locality sensitive processing enabled
        * Asynchroous send
            * Batching  enabled because Kafka producer attempt to accumulate data in. Memory and send out larger batches in a single request
            * Configurable buffering gives a fair tradeoff of sacrificing a small bit of latency and actual throughput