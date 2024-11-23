import pandas as pd
import plotly.express as px
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output

# Función para cargar datos de Dogecoin desde un archivo CSV
def cargar_datos_csv(ruta):
    try:
        dataset = pd.read_csv(ruta)
        dataset.dropna(inplace=True)
        dataset['Date'] = pd.to_datetime(dataset['Date'])
        return dataset
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

# Simulador de inversión interactivo
def simulador_inversion_interactivo(inversion_inicial, num_transacciones, objetivo_ganancias, duracion, estrategia='normal'):
    cambios_simulados = np.random.normal(0, 0.05, num_transacciones)  # Cambios aleatorios en el precio
    saldo = inversion_inicial
    historico_saldo = [saldo]

    for i in range(num_transacciones):
        if estrategia == 'agresiva':
            cambio = cambios_simulados[i] * 1.5  # Aumentar la volatilidad
        elif estrategia == 'conservadora':
            cambio = cambios_simulados[i] * 0.5  # Reducir la volatilidad
        else:
            cambio = cambios_simulados[i]  # Estrategia normal

        saldo *= (1 + cambio)
        historico_saldo.append(saldo)
        if saldo >= objetivo_ganancias:
            print(f"🎯 ¡Objetivo de ganancias alcanzado! Saldo: ${saldo:.9f}")
            break

    return saldo, historico_saldo

# Función para graficar saldo histórico


def graficar_saldo_historico(saldo_historico): #Cambio de biblioteca
    # Crear un DataFrame para facilitar el uso con Plotly
    data = {
        'Número de Transacciones': range(1, len(saldo_historico) + 1),
        'Saldo (USD)': saldo_historico
    }

    fig = px.line(
        data,
        x='Número de Transacciones',
        y='Saldo (USD)',
        title='Simulación de Inversión en Dogecoin',
        markers=True,  
        template='plotly_white'
    )

    # Personalizar diseño
    fig.update_layout(
        xaxis_title='Número de Transacciones',
        yaxis_title='Saldo (USD)',
        title_font_size=20,
        font=dict(size=16),
        showlegend=False
    )
    
  


# Función para calcular el rendimiento de la inversión
def calcular_rendimiento(inversion_inicial, saldo_final):
    return (saldo_final - inversion_inicial) / inversion_inicial * 100

# Función para mostrar el rendimiento de la inversión
def mostrar_rendimiento(inversion_inicial, saldo_final):
    rendimiento = calcular_rendimiento(inversion_inicial, saldo_final)
    print(f"### Rendimiento de la Inversión: {rendimiento:.2f}%")
    if rendimiento > 0:
        return(f"Rendimiento de la Inversión: {rendimiento:.2f}%"),("💰 ¡Felicidades! Has ganado dinero.")
    else:
        return(f"Rendimiento de la Inversión: {rendimiento:.2f}%"),("⚠️ Has perdido dinero. Considera revisar tu estrategia de inversión.")

# Función principal
def main():
    # Cargar datos
    dataset = cargar_datos_csv('DOGE-USD.csv')

    # Simulación de inversión interactiva
    inversion_inicial = widgets.FloatText(value=10.0, description='Inversión Inicial (USD):')
    objetivo_ganancias = widgets.FloatText(value=15.0, description='Objetivo de Ganancias (USD):')
    num_transacciones = widgets.IntSlider(value=100, min=10, max=500, step=10, description='Transacciones:')
    estrategia = widgets.Dropdown(options=['normal', 'agresiva', 'conservadora'], description='Estrategia:')
    dias_futuros = widgets.IntSlider(value=2, min=1, max=7, description='Días a Predecir:')

    button = widgets.Button(description="Ejecutar Simulación")
    output = widgets.Output()

    def on_button_clicked(b):
        with output:
            clear_output()
            saldo_final, saldo_historico = simulador_inversion_interactivo(
                inversion_inicial.value,
                num_transacciones.value,
                objetivo_ganancias.value,
                dias_futuros.value * 24,
                estrategia.value
            )
            graficar_saldo_historico(saldo_historico)
            mostrar_rendimiento(inversion_inicial.value, saldo_final)

    button.on_click(on_button_clicked)

    display(inversion_inicial, objetivo_ganancias, num_transacciones, estrategia, dias_futuros, button, output)

# Ejecución del programa
main()
