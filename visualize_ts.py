import streamlit as st
import redis
import pandas as pd
import altair as alt
import json

# Function to fetch data from Redis TimeSeries
def fetch_timeseries_data(redis_host, redis_port, timeseries_keys):
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    # Dictionary to store data for each key
    data_dict = {}
    
    for key in timeseries_keys:
        try:
            data = r.ts().range(key,"-", "+")
            data_dict[key] = data
        except redis.exceptions.RedisError as e:
            st.error(f"Error fetching data for key {key}: {e}")
        
    
    return data_dict

# Streamlit app
def main():
    st.title("Redis TimeSeries Visualization")

    # Set your Redis instance details
    redis_host = "localhost"
    redis_port = 6335
    timeseries_keys = ["TS801", "TS091", "H098"]

    # Fetch data from Redis TimeSeries
    timeseries_data_dict = fetch_timeseries_data(redis_host, redis_port, timeseries_keys)

    # Check if there is data available
    if timeseries_data_dict:
        for key, data in timeseries_data_dict.items():
            # Convert data to DataFrame
            df = pd.DataFrame(data, columns=["timestamp", "value"])

            # Convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

            # Display the DataFrame for each key
            st.write(f"Time Series Data for {key}:")
            st.write(df)

            # Create an Altair chart for each key
            chart = alt.Chart(df).mark_line().encode(
                x="timestamp:T",
                y="value:Q",
                tooltip=["timestamp:T", "value:Q"]
            ).properties(
                width=600,
                height=300
            )

            # Display the chart for each key
            st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No data available in the Redis TimeSeries.")

if __name__ == "__main__":
    main()
