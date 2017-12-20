## Kakfa Streaming
Kafka streaming is a client library developed by Confluent that abstracts away a lot of the nitty gritty details
of writing streaming applications. Thus instead of using a Kafka Consumer and then building out a lot of your own logic to do complex streaming operations(joins and filters), you would use the streaming client library. For a deep introduction to Kafka streams, see the Kafka docs and the reference tutorials at the bottom of the README. What follows is a bullet point highlight of Kafka Streaming
_____________________________________________________________________________________________________
* A Kafka stream has a source (a topic it reads from), a processor (it does something with the source) and a sink (topi it writes to)
* Kafka streaming is composed of two things, a low level processor api and a "higher" level DSL. The tutorial uses this DSL, called the KStreams DSL
* The KStreams DSL has two abstractions:
    * A KStream: This is a view over the records where each key-value is independent and does not replace the previous. Thus, if you had `Bob->New York, Bob-> L.A., Bob->Chicago` and you read the stream from the beginning, you'd see all three messages
    * A KTable: In this view, later records are considered "updates" of earlier records. In this sense, it functions much like a database where records get overwritten. In the case above, all we would see would be `Bob->Chicago`. It's also known as a `changelog stream`
* Both of the abstractions offer mapping, filtering, reducing, joining and aggregation
* Join types:
    * Inner Joins: Emits a record when both sources have a key
    * Outer Joins: Always emits a record. If one source doesn't exist for a key, it's set to null
    * Left Joins: Emits for every record in the left stream. If the same key doesn't exist on the right hand stream, the right hand record is set to null
