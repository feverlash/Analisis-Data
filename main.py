import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

st.set_page_config(
    page_title=":green[Analisis] Data Penyewaan Sepeda Harian :bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded")

# Membaca data yang sudah dibersihkan
url = 'https://raw.githubusercontent.com/feverlash/Analisis-Data/1b784470df03a8e53000ea6a7393bf2fbafc7919/Bike-sharing-dataset/cleaned_day.csv'
data = pd.read_csv(url)

# Function 1
def visualize_season_counts(data):
    data['season'] = data['season'].map({
        'Spring': 'Spring',
        'Summer': 'Summer',
        'Fall': 'Fall',
        'Winter': 'Winter'
    })

    season_counts = data.groupby('season')['total_rental'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(season_counts['season'], season_counts['total_rental'], color=['#4CAF50', '#FFC107', '#FF5722', '#2196F3'])
    plt.title('Total Jumlah Penyewaan Sepeda Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Total Penyewaan Sepeda')
    st.pyplot(plt)

# Function 2
def visualize_year_tren(data):
    data['month'] = pd.Categorical(data['month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
    
    monthly_counts = data.groupby(by=["month", "year"]).agg({"total_rental": "sum"}).reset_index()

    plt.figure(figsize=(10, 6))
    for year in monthly_counts['year'].unique():
        plt.plot(monthly_counts[monthly_counts['year'] == year]['month'], 
                 monthly_counts[monthly_counts['year'] == year]['total_rental'], 
                 marker='o', label=f'{"2011" if year == 0 else "2012"}')
    plt.title("Jumlah sepeda yang disewakan berdasarkan Bulan dan Tahun")
    plt.xlabel('Bulan')
    plt.ylabel('Total Penyewaan Sepeda')
    plt.legend(title='Tahun')
    st.pyplot(plt)

# Function 3
def visualize_weather_counts(data):
    bike_rentals_per_weather = data.groupby('weather_cond')['total_rental'].sum().reset_index()
    bike_rentals_per_weather.columns = ['Weather Situation', 'Total Rentals']

    plt.figure(figsize=(10, 6))
    plt.bar(bike_rentals_per_weather['Weather Situation'], bike_rentals_per_weather['Total Rentals'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.xticks(ticks=[0, 1, 2], labels=['1', '2', '3'])
    st.pyplot(plt)

# Function 4
def visualize_workingday_counts(data):
    workingday_counts = data.groupby('workingday')['total_rental'].sum().reset_index()
    workingday_counts.columns = ['Working Day', 'Counts']
    workingday_counts['Working Day'] = workingday_counts['Working Day'].map({0: 'Hari Libur', 1: 'Hari Kerja'})
    
    plt.figure(figsize=(10, 6))
    plt.bar(workingday_counts['Working Day'], workingday_counts['Counts'], color=['#e377c2', '#17becf'])
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur')
    plt.xlabel('Hari Kerja / Hari Libur')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(plt)

# Function 5
def visualize_timeseries(data):
    data['dateday'] = pd.to_datetime(data['dateday'])
    data.set_index('dateday', inplace=True)

    y = data['total_rental']
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')

    plt.figure(figsize=(12, 8))
    if show_original:
        plt.subplot(411)
        plt.plot(y, label='Original', color='blue')
        plt.title('Original')
        plt.legend()

    if show_trend:
        plt.subplot(412)
        plt.plot(decomposition.trend, label='Trend', color='orange')
        plt.title('Trend')
        plt.legend()

    if show_seasonal:
        plt.subplot(413)
        plt.plot(decomposition.seasonal, label='Seasonal', color='green')
        plt.title('Seasonal')
        plt.legend()

    if show_residual:
        plt.subplot(414)
        plt.plot(decomposition.resid, label='Residual', color='red')
        plt.title('Residual')
        plt.legend()

    plt.tight_layout()
    st.pyplot(plt)

# Sidebar with options
st.sidebar.title(':computer: :thinking_face: :question:')
st.sidebar.title('**Pilihan Pertanyaan Bisnis**')
st.sidebar.markdown("**Pada proyek ini saya menganalisis dataset sewa sepeda harian untuk menjawab beberapa pertanyaan di bawah ini**")
question = st.sidebar.selectbox('Pilih Pertanyaan:', ['Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3', 'Pertanyaan 4', 'Analisis Lanjutan'])

# Display the selected question and visualization based on selected question
st.title(':green[Analisis] Data Penyewaan Sepeda Harian :bar_chart:')

if question == 'Pertanyaan 1':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda pada setiap musim?")
    visualize_season_counts(data)
elif question == 'Pertanyaan 2':
    st.write("### Bagaimana tren jumlah total penyewaan sepeda dari bulan ke bulan selama periode 2011 dan 2012?")
    visualize_year_tren(data)
elif question == 'Pertanyaan 3':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara setiap cuaca?")
    visualize_weather_counts(data)
elif question == 'Pertanyaan 4':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara hari kerja dan hari libur?")
    visualize_workingday_counts(data)
elif question == 'Analisis Lanjutan':
    st.write("### Analisis lanjutan time series analysis")
    visualize_timeseries(data)
