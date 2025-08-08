import pika
from pika.adapters.blocking_connection import BlockingChannel
from app.config import settings
from app.config import info_logger, error_logger
from app.exceptions.msgqueue_exception import MsgQueueException

class RabbitMQQueue:
    _instance = None

    def __init__(self, client_name: str):
        try:
            self.client_name = client_name
            # init connection
            info_logger.info(f"init connection to {client_name}")
            self.config = settings.rabbitmq_config
            credentials = pika.PlainCredentials(**self.config["credentials"])
            self.conn_params = pika.ConnectionParameters(host=self.config["host"], credentials=credentials, heartbeat=60)
            self.connection = pika.BlockingConnection(self.conn_params)
            # init channel
            info_logger.info(f"init channel for {client_name}")
            # cấu hình client và id tương ứng
            clients = self.config["client_ids"]
            self.channel = self.connection.channel(channel_number=clients.get(client_name))
            # init direct exchange and queue
            info_logger.info(f"init exchange and queue for {client_name}")
            self.channel.exchange_declare(exchange=f'{client_name}_exchange', exchange_type='direct')
            self.channel.queue_declare(queue=f'{client_name}_queue')
            self.channel.queue_bind(queue=f'{client_name}_queue', exchange=f'{client_name}_exchange', routing_key=f'{client_name}_key')

            self.channel.exchange_declare(exchange=f'{client_name}_error_exchange', exchange_type='direct')
            self.channel.queue_declare(queue=f'{client_name}_error_queue')
            self.channel.queue_bind(queue=f'{client_name}_error_queue', exchange=f'{client_name}_error_exchange', routing_key=f'{client_name}_error_key')
        except Exception as e:
            raise MsgQueueException(f"Failed to init msg queue: {e}")

    def close_connection(self):
        try:
            info_logger.info(f"closing connection to {self.client_name}")
            self.connection.close()
        except Exception as e:
            raise MsgQueueException(f"Error when closing connection: {e}")

    def publish_result(self, client_name: str, body):
        try:
            self.channel.basic_publish(exchange=f'{client_name}_exchange', routing_key=f'{client_name}_key', body=body)
        except Exception as e:
            raise MsgQueueException(f"Failed to publish result: {e}")

    def emit_error(self, client_name: str, err):
        try:
            self.channel.basic_publish(exchange=f'{client_name}_error_exchange', routing_key=f'{client_name}_error_key', body=err)
        except Exception as e:
            raise MsgQueueException(f"Failed to emit error: {e}")