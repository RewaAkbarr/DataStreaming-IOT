from flask import Flask, request
from kafka import KafkaProducer
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
import os
import json

dotenv_path = Path('/app/.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

kafka_host = "dataeng-kafka"
kafka_topic = "test-topic"
kafka_port = 9092

# Menambahkan value_serializer untuk otomatis mengonversi data ke bytes
producer = KafkaProducer(
    bootstrap_servers=[f'{kafka_host}:{kafka_port}'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

@app.route('/post-data', methods=['POST'])
def post_data():
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    local_now = datetime.now().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=7)))
    timestamp = local_now.strftime('%Y-%m-%d %H:%M:%S')
    data = {'temperature': temperature, 'humidity': humidity, 'timestamp': timestamp}
    # Mengirim data ke Kafka
    producer.send(kafka_topic, value=data)
    producer.flush()
    print(f'Received data: {data}')
    return 'Data received and sent to Kafka', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=51678, debug=True)