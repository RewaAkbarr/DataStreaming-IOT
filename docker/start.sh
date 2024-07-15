#!/bin/bash
python /app/consumer.py &
python /app/producer.py &
wait