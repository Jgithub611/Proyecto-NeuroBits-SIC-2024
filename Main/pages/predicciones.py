import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import plotly.express as px
import streamlit as st
st.set_page_config(
    page_title="",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

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
st.markdown("<h1 style='text-align: center;'>Dogecoin predicciones</h1>", unsafe_allow_html=True)
st.image(logo, width=200)
with st.sidebar: 
    predict=st.button("Generar predicción",key="button")
if predict:

    doge_data = pd.read_csv('DOGE-USD.csv')
    doge_data = doge_data.drop_duplicates()
    for column in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
        doge_data[column] = doge_data[column].ffill().bfill()
    doge_data['Date'] = pd.to_datetime(doge_data['Date'])
    doge_data.set_index('Date', inplace=True)
    doge_data = doge_data.sort_index()
    doge_data_weekly = doge_data['Close'].resample('W').mean()

    model_sarimax = SARIMAX(doge_data_weekly, order=(2, 1, 2), seasonal_order=(1, 1, 1, 52))
    sarimax_model = model_sarimax.fit(maxiter=10, disp=True)#########################################

    forecast_steps = 365
    forecast = sarimax_model.get_forecast(steps=forecast_steps)

    forecast_index_weekly = pd.date_range(start=doge_data_weekly.index[-1], periods=forecast_steps + 1, freq='W')[1:]
    forecast_weekly = pd.DataFrame({
        'Semana': forecast_index_weekly,
        'Predicción_Cierre': forecast.predicted_mean,
        'Límite_Inferior': forecast.conf_int().iloc[:, 0],
        'Límite_Superior': forecast.conf_int().iloc[:, 1]
    })

    forecast_daily = forecast_weekly.set_index('Semana').resample('D').interpolate(method='linear').reset_index()
    forecast_daily.rename(columns={'Semana': 'Fecha'}, inplace=True)

    forecast_daily.to_csv('Predicciones_Diarias_Dogecoin_SARIMAX.csv', index=False)

    st.title('Predicción de Precios de Dogecoin (SARIMAX)')

    fig = px.line(
        doge_data.reset_index(), 
        x='Date', y='Close', 
        labels={'Date': 'Fecha', 'Close': 'Precio (USD)'},
        title='Datos Históricos y Predicciones de Dogecoin (SARIMAX)'
    )

    fig.add_scatter(x=forecast_weekly['Semana'], 
                    y=forecast_weekly['Predicción_Cierre'], 
                    mode='lines', 
                    name='Predicción (Semanal)', 
                    line=dict(color='orange'))

    fig.add_scatter(x=forecast_weekly['Semana'], 
                    y=forecast_weekly['Límite_Inferior'], 
                    mode='lines', 
                    name='Límite Inferior', 
                    line=dict(dash='dot', color='orange'))

    fig.add_scatter(x=forecast_weekly['Semana'], 
                    y=forecast_weekly['Límite_Superior'], 
                    mode='lines', 
                    name='Límite Superior', 
                    line=dict(dash='dot', color='orange'))

    st.plotly_chart(fig, use_container_width=True)