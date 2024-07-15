from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
import os

from dotenv import load_dotenv
load_dotenv()

kafka_host = os.getenv('KAFKA_HOST')
kafka_topic = os.getenv('KAFKA_TOPIC_NAME')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
postgres_container = os.getenv('POSTGRES_CONTAINER')

# Membuat SparkSession
spark = SparkSession.builder \
    .appName("Kafka to Spark to Postgres") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2") \
    .getOrCreate()

# Membaca data dari Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", os.getenv('KAFKA_HOST') + ':9092') \
    .option("subscribe", os.getenv('KAFKA_TOPIC_NAME')) \
    .load()

# Mengubah data menjadi string
df = df.selectExpr("CAST(value AS STRING)")

# Menyimpan data ke PostgreSQL
df.write \
    .format("jdbc") \
    .option("url", f"jdbc:postgresql://{os.getenv('POSTGRES_CONTAINER_NAME')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}") \
    .option("dbtable", "sensor_data") \
    .option("user", os.getenv('POSTGRES_USER')) \
    .option("password", os.getenv('POSTGRES_PASSWORD')) \
    .option("driver", "org.postgresql.Driver") \
    .save()