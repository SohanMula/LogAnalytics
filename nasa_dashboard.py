import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("🚀 NASA Logs Analysis Dashboard")

# Base local directory for Parquet files
local_base = "/home/hdoop/bdsel/parquet_downloads"

# Helper to load parquet
def load_parquet(folder):
    path = f"{local_base}/{folder}"
    return pd.read_parquet(path)

# Top Hosts
st.header("Top 10 Hosts by Requests")
df_hosts = load_parquet("top_hosts")
df_hosts = df_hosts.sort_values(by="total_requests", ascending=True)
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(df_hosts['host'], df_hosts['total_requests'], color='skyblue')
ax1.set_xlabel("Total Requests")
st.pyplot(fig1)

# Status Codes
st.header("Status Codes Distribution")
df_status = load_parquet("status_counts")
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(df_status['status'], df_status['count'], color='orange')
ax2.set_xlabel("Status Code")
ax2.set_ylabel("Count")
st.pyplot(fig2)

# Requests per Day
st.header("Requests per Day")
df_days = load_parquet("requests_per_day")
df_days = df_days.sort_values(by="day")
fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(df_days['day'], df_days['requests'], marker='o')
ax3.set_xticklabels(df_days['day'], rotation=90)
st.pyplot(fig3)

# Requests per Hour
st.header("Requests per Hour")
df_hours = load_parquet("requests_per_hour")
fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.bar(df_hours['hour'], df_hours['requests'], color='green')
st.pyplot(fig4)

# Top Requested URLs
st.header("Top Requested URLs")
df_urls = load_parquet("top_requests")
st.dataframe(df_urls)

# Hosts with most 404 errors
st.header("Top Hosts with 404 Errors")
df_404 = load_parquet("hosts_404")
st.dataframe(df_404)

# Total Bytes
st.header("Total Bytes Transferred")
df_bytes = load_parquet("total_bytes")
total_bytes_value = df_bytes['total_bytes'].iloc[0]
st.metric("Total Bytes", f"{total_bytes_value:,}")

# Error Categories
st.header("Error Categories")
df_errors = load_parquet("error_categories")
fig5, ax5 = plt.subplots()
ax5.pie(df_errors['count'], labels=df_errors['category'], autopct='%1.1f%%', startangle=140)
st.pyplot(fig5)

# Unique Hosts
st.header("Unique Hosts Count")
df_unique = load_parquet("unique_hosts")
unique_count = df_unique['unique_host_count'].iloc[0]
st.metric("Unique Hosts", unique_count)

# Most Popular Files
st.header("Most Popular Files")
df_files = load_parquet("popular_files")
st.dataframe(df_files)

st.success("✅ Dashboard loaded successfully!")
