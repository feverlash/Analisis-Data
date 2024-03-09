import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title=":green[Analisis] Data Penyewaan Sepeda Harian :bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded")

# Load the data
url = 'https://raw.githubusercontent.com/feverlash/Analisis-Data/1b784470df03a8e53000ea6a7393bf2fbafc7919/Bike-sharing-dataset/cleaned_day.csv'
data = pd.read_csv(url)

# Sidebar with options
st.sidebar.title(':computer: :thinking_face: :question:')
st.sidebar.title('**Pilihan Pertanyaan Bisnis**')
st.sidebar.markdown("**Pada proyek ini saya menganalisis dataset sewa sepeda harian untuk menjawab beberapa pertanyaan di bawah ini**")
question = st.sidebar.selectbox('Pilih Pertanyaan:', ['Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3', 'Pertanyaan 4'])

#Fungsi 1
import plotly.express as px

import plotly.express as px
import streamlit as st

def visualize_season_counts(data):
    data['season'] = data['season'].map({
        'Spring': 'Spring',
        'Summer': 'Summer',
        'Fall': 'Fall',
        'Winter': 'Winter'
    })

    season_counts = data.groupby('season')['total_rental'].sum().reset_index()

    color_map = {'Spring': '#4CAF50', 
                 'Summer': '#FFC107',  
                 'Fall': '#FF5722', 
                 'Winter': '#2196F3'}

    fig = px.bar(season_counts, x='season', y='total_rental', 
                 title='Total Jumlah Penyewaan Sepeda Berdasarkan Musim',
                 labels={'season': 'Musim', 'total_rental': 'Total Penyewaan Sepeda'},
                 color='season', color_discrete_map=color_map)

    fig.update_xaxes(title_text='Musim')
    fig.update_yaxes(title_text='Total Penyewaan Sepeda')
    st.plotly_chart(fig)

#Fungsi 2
def visualize_year_tren(data, year_2011, year_2012):
    if not year_2011 and not year_2012:
        st.write(":heavy_exclamation_mark: Silahkan pilih salah satu checkbox untuk menampilkan grafik :heavy_exclamation_mark:")
        return

    data['month'] = pd.Categorical(data['month'], categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
    
    monthly_counts = data.groupby(by=["month","year"]).agg({"total_rental": "sum"}).reset_index()

    fig = px.line(title="Jumlah sepeda yang disewakan berdasarkan Bulan dan Tahun",
                  labels={"month": "Bulan", "total_rental": "Total Penyewaan Sepeda", "year": "Tahun"},
                  markers=False)

    if year_2011:
        fig.add_scatter(x=monthly_counts[monthly_counts['year']==0]['month'], 
                        y=monthly_counts[monthly_counts['year']==0]['total_rental'],
                        mode='lines', name='2011', marker=dict(color='blue'))
    
    if year_2012:
        fig.add_scatter(x=monthly_counts[monthly_counts['year']==1]['month'], 
                        y=monthly_counts[monthly_counts['year']==1]['total_rental'],
                        mode='lines', name='2012', marker=dict(color='green'))

    fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title="Tahun",
                      width=800, height=500)
    
    st.plotly_chart(fig)



#Fungsi 3
def visualize_weather_counts(data):
    # Menghitung jumlah penyewaan sepeda berdasarkan workingday
    bike_rentals_per_weather = data.groupby('weather_cond')['total_rental'].sum().reset_index()
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

#Fungsi 4
def visualize_workingday_counts(data):
    workingday_counts = data.groupby('workingday')['total_rental'].sum().reset_index()
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
    st.write("### Bagaimana perbedaan pola penyewaan sepeda pada setiap musim?")
    visualize_season_counts(data)
elif question == 'Pertanyaan 2':
    st.write("### Bagaimana tren jumlah total penyewaan sepeda dari bulan ke bulan selama periode 2011 dan 2012?")
    year_2011 = st.checkbox('Tahun 2011', value=True)
    year_2012 = st.checkbox('Tahun 2012', value=True)
    visualize_year_tren(data, year_2011, year_2012)
elif question == 'Pertanyaan 3':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara setiap cuaca?")
    visualize_weather_counts(data)
elif question == 'Pertanyaan 4':
    st.write("### Bagaimana perbedaan pola penyewaan sepeda antara hari kerja dan hari libur?")
    visualize_workingday_counts(data)
