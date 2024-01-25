import redis
import json


def insert_into_timeseries(r, timeseries_key, stream, msg_id, msg_body):
    # Insert the message into a Redis TimeSeries
    
    dev_group = msg_body["device_group_id"]
    for key, value in msg_body.items():
        if(key == "device_group_id"):
            continue
        r.ts().add(key, "*",  value, labels={"devie_group": dev_group})

    # r.ts().add(timeseries_key, "*", msg_body["hello"], labels={"stream": dev_group, "msg_id": msg_id})

def read_redis_stream(redis_host, redis_port, stream_name, consumer_group, consumer_name, timeseries_key):
    # Connect to Redis with password
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    # Create a consumer group (if not exists)
    print("Connected")
    try:
        r.xgroup_create(stream_name, consumer_group, id='$', mkstream=True)
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP Consumer Group name already exists" not in str(e):
            raise

    # Read messages from the stream
    while True:
        # Read messages from the stream
        try:
            messages = r.xreadgroup(consumer_group, consumer_name, {stream_name: '>'}, count=1, block=1)
            for message in messages:
                stream, data = message
                for msg_id, msg_body in data:
                    print(f"Received message from {stream}: {msg_body}") 
                    # Call the function to insert into the Redis TimeSeries
                    insert_into_timeseries(r, timeseries_key, stream, msg_id, json.loads(msg_body["data"]))
        except redis.exceptions.ResponseError as e: 
            print("Error in reading message", e)

if __name__ == "__main__":
    # Set your Redis instance details
    redis_host = "localhost"
    timeseries_key = "temprature_data"
    redis_port = 6335
    stream_name = "temperature_sensor_data"
    consumer_group = "analytics"
    consumer_name = "analytics_node1"
    timeseries_key = "temperature_timeseries"
    print("Starting")
    read_redis_stream(redis_host, redis_port, stream_name, consumer_group, consumer_name, timeseries_key)
