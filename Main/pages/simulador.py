import streamlit as st
import pandas as pd
import plotly.express as px
import simulador as sm
st.set_page_config(
    page_title="Dogecoin Simulator",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded"
)
#Load data sm
sm.main()

st.markdown("""
<style>
 [data-testid="block-container"] {
     padding-left: 2rem;
     padding-right: 2rem;
     padding-top: 1rem;
     padding-bottom: 0rem;
     margin-bottom: -7rem;
            
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
st.markdown("<h1 style='text-align: center;'>Dogecoin Simulador</h1>", unsafe_allow_html=True)
st.image(logo, width=200)

file_path = 'DOGE-USD.csv'
dataset = pd.read_csv(file_path)
dataset.dropna(inplace=True)
dataset['Date'] = pd.to_datetime(dataset['Date'])


with st.sidebar: #sim
    st.title('🐕Dogecoin')
    inversion_inicial=st.number_input("Inversión inicial(USD)",value=5)
    objetivos_ganancia=st.number_input("Objetivo de ganancias(USD)",value=8)
    estrategia=st.selectbox("Estrategia",["Normal","Agresiva","Conservadora"],placeholder="Seleccione una estrategia") 
    num_transaciones=st.slider("Número de transacciones",step=10,min_value=10,max_value=500,value=20)
    dias_futuros=st.slider("Días a predecir",step=1,min_value=1,max_value=7,value=2)
    
st.subheader("Simulación")
with st.container(): 
    def fig_sim():
        simulacion =px.line(
        filtered_data,
        x='Número de Transacciones',
        y='Saldo (USD)',
        title='Simulación de Inversión en Dogecoin',
        markers=True,  
        template='plotly_white'
                )
        simulacion.update_layout(
        xaxis_title='Número de Transacciones',
        yaxis_title='Saldo (USD)',
        title_font_size=20,
        font=dict(size=16),
        showlegend=False,
        width=1280,  
        height=600  
                )
        st.plotly_chart(simulacion, use_container_width=False)
    
with st.sidebar: #Simulation buttom
    simulation=st.button("Iniciar simulación",key="button")
if simulation:  
    saldo_total=sm.simulador_inversion_interactivo(inversion_inicial,num_transaciones,objetivos_ganancia,dias_futuros,estrategia)[0]
    saldo_historico=sm.simulador_inversion_interactivo(inversion_inicial,num_transaciones,objetivos_ganancia,dias_futuros,estrategia)[1]
    sm.graficar_saldo_historico(saldo_historico)
    filtered_data = {
    'Número de Transacciones': range(1, len(saldo_historico) + 1),
    'Saldo (USD)': saldo_historico
    } 
    fig_sim()
    resultado1,resultado2=(sm.mostrar_rendimiento(inversion_inicial,saldo_total))
    if resultado2 =="💰 ¡Felicidades! Has ganado dinero.":
        st.markdown(
            f"""
            <div style='
                text-align: center;
                color: green;
                font-size: 24px;
            '>
                ✅ <strong>Rendimiento Total:</strong> {resultado1},{resultado2}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
         st.markdown(
            f"""
            <div style='
                text-align: center;
                color: red;
                font-size: 24px;
            '>
                ✖️ <strong>Rendimiento Total:</strong> {resultado1},{resultado2}
            </div>
            """,
            unsafe_allow_html=True 
            )