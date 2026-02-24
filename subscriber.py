from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.futures import StreamingPullFuture
from google.cloud.pubsub_v1.subscriber.message import Message

from config import Settings

settings = Settings()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(settings.PROJECT_ID, settings.SUBSCRIPTION_ID)


def callback(message: Message) -> None:
    print(f"Received message: {message.data.decode()}")
    message.ack()


def start_listener() -> StreamingPullFuture:
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback,
    )
    print("Listening for messages...")
    return streaming_pull_future
