~ DATA STREAMING IOT ~
Real-time data originates from IoT temperature and air humidity sensors within a room.
In this scenario, my task involves processing the data for monitoring and visualization.

Installation:

Clone this repository.
#Usage:
- Ensure the IoT device and Flask server configurations are connected.
- Run 'make kafka-create'
- Run 'make docker-build-flask'
- Run 'make postgres-create'
- Run 'make postgres-create-table'
- Run 'make grafana'
- Open Docker Desktop and access the Flask Docker image to check logs for data transmission status.
- Access the Kafka link to verify Kafka topics for data reception.
- Open the PostgreSQL database management tool, configure the database in consumer.py.
- Access the Grafana link, log in, and configure PostgreSQL database with Grafana.

#Architecture of Data:
- IoT devices send real-time data to the Flask server.
- Data is read by a Kafka producer and sent to the broker.
- Kafka consumer reads and receives data from the broker.
- Data is then stored in PostgreSQL.
- PostgreSQL data is configured with Grafana for monitoring and visualization.

#Supporting Tools Used:
- Visual Studio Code
- Docker Desktop
- Flask
- Kafka
- DBeaver
- PostgreSQL
- Grafana
  
#License

Contact

Muhammad Rewa Akbari - muhammadrewaakbari@gmail.com
