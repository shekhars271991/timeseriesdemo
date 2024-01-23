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
consumer_name = "temperature_consumer"

# Connect to Redis with password
r = redis.Redis(host=redis_host, port=redis_port,decode_responses=True)

# Create the consumer group if it doesn't exist
try:
    r.xgroup_create(stream_name, consumer_group, id="0", mkstream=True)
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP Consumer Group name already exists" not in str(e):
        raise

def visualize_stream_data():
    st.title("Temperature Sensor Data Visualization")
    df = pd.DataFrame(columns=["TS091", "TS801", "H098"])

    # Create a streamlit chart
    chart = st.line_chart()

    while True:
        # Read the latest data from the Redis stream using XREADGROUP
        data = r.xreadgroup(consumer_group, consumer_name, {stream_name: ">"}, count=1, block=1000)

        if data:
            # Extract the relevant information from the Redis stream data
            _, messages = data[0][1][0]
            json_data = json.loads(messages['data'])
            
            # Append the new data to the DataFrame
            # df = df.concat(json_data, ignore_index=True)

            df = pd.concat([df, pd.DataFrame([json_data])], ignore_index=True)

            # Update the streamlit chart with the new data
            chart.line_chart(df, use_container_width=True)

            # Display the raw data
            st.write("Raw Data:", json_data)

            # # Update the streamlit chart with the new data
            # chart.line_chart([json_data["TS091"], json_data["TS801"], json_data["H098"]])
            
            # # Display the raw data
            # st.write("Raw Data:", json_data)

# Run the Streamlit app
if __name__ == "__main__":
    visualize_stream_data()
