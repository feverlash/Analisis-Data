import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title=":green[Analisis] Data Penyewaan Sepeda Harian :bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded")

# Load the data
url = 'https://raw.githubusercontent.com/feverlash/Analisis-Data/d4f2afc8974492315841fd0f7120133dd50bfb8c/Bike-sharing-dataset/cleaned_day.csv'
data = pd.read_csv(url)

# Sidebar with options
st.sidebar.title(':computer: :thinking_face: :question:')
st.sidebar.title('**Pilihan Pertanyaan Bisnis**')
st.sidebar.markdown("**Pada proyek ini saya menganalisis dataset sewa sepeda harian untuk menjawab beberapa pertanyaan di bawah ini**")
question = st.sidebar.selectbox('Pilih Pertanyaan:', ['Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3', 'Pertanyaan 4'])

# Function to visualize correlation between weather condition and daily bike rentals
def visualize_correlation_1(data):
    corr_matrix = data[['weathersit', 'cnt']].corr()
    fig = px.imshow(corr_matrix.values, 
                    labels=dict(color="Correlation"),
                    x=['Kondisi Cuaca', 'Jumlah Sewa Harian'], 
                    y=['Kondisi Cuaca', 'Jumlah Sewa Harian'], 
                    color_continuous_scale='viridis')
    
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            fig.add_annotation(x=i, y=j, 
                               text=f'{corr_matrix.iloc[i, j]:.2f}', 
                               showarrow=False, 
                               font=dict(color='black' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'white'))
    
    fig.update_layout(title='Korelasi antara Jumlah Penyewaan Sepeda Harian dengan Kondisi Cuaca', font=dict(size=11))
    st.plotly_chart(fig)

# Function to visualize correlation between day and daily bike rentals
def visualize_correlation_2(data):
    corr_matrix = data[['workingday', 'holiday', 'cnt']].corr()
    fig = px.imshow(corr_matrix.values, 
                    labels=dict(color="Correlation"),
                    x=['Hari Kerja', 'Hari Libur', 'Jumlah Sewa Harian'], 
                    y=['Hari Kerja', 'Hari Libur', 'Jumlah Sewa Harian'], 
                    color_continuous_scale='viridis')
    
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            fig.add_annotation(x=i, y=j, 
                               text=f'{corr_matrix.iloc[i, j]:.2f}', 
                               showarrow=False, 
                               font=dict(color='black' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'white'))
    
    fig.update_layout(title='Korelasi antara Jumlah Penyewaan Sepeda Harian dengan Hari Kerja dan Hari Libur', font=dict(size=11))
    st.plotly_chart(fig)


# Function to visualize bike rentals based on weather situation
def visualize_weather_counts(data):
    # Menghitung jumlah penyewaan sepeda berdasarkan workingday
    bike_rentals_per_weather = data.groupby('weathersit')['cnt'].sum().reset_index()
    bike_rentals_per_weather.columns = ['Weather Situation', 'Total Rentals']
    
    fig = px.bar(bike_rentals_per_weather, x='Weather Situation', y='Total Rentals', 
                 title='Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca', 
                 labels={'Weather Situation': 'Kondisi Cuaca', 'Jumlah Sewa Harian': 'Jumlah Penyewaan Sepeda'},
                 color='Weather Situation',
                 color_discrete_map={'1': 'blue', '2': 'green', '3': 'red'})  # Specify discrete colors
    
    fig.update_xaxes(title_text='Kondisi Cuaca')
    fig.update_yaxes(title_text='Jumlah Penyewaan Sepeda')
    fig.update_xaxes(tickvals=[1, 2, 3], ticktext=['1', '2', '3'])
    st.plotly_chart(fig)

# Function to visualize bike rentals based on working day
def visualize_workingday_counts(data):
    workingday_counts = data.groupby('workingday')['cnt'].sum().reset_index()
    workingday_counts.columns = ['Working Day', 'Counts']
    workingday_counts['Working Day'] = workingday_counts['Working Day'].map({0: 'Hari Libur', 1: 'Hari Kerja'})
    
    fig = px.bar(workingday_counts, x='Working Day', y='Counts', 
                 title='Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur', 
                 labels={'Working Day': 'Hari', 'Counts': 'Jumlah Penyewaan Sepeda'},
                 color='Working Day', color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_xaxes(title_text='Hari Kerja / Hari Libur')
    fig.update_yaxes(title_text='Jumlah Penyewaan Sepeda')
    st.plotly_chart(fig)

# Display the selected question and visualization based on selected question
st.title(':green[Analisis] Data Penyewaan Sepeda Harian :bar_chart:')

if question == 'Pertanyaan 1':
    st.write("### Bagaimana korelasi antara kondisi cuaca dengan jumlah penyewaan sepeda harian ?")
    visualize_correlation_1(data)
elif question == 'Pertanyaan 2':
    st.write("### Bagaimana korelasi antara hari libur, hari kerja, dan jumlah penyewaan sepeda harian ?")
    visualize_correlation_2(data)
elif question == 'Pertanyaan 3':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara setiap cuaca?")
    st.write("- 1: Clear, Few clouds, Partly cloudy, Partly cloudy")
    st.write("- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist")
    st.write("- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds")
    visualize_weather_counts(data)
elif question == 'Pertanyaan 4':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara hari kerja dan hari libur?")
    visualize_workingday_counts(data)
