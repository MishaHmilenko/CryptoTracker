import os

from kafka import KafkaAdminClient
from kafka.admin import NewTopic


class KafkaAdminClientService:

    def __init__(self) -> None:
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=f'{os.getenv("KAFKA_BROKER_HOST")}:{os.getenv("KAFKA_BROKER_PORT")}',
            client_id='admin-client'
        )

    def add_topic(self, topic_name: str) -> None:

        if topic_name not in self.admin_client.list_topics():
            new_topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
            self.admin_client.create_topics(new_topics=[new_topic], validate_only=False)
