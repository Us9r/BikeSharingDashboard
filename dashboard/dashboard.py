import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
bike_sharing_day = pd.read_csv('https://raw.githubusercontent.com/Us9r/submission-dicoding/main/data/day.csv')
bike_sharing_hour = pd.read_csv('https://raw.githubusercontent.com/Us9r/submission-dicoding/main/data/hour.csv')

# Convert 'dteday' to datetime format
bike_sharing_day['dteday'] = pd.to_datetime(bike_sharing_day['dteday'])

# Create a new column that combines year and month
bike_sharing_day['yr_month'] = bike_sharing_day.apply(lambda row: f"{row['yr']}-{row['mnth']}", axis=1)

# Define morning, afternoon, evening, and night times
waktu_pagi = bike_sharing_hour[(bike_sharing_hour['hr'] >= 6) & (bike_sharing_hour['hr'] < 12)]
waktu_siang = bike_sharing_hour[(bike_sharing_hour['hr'] >= 12) & (bike_sharing_hour['hr'] < 18)]
waktu_sore = bike_sharing_hour[(bike_sharing_hour['hr'] >= 18) & (bike_sharing_hour['hr'] < 22)]
waktu_malam = bike_sharing_hour[(bike_sharing_hour['hr'] >= 22) | (bike_sharing_hour['hr'] < 0)]
waktu_tengah_malam = bike_sharing_hour[(bike_sharing_hour['hr'] >= 0) & (bike_sharing_hour['hr'] < 6)]

# Create a title for the dashboard
st.title("Bike Sharing Dashboard")

# Sidebar for filtering
st.sidebar.header("Filter Data")

# Date filter
start_date = st.sidebar.date_input("Pilih tanggal mulai", value=bike_sharing_day['dteday'].min())
end_date = st.sidebar.date_input("Pilih tanggal akhir", value=bike_sharing_day['dteday'].max())

# Filter data based on selected date range
filtered_data = bike_sharing_day[(bike_sharing_day['dteday'] >= pd.to_datetime(start_date)) & 
                                  (bike_sharing_day['dteday'] <= pd.to_datetime(end_date))]

# Create a tab for the dashboard
tab1, tab2, tab3 = st.tabs(["Penggunaan Sepeda Sepanjang Tahun", "Penggunaan Sepeda Berdasarkan Jam", "Penggunaan Sepeda Berdasarkan Waktu Pagi, Siang dan Sore"])

# Tab 1: Penggunaan Sepeda Sepanjang Tahun
with tab1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='yr_month', y='cnt', data=filtered_data, ax=ax)
    ax.set_title('Penggunaan Sepeda Sepanjang Tahun 2011 hingga 2012')
    ax.set_xlabel('Tahun-Bulan')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

# Tab 2: Penggunaan Sepeda Berdasarkan Jam
with tab2:
    hourly_data = bike_sharing_hour.groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='hr', y='cnt', data=hourly_data, ax=ax)
    ax.set_title('Penggunaan Sepeda Berdasarkan Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

# Tab 3: Penggunaan Sepeda Berdasarkan Waktu Pagi, Siang dan Sore
with tab3:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='hr', y='cnt', data=waktu_tengah_malam, label='Tengah Malam', ax=ax)
    sns.lineplot(x='hr', y='cnt', data=waktu_pagi, label='Pagi', ax=ax)
    sns.lineplot(x='hr', y='cnt', data=waktu_siang, label='Siang', ax=ax)
    sns.lineplot(x='hr', y='cnt', data=waktu_sore, label='Sore', ax=ax)
    sns.lineplot(x='hr', y='cnt', data=waktu_malam, label='Malam', ax=ax)
    ax.set_title('Penggunaan Sepeda Berdasarkan Waktu Pagi, Siang dan Sore')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    ax.legend()
    st.pyplot(fig)