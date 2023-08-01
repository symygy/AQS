from kafka import KafkaConsumer, consumer
from time import sleep
import json


class MessageConsumer:
    broker = ""
    topic = ""
    group_id = ""
    logger = None

    def __init__(self, broker, topic, group_id):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id

    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers=self.broker,
                                 group_id='my-group',
                                 consumer_timeout_ms=600000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

        consumer.subscribe(self.topic)
        print("consumer is listening....")
        try:
            for message in consumer:
                print(message)

                consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()

if __name__=='__main__':
    broker = '192.168.1.26:9092'
    topic = 'gios_atmo_data'
    group_id = 'consumer-1'

    consumer1 = MessageConsumer(broker,topic,group_id)
    consumer1.activate_listener()

