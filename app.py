import streamlit as st
import redis
import pandas as pd
from datetime import datetime
import time

# Function to read data from the Redis time series
def read_redis_timeseries(redis_host, redis_port, password, timeseries_key):
    r = redis.Redis(host=redis_host, port=redis_port, password=password, decode_responses=True)

    # Read data from the time series
    data = r.ts().range(timeseries_key, "-", "+")

    data_list = []
    for timestamp, value in data:
        timestamp = datetime.utcfromtimestamp(int(timestamp) / 1000.0)
        data_list.append({"Timestamp": timestamp, "Value": float(value)})

    return pd.DataFrame(data_list)

# Streamlit app
@st.cache(allow_output_mutation=True)
def get_chart_data(redis_host, redis_port, password, timeseries_key):
    df = read_redis_timeseries(redis_host, redis_port, password, timeseries_key)
    return df

def main():
    # Set your Redis instance details
    redis_host = "localhost"
    redis_port = 15400
    password = "ZUr6Cu5B"  # Replace with your Redis password if applicable
    timeseries_key = "TS091"  # Replace with the actual key of your time series

    # Streamlit UI
    st.title("Time Series Data Visualization")
    st.write(f"## {timeseries_key} Time Series")

    # Create an empty container for the chart
    chart_container = st.empty()

    while True:
        # Get data for the chart
        df = get_chart_data(redis_host, redis_port, password, timeseries_key)

        # Plot the time series data
        chart_container.line_chart(df.set_index("Timestamp"))

        # Wait for 10 seconds before refreshing
        time.sleep(10)

if __name__ == "__main__":
    main()
