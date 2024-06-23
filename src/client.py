from datetime import datetime

import streamlit as st
import requests
import pandas as pd
import altair as alt
from dateutil.parser import parse


def fetch_usage_data():
    response = requests.get("http://localhost:8000/usage")  # TODO fetch port from env
    if response.status_code == 200:
        return response.json()["usage"]
    else:
        st.error("Failed to fetch usage data")
        return None


# TODO move to utils
def format_timestamp(timestamp: str) -> str:
    date_time = parse(timestamp)
    formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M")
    return formatted_date_time


def date_obj(timestamp: str) -> datetime:
    return parse(timestamp)


def main():
    st.title("Credit Usage Dashboard")
    usage_data = fetch_usage_data()
    if usage_data:
        # Convert usage data to a DataFrame
        usage_df = pd.DataFrame(usage_data)
        usage_df['formatted_timestamp'] = usage_df['timestamp'].apply(format_timestamp)
        # Create a bar chart of daily credit usage
        usage_df['date'] = usage_df['timestamp'].apply(date_obj).apply(lambda x: x.date())
        chart_data = usage_df.groupby('date')['credits'].sum().reset_index()
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='date:T',
            y='credits:Q',
            tooltip=['date', 'credits']
        ).properties(
            width=800,
            height=400,
            title="Daily Credit Usage"
        )
        st.altair_chart(chart)

        # Create sortable data table
        st.subheader("Usage Details")

        # Sorting options
        sort_column = st.selectbox("Sort by", usage_df.columns)
        sort_order = st.radio("Sort order", ["Ascending", "Descending"])

        # Sort data
        if sort_order == "Ascending":
            usage_df = usage_df.sort_values(by=sort_column, ascending=True)
        else:
            usage_df = usage_df.sort_values(by=sort_column, ascending=False)

        # Display data table with headers Message ID, Timestamp, Report Name, Credits
        st.dataframe(usage_df[["id", "timestamp", "report_name", "credits"]].style.format({
            "credits": "{:.2f}"
        }))


if __name__ == "__main__":
    main()
