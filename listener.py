import logging
import subprocess
from google.cloud import pubsub_v1
import os

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Config
PROJECT_ID = 'gmail-classifier-454221'  # Replace with your project ID
SUBSCRIPTION_NAME = 'gmail-notifications-sub'  # Replace with your subscription name

def callback(message):
    logging.info("New message received via Pub/Sub")
    try:
        logging.info("Triggering main.py to classify emails...")
        # Run main.py as a subprocess
        subprocess.run(["python3", "main.py"], check=True) # check=True will raise an error if main.py fails.

        message.ack()

    except subprocess.CalledProcessError as e:
        logging.error(f"Error running main.py: {e}")
        message.ack() # still ack the message to prevent redelivery
    except Exception as e:
        logging.error(f"Error processing Pub/Sub message: {e}")
        message.ack()

if __name__ == '__main__':
    print("Starting Gmail Pub/Sub listener...")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    print(f"Listening to Pub/Sub subscription: {SUBSCRIPTION_NAME}")
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("Stopped.")
