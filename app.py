import pandas as pd
import streamlit as st
import plotly.express as px

# Load hotel data
df = pd.read_csv("hotels.csv")

# Set page config
st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")
st.title("🏨 Hotel Booking Dashboard")

# --- Sidebar Filters ---
st.sidebar.title("📂 Dashboard Filters")
st.sidebar.image('filter.png')
st.sidebar.title("📊 Bar Chart Filter")

# Bar Chart filter (categorical)
bar_filter = st.sidebar.selectbox(
    "Group Total Revenue By:",
    options=['hotel', 'customer_type', 'country', 'market_segment']
)

st.sidebar.title("📈 Scatter Plot Filter")

# Scatter Plot filter (numeric columns)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
x_axis = st.sidebar.selectbox("X-Axis (Numeric):", options=numeric_cols)

# --- Data Preview ---
st.write("Dataset Shape:", df.shape)
st.dataframe(df.head())

# --- Pie Chart: Distribution by Hotel Type ---
st.subheader("Pie Chart: Booking Share by Hotel Type")
hotel_counts = df['hotel'].value_counts().reset_index()
hotel_counts.columns = ['hotel', 'count']
fig_pie = px.pie(hotel_counts, names='hotel', values='count', title="Hotel Booking Distribution")
st.plotly_chart(fig_pie, use_container_width=True)

# --- Bar Chart: Total Revenue by Selected Column ---
st.subheader(f"Bar Chart: Total Revenue by {bar_filter}")
if 'adr' in df.columns and 'stays_in_weekend_nights' in df.columns and 'stays_in_week_nights' in df.columns:
    df['Revenue'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    grouped = df.groupby(bar_filter)['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    fig_bar = px.bar(grouped, x=bar_filter, y='Revenue', text='Revenue',
                     title=f"Total Revenue by {bar_filter}")
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(yaxis=dict(visible=False))
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Revenue columns not found in the dataset.")

# --- Scatter Plot: Selected X vs Revenue ---
st.subheader(f"Scatter Plot: {x_axis} vs Revenue")
fig_scatter = px.scatter(
    df,
    x=x_axis,
    y='Revenue',
    color='hotel',
    title=f"{x_axis} vs Revenue by Hotel Type"
)
fig_scatter.update_layout(
    xaxis_title=x_axis,
    yaxis_title="Revenue"
)
st.plotly_chart(fig_scatter, use_container_width=True)
