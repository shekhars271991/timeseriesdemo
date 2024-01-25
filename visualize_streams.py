import streamlit as st
import redis
import json
import pandas as pd

# Set your Redis instance details
redis_host = "localhost"
redis_port = 6335
password = "ZUr6Cu5B"  # Replace with your Redis password if applicable
stream_name = "temperature_sensor_data"  # Replace with the desired stream name
consumer_group = "group1"
consumer_name = "cdot_temperature_sensor_data"

# Connect to Redis with password
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Create the consumer group if it doesn't exist
try:
    r.xgroup_create(stream_name, consumer_group, id="0", mkstream=True)
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP Consumer Group name already exists" not in str(e):
        raise

def visualize_stream_data():
    st.title("Temperature Sensor Data Visualization")

    while True:
        # Read the latest data from the Redis stream using XREADGROUP
        data = r.xreadgroup(consumer_group, consumer_name, {stream_name: ">"}, count=1, block=1000)

        if data:
            # Extract the relevant information from the Redis stream data
            _, messages = data[0][1][0]
            json_data = json.loads(messages['data'])
            
            # Create a new streamlit chart with the updated data
            chart = st.line_chart(pd.DataFrame([json_data]).T, use_container_width=True)

            # Display the raw data
            st.write("Raw Data:", json_data)

# Run the Streamlit app
if __name__ == "__main__":
    visualize_stream_data()
