import streamlit as st
import pandas as pd
import plotly.express as px
import simulador as sm
#######################################
st.set_page_config(
    page_title="Dogecoin Analysis Dashboard",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)
sm.main() #Load data simulator
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
            
[data-testid="stButton"] {
   /*background-color: #4CAF50;*/ 
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;   
    font-size: 16px;
}

 </style>
""", unsafe_allow_html=True)

st.sidebar.markdown('''
NeutroBits
''')
logo = "dogecoin-doge-logo.png"  
st.markdown("<h1 style='text-align: center;'>Dogecoin análisis</h1>", unsafe_allow_html=True)
st.image(logo, width=200)
file_path = 'DOGE-USD.csv'
dataset = pd.read_csv(file_path)
dataset.dropna(inplace=True)#Eliminar datos nulos
dataset['Date'] = pd.to_datetime(dataset['Date'])
with st.sidebar:
    st.title('🐕Dogecoin')
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

st.subheader("Relación de precios")
dataset.dropna(inplace=True)
fig = px.scatter(filtered_data,
                x = 'Open',
                y = 'Close',
                title = "Relación entre Precio de Apertura y Precio de Cierre",
                labels = {'Open': 'Precio de Apertura', 'Close': 'Precio de Cierre'},
                size='Volume', 
                hover_data=['Date'], 
                template='plotly_white'     
                )
st.plotly_chart(fig,use_container_width=True)

st.subheader("Correlación")
numerical_data = filtered_data.select_dtypes(include='number')
correlation_matrix = numerical_data.corr()
custom_colorscale = ['#FFFFFF','#3848c7']
fig = px.imshow(correlation_matrix,
                color_continuous_scale=custom_colorscale,
                text_auto='.2f',
                zmin=0, zmax=1,
                labels=dict(color="Correlación"),
                title=f'Matriz de Correlación para el Año {selected_year}') 

fig.update_traces(xgap=2, ygap=2)  
fig.update_layout(
    font=dict(size=12), 
    title_font=dict(size=16), 
    margin=dict(l=40, r=40, t=40, b=40)  
)
st.plotly_chart(fig,use_container_width=True)