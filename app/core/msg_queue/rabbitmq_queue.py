import pika
from pika.adapters.blocking_connection import BlockingChannel
from app.config import settings

class RabbitMQQueue:
    _instance = None

    def __init__(self):
        self.config = settings.rabbitmq_config
        credentials = pika.PlainCredentials(**self.config["credentials"])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config["host"], credentials=credentials)
        )
        self.channels: dict[str, BlockingChannel] = {}

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = RabbitMQQueue()
        return cls._instance
    
    def create_channel(self, client_name: str):
        # cấu hình client và id tương ứng
        clients = self.config["client_ids"]
        if not self.channels.get(client_name):
            new_channel = self.connection.channel(channel_number=clients.get(client_name))
            self.channels[client_name] = new_channel

    def get_channel(self, client_name: str) -> BlockingChannel:
        return self.channels.get(client_name)
    
    def init_direct_exchange_and_queue(self, client_name: str):
        channel = self.get_channel(client_name=client_name)
        channel.exchange_declare(exchange=f'{client_name}_test_exchange', exchange_type='direct')
        channel.queue_declare(queue=f'{client_name}_test_queue')
        channel.queue_bind(queue=f'{client_name}_test_queue', exchange=f'{client_name}_test_exchange', routing_key=f'{client_name}_test_key')

        channel.exchange_declare(exchange=f'{client_name}_test_error_exchange', exchange_type='direct')
        channel.queue_declare(queue=f'{client_name}_test_error_queue')
        channel.queue_bind(queue=f'{client_name}_test_error_queue', exchange=f'{client_name}_test_error_exchange', routing_key=f'{client_name}_test_error_key')

    def publish_result(self, client_name: str, body):
        channel = self.get_channel(client_name=client_name)
        channel.basic_publish(exchange=f'{client_name}_test_exchange', routing_key=f'{client_name}_test_key', body=body)

    def emit_error(self, client_name: str, err):
        channel = self.get_channel(client_name=client_name)
        channel.basic_publish(exchange=f'{client_name}_test_error_exchange', routing_key=f'{client_name}_test_error_key', body=err)