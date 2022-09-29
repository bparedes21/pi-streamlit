from sys import implementation
import streamlit as st
import pandas as pd
import numpy as np

import ccxt
from st_aggrid import AgGrid
#print(ccxt.exchanges)
#archivo=ccxt.exchanges
#AgGrid(archivo)


import pandas as pd
import requests
from datetime import datetime
import time
def funcion_crearDF_por_año(año):
    endpoint_url='https://ftx.com/api/markets'
    base_currency = 'FTT'
    quote_currency = 'USD'

    request_url = f'{endpoint_url}/{base_currency}/{quote_currency}'
    import pandas as pd
    import requests
    from datetime import datetime
    # 1 day = 60 * 60 * 24 (60 segundos 1 (minuto) por 60 minutos(1 hora) por 24 (horas))
    daily=str(60*60*24)
    #Obtengo los datos a partir de 2022
    start_date = datetime(año, 1, 1).timestamp()
    st.write(start_date)
    #Get para obtener los datos de la API en formato JSON
    # Get the historical market data as JSON
    historical = requests.get(
        f'{request_url}/candles?resolution={daily}&start_time={start_date}'
    ).json()
    # Convert JSON to Pandas DataFrame
    df = pd.DataFrame(historical['result'])
    # Convert time to date
    df['date'] = pd.to_datetime(
        df['time']/1000, unit='s', origin='unix'
    ) 
    pd.DataFrame(df ,columns=[	"open",	"high",	"low",	"close","date"])


    # Remove unnecessar columns
    df.drop(['startTime', 'time'], axis=1, inplace=True)
    #dividir date en año, mes, dia. Redondear volume 
    df['año'] = pd.DatetimeIndex(df['date']).year
    df['mes'] = pd.DatetimeIndex(df['date']).month
    df['dia'] = pd.DatetimeIndex(df['date']).day
    
    df['volume']=round(df['volume'],1)
    return df
def funcion_calcular_varianza(li):

  suma=0
  for i in li:
    suma=suma+i
  #print("suma: ",suma)
  promedio2=suma/5
  #print("promedio2: ",promedio2)
  nuevali=[]
  for i in li:

      resta_i=i-promedio2
      #print("varianza: ",resta_i)
      nuevali.append(resta_i**2)
  ##print("nuevali: ",nuevali)
  suma2=0
  for i in nuevali:
    suma2=suma2+i
  #print("suma: ",suma2)
  varianza=suma2/5
  #print("promedio3: ",varianza)
  std_dev=varianza** (0.5)
  return  varianza,std_dev

def funcion_obtener_price_coin_actual():
    import pandas as pd
    import requests
    import numpy as np
   
    markets = requests.get('https://ftx.com/api/markets').json()
    keys_ñl=markets.keys()
    df = pd.DataFrame(markets['result'])
    df.set_index('name', inplace = False)
    list_names=[]
    lista_precio_actual=[]
    lista_conversion=[]
    precio_sin_media=[]
    list_monedas=["LINK","MATIC","USDT","NEAR","XRP","DOT","DAI","SOL","DOGE"]
    
    for moneda in list_monedas:
        string_moneda=moneda+"/USD"
        #print(string_moneda)
        btc_df=df[df["name"]==string_moneda]
        #st.write("I'm ", btc_df, 'years old')
        #btc_df["price"]=btc_df["price"].astype('float')
        price_val=btc_df['price']
        price_val=round(float(btc_df['price']),2)
        #print(price_val)
        lista_precio_actual.append(price_val)
        list_names.append(moneda)
        #conversion
        val_conversion=1/price_val
        lista_conversion.append(val_conversion)
        #print(list_names)
    col=["precio","moneda","precio_usd"]
    c = zip(lista_precio_actual,list_names,lista_conversion)
    df3=pd.DataFrame(c)
    #data_ML_car.loc[data_ML_car['carwidth']]=df[
    df3.columns=col    
    varianza_coin,desv_estd_coin=funcion_calcular_varianza(lista_precio_actual)
    varianza_coin=round(varianza_coin,2)
    desv_estd_coin=round(desv_estd_coin,2) 
    varianza_USD,desv_estd_USD=funcion_calcular_varianza(lista_conversion)
    varianza_USD=round(varianza_USD,2)
    desv_estd_USD=round(desv_estd_USD,2)
    return df3,varianza_coin,desv_estd_coin,varianza_USD,desv_estd_USD

df_stadistic,varianza_coin,desv_estd_coin,varianza_USD,desv_estd_USD=funcion_obtener_price_coin_actual()

st.set_page_config(
    page_title="Dashboard de FTX :",
    page_icon="✅",
    layout="wide",
)

df_concat=funcion_crearDF_por_año(2019)
df_concat['date'] = pd.to_datetime(df_concat['date'], format="%Y %m/%d")
df_concat=df_concat.drop(columns=["año","mes","dia","open","high","low","close"])
#df_concat=df_concat.reset_index(drop=True)
#df_concat=df_concat.drop(columns="index")
st.title("Dashboard de FTX")
col1,col2,col3= st.columns([1,2,1])

with st.sidebar:
    list_menu=["Reporte de calidad y detalle de los datos","Ultimas 24hs","Datos historicos","Varianza, Volumen de transacción ","Calculadora","Media Móvil"]
    opcion_elegida=st.sidebar.selectbox( "Menu",list_menu )

    if(opcion_elegida=="Ultimas 24hs"):
        st.subheader("Ultimas 24hs")
        st.success("layout")
        precio_lit=list(df_stadistic["precio"])
        datos_list=list(df_stadistic["moneda"])
        
        import plotly.graph_objs as go
        with col1:
            
            st.title("Ultimas 24hs")
            fig = go.Figure(
            go.Pie(
            labels = datos_list,
            values = precio_lit,
            hoverinfo = "label+percent",
            textinfo = "value"
            ))
            st.header("Pie chart")
            st.plotly_chart(fig)
    elif opcion_elegida=="Datos historicos": 
        list_menu2=["Filtrar por Año","Filtrar por Año y Mes","Filtrar por Año, Mes y Dia"]
        
        opcion_elegida2=st.sidebar.selectbox( "Menu",list_menu2 )  
        if(opcion_elegida2=="Filtrar por Año"):
            with col2:
                max_year=df_concat['date'].dt.year.max()
                min_year=df_concat['date'].dt.year.min()
                max_year=int(max_year)
                min_year=int(min_year)
                year_slider = st.slider('Año precio historico:',min_year,  max_year, max_year)
                datos_año=df_concat[df_concat['date'].dt.year==year_slider]
                #df_reset_datos_mes=datos_año.reset_index()
                #df_reset_datos_mes.duplicated(keep='first')
                datos_año=datos_año.set_index('date', inplace = False)
                
                import plotly_express as px
            
                fig=px.line(datos_año, x = datos_año.index, y = datos_año.columns)
                # Plot!
                st.plotly_chart(fig)
                #sns.line_chart(datos_año, x = datos_año.index, y = datos_año.columns)
                #st.line_chart(datos_año)

        elif (opcion_elegida2=="Filtrar por Año y Mes"): 
            with col2:
                max_year=df_concat['date'].dt.year.max()
                min_year=df_concat['date'].dt.year.min()
                max_year=int(max_year)
                min_year=int(min_year)
                year_slider = st.slider('Año precio historico:',min_year,  max_year, max_year)
                datos_año=df_concat[df_concat['date'].dt.year==year_slider]
                datos_año.duplicated(keep='first')
                max_month=datos_año['date'].dt.month.max()
                min_month=datos_año['date'].dt.month.min()
                max_month=int(max_month)
                min_month=int(min_month)

                    
                month_slider = st.slider('Mes precio historico:',min_month,  max_month, max_month)
                datos_mes=datos_año[datos_año['date'].dt.month==month_slider]
                #df_reset_datos_mes=datos_mes.reset_index()
                #df_reset_datos_mes.duplicated(keep='first')
                datos_mes=datos_mes.set_index('date', inplace = False)
                
                import plotly_express as px
            
                fig=px.line(datos_mes, x = datos_mes.index, y = datos_mes.columns)
        else:  
            with col2:
                max_year=df_concat['date'].dt.year.max()
                min_year=df_concat['date'].dt.year.min()
                max_year=int(max_year)
                min_year=int(min_year)

                year_slider = st.slider('Año precio historico:',min_year,  max_year, max_year)
                datos_año=df_concat[df_concat['date'].dt.year==year_slider]
                datos_año.duplicated(keep='first')

                max_month=datos_año['date'].dt.month.max()
                min_month=datos_año['date'].dt.month.min()
                max_month=int(max_month)
                min_month=int(min_month)

                month_slider = st.slider('Mes precio historico:',min_month,  max_month, max_month)
                datos_mes=datos_año[datos_año['date'].dt.month==month_slider]

                datos_mes.duplicated(keep='first')
                max_da=datos_mes['date'].dt.day.max()
                max_da=int(max_da)
                min_da=datos_mes['date'].dt.day.min()
                min_da=int(min_da)
                
                day_slider = st.slider('Dia precio historico:',min_da,  max_da, max_da)
                datos_dia=datos_mes[datos_mes['date'].dt.day==day_slider]
            
                datos_dia=datos_dia.set_index('date', inplace = False)
                
                import plotly_express as px
            
                fig=px.line(datos_dia, x = datos_dia.index, y = datos_dia.columns)

            #df_stadistic,varianza_coin,desv_estd_coin,varianza_USD,desv_estd_USD

