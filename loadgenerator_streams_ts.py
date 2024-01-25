import redis
import json
import random
import time

def generate_random_data(prev_values={}):
    data = {
        "device_group_id": "D001",
    }

    # Generate random values with no more than 10% variance from the previous values
    for key in ["TS091", "TS801", "H098"]:
        prev_value = prev_values.get(key, random.uniform(1, 100))
        variance_limit = 0.15 * prev_value
        new_value = max(min(random.uniform(prev_value - variance_limit, prev_value + variance_limit), 100), 1)
        data[key] = new_value

        # Update previous values
        prev_values[key] = new_value

    return json.dumps(data)

def write_to_redis_stream(r, stream_name):
    prev_values = {}

    while True:
        # Generate random data
        random_data = generate_random_data(prev_values)

        # Write to Redis stream
        r.xadd(stream_name, {"data": random_data})

        print(f"Data written to {stream_name}: {random_data}")

        # Wait for one second
        time.sleep(0.01)

if __name__ == "__main__":
    # Set your Redis instance details
    redis_host = "localhost"
    redis_port = 6335
    password = "ZUr6Cu5B"  # Replace with your Redis password if applicable
    stream_name = "temperature_sensor_data"  # Replace with the desired stream name

    # Connect to Redis with password
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    # Run the script to continuously write random data to the Redis stream
    write_to_redis_stream(r, stream_name)
