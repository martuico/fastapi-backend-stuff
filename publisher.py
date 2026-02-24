from google.cloud import pubsub_v1

from config import Settings

settings = Settings()

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(settings.PROJECT_ID, settings.TOPIC_ID)


def publish_message(message: str) -> str:
    future = publisher.publish(topic_path, message.encode("utf-8"))
    return future.result()  # type: ignore
