import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dogecoin Analysis Dashboard",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
 [data-testid="block-container"] {
     padding-left: 2rem;
     padding-right: 2rem;
     padding-top: 1rem;
     padding-bottom: 0rem;
     margin-bottom: -7rem;
 }
 [data-testid="stMetric"] {
     background-color: #2D2D2D;
     text-align: center;
     padding: 15px 0;
     border-radius: 10px;
     box-shadow: 0px 10px 20px 20px #0000002b;
 }
 </style>
""", unsafe_allow_html=True)

st.sidebar.markdown('''
---
NeutroBits
''')

logo = "dogecoin-doge-logo.png"  
st.markdown("<h1 style='text-align: center;'>Dogecoin análisis</h1>", unsafe_allow_html=True)
st.image(logo, width=200)

file_path = 'DOGE-USD.csv'
dataset = pd.read_csv(file_path)
dataset.dropna(inplace=True)
dataset['Date'] = pd.to_datetime(dataset['Date'])

with st.sidebar:
    st.title('🐕Dogecoin')
    
    # Date filter
    years = dataset['Date'].dt.year.unique()
    selected_year = st.selectbox('Año', years[::-1])
    filtered_data = dataset[dataset['Date'].dt.year == selected_year]

st.title(f"Dogecoin análisis año {selected_year}")

col1, col2, col3 = st.columns(3)
col1.markdown(f"<h4 style='text-align:center;'>Precio más alto</h4>", unsafe_allow_html=True)
col2.markdown(f"<h4 style='text-align:center'>Precio más bajo</h4>", unsafe_allow_html=True)
col3.markdown(f"<h4 style='text-align:center'>Volumen total</h4>", unsafe_allow_html=True)
col1.metric(" ", f"${filtered_data['High'].max():,.4f}")
col2.metric(" ", f"${filtered_data['Low'].min():,.4f}")
col3.metric(" ", f"{filtered_data['Volume'].sum():,.0f}")

st.subheader("Movimiento de precios")
price_chart = px.line(
    filtered_data, 
    x='Date', 
    y=['Open', 'High', 'Low', 'Close'], 
    labels={'value': 'Price (USD)', 'Date': 'Date'},
    title="Daily Prices", 
)
st.plotly_chart(price_chart, use_container_width=True)

st.subheader("Volumen de operaciones")
volume_chart = px.bar(
    filtered_data, 
    x='Date', 
    y='Volume', 
    labels={'Volume': 'Volume', 'Date': 'Date'},
    title="Daily Trading Volume",
)
st.plotly_chart(volume_chart, use_container_width=True)