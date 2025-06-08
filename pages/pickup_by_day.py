import streamlit as st
import pandas as pd
import altair as alt

st.title("Uber Pickups in NYC - By Day")

DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data['date_only'] = data[DATE_COLUMN].dt.date
    return data

data = load_data(10000)

pickup_counts_by_date = data['date_only'].value_counts().sort_index()
chart_data = pickup_counts_by_date.reset_index()
chart_data.columns = ['date', 'count']

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pickups per Day (Altair Chart)")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x='date:T',
        y='count:Q',
        tooltip=['date:T', 'count:Q']
    ).properties(width=330, height=400)
    st.altair_chart(chart, use_container_width=False)

with col2:
    st.subheader("Map of pickups for selected date")
    selected_date = st.selectbox('Pick a date to visualize:', sorted(data['date_only'].unique()))
    filtered_data = data[data['date_only'] == selected_date]
    st.write(f'Number of pickups on {selected_date}: {len(filtered_data)}')
    st.map(filtered_data)
