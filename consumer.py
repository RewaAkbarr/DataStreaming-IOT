from kafka import KafkaConsumer
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from pathlib import Path
import logging
import json

dotenv_path = Path('/app/.env')
load_dotenv(dotenv_path=dotenv_path)

kafka_host = "dataeng-kafka"
kafka_port = 9092
kafka_topic = "test-topic"
postgres_host = "host.docker.internal"
postgres_password = "password"
postgres_db = "postgres_db"
postgres_user = "user"

# Set up logging
logging.basicConfig(level=logging.INFO)

try:
    # Create a Kafka consumer
    consumer = KafkaConsumer('test-topic',
    bootstrap_servers=[f'{kafka_host}:{kafka_port}'],
    group_id='dibimbing-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
    logging.info("Kafka consumer created")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=postgres_host,
        database=postgres_db,
        user=postgres_user,
        password=postgres_password,
        port=5432
    )
    logging.info("Connected to PostgreSQL")

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    for message in consumer:
        try:
            # message.value is already a dict because of the value_deserializer
            data = message.value
            logging.info(f"Received data: {data}")

            # Check if data has necessary keys
            if 'temperature' in data and 'humidity' in data and 'timestamp' in data:
                # Insert data into PostgreSQL
                cur.execute("INSERT INTO public.sensor_data (temperature, humidity, timestamp) VALUES (%s, %s, %s)",
                            (data['temperature'], data['humidity'], data['timestamp']))
                conn.commit()
                logging.info("Data inserted into PostgreSQL")
            else:
                logging.error("Data does not have necessary keys")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

    # Close connections
    cur.close()
    conn.close()

except Exception as e:
    logging.error(f"An error occurred: {e}")