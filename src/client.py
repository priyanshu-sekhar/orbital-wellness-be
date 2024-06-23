from datetime import datetime

import streamlit as st
import requests
import pandas as pd
import altair as alt
from dateutil.parser import parse


def fetch_usage_data():
    response = requests.get("http://localhost:8000/usage")
    if response.status_code == 200:
        return response.json()["usage"]
    else:
        st.error("Failed to fetch usage data")
        return None


def format_timestamp(timestamp: str) -> str:
    date_time = parse(timestamp)
    formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M")
    return formatted_date_time


def date_obj(timestamp: str) -> datetime:
    return parse(timestamp)


MESSAGE_ID_FIELD = "message_id"
TIMESTAMP_FIELD = "timestamp"
REPORT_NAME_FIELD = "report_name"
CREDITS_USED_FIELD = "credits_used"
DATE_FIELD = "date"


def main():
    st.title("Credit Usage Dashboard")
    usage_data = fetch_usage_data()
    if usage_data:
        # Convert usage data to a DataFrame
        usage_df = pd.DataFrame(usage_data)
        # Create a bar chart of daily credit usage
        usage_df[DATE_FIELD] = usage_df[TIMESTAMP_FIELD].apply(date_obj).apply(lambda x: x.date())
        chart_data = usage_df.groupby(DATE_FIELD)[CREDITS_USED_FIELD].sum().reset_index()
        chart = alt.Chart(chart_data).mark_bar().encode(
            x='date:T',
            y='credits_used:Q',
            tooltip=['date', CREDITS_USED_FIELD]
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

        table_fields = [MESSAGE_ID_FIELD, TIMESTAMP_FIELD, REPORT_NAME_FIELD, CREDITS_USED_FIELD]
        st.dataframe(usage_df[table_fields].style.format({
            CREDITS_USED_FIELD: "{:.2f}"
        }))


if __name__ == "__main__":
    main()
