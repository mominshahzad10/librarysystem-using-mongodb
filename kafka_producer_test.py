from kafka import KafkaProducer

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Define the topic to which you want to send a message
topic = 'test_topic'

# Send a test message to the Kafka topic
message = 'This is a test message.'
producer.send(topic, message.encode('utf-8'))

# Close the producer
producer.close()

print('Message sent to Kafka successfully.')
