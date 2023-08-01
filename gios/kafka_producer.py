from kafka import KafkaProducer
import json

class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks='all',
        retries = 3)


    def send_msg(self, msg):
        print("sending message...")
        try:
            future = self.producer.send(self.topic,msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex


if __name__=='__main__':
    broker = '192.168.1.26:9092'
    topic = 'gios_atmo_data'
    message_producer = MessageProducer(broker,topic)

    data = {'name':'abc4', 'email':'abc@example.com'}
    resp = message_producer.send_msg(data)
    print(resp)