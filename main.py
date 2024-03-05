import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Analisis Data Penyewaan Sepeda Harian",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Function to set font properties for matplotlib
def set_matplotlib_font():
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.weight'] = 'medium'

# Load the data
url = 'https://raw.githubusercontent.com/feverlash/Analisis-Data/d4f2afc8974492315841fd0f7120133dd50bfb8c/Bike-sharing-dataset/cleaned_day.csv'
data = pd.read_csv(url)

# Sidebar with options
st.sidebar.title('Pilihan Pertanyaan')
question = st.sidebar.selectbox('Pilih Pertanyaan:', ['Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3'])

# Function to visualize correlation between weather condition and daily bike rentals
def visualize_correlation(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    corr_matrix = data[['weathersit', 'cnt']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='flare', fmt=".2f", ax=ax)
    ax.set_title('Correlation between Weather Condition and Daily Bike Rentals', fontweight='medium')
    ax.set_xlabel('Variable')
    ax.set_ylabel('Variable')
    st.pyplot(fig)

# Function to visualize bike rentals based on weather situation
def visualize_weather_counts(data):
    weather_counts = data['weathersit'].value_counts().reset_index()
    weather_counts.columns = ['Weather Situation', 'Counts']

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Weather Situation', y='Counts', data=weather_counts, palette='flare', ax=ax)
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca', fontweight='medium')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)

# Function to visualize bike rentals based on working day
def visualize_workingday_counts(data):
    workingday_counts = data['workingday'].value_counts().reset_index()
    workingday_counts.columns = ['Working Day', 'Counts']

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='Working Day', y='Counts', data=workingday_counts, palette='flare', ax=ax)
    ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Hari', fontweight='medium')
    ax.set_xlabel('Hari Kerja / Hari Libur ')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.set_xticks(ticks=[0, 1], labels=['Hari Libur', 'Hari Kerja'])
    st.pyplot(fig)

# Set font properties
set_matplotlib_font()

# Display the selected question and visualization based on selected question
st.title('Analisis Data Penyewaan Sepeda Harian')

if question == 'Pertanyaan 1':
    st.write("### Bagaimana korelasi antara kondisi cuaca dengan jumlah penyewaan sepeda harian ?")
    visualize_correlation(data)
elif question == 'Pertanyaan 2':
    st.write("### Apakah ada pola yang dapat diidentifikasi, seperti penurunan dalam penyewaan sepeda saat terjadi hujan atau kondisi cuaca buruk lainnya?")
    visualize_weather_counts(data)
elif question == 'Pertanyaan 3':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara hari kerja dan akhir pekan?")
    visualize_workingday_counts(data)