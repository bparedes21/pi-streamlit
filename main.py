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
def funcion_crearDF_por_año(año,base_currency):
    endpoint_url='https://ftx.com/api/markets'
    
    quote_currency= 'USD'
    request_url = f'{endpoint_url}/{base_currency}/{quote_currency}'
    import pandas as pd
    import requests
    from datetime import datetime
    # 1 day = 60 * 60 * 24 (60 segundos 1 (minuto) por 60 minutos(1 hora) por 24 (horas))
    daily=str(60*60*24)
    #Obtengo los datos a partir de 2022
    start_date = datetime(año, 1, 1).timestamp()
    
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
    list_monedas=["LINK","MATIC","USDT","SRM","XRP","DOT","DAI","SOL","DOGE"]
    
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
    page_title="Dashboard de FTX : ",
    page_icon="✅",
    layout="wide",
)



st.title("Dashboard de FTX")
st.write(":sunglasses:")
col1,col2,col3,col4= st.columns([1,1,1,1])
column1,column2= st.columns([1,1])
col_1,col_2= st.columns(2)

#st.info('This is a purely informational message', icon="ℹ️")
with st.sidebar:
    list_menu=["Reporte de calidad y detalle de los datos","Volumen de transaccion para la moneda elegida","Varianza","Calculadora","Media Móvil"]
    opcion_elegida=st.sidebar.selectbox( "Menu",list_menu )

    if(opcion_elegida=="Calculadora"):
        
        
        precio_lit=list(df_stadistic["precio"])
        datos_list=list(df_stadistic["moneda"])
        
        
        with column1:
            st.title("Obtener conversion :")
            #st.subheader("Elegir Criptomoneda")
            st.success(" ")
            list_menu3=["Conversion de Criptomoneda/USD","USD/Criptomoneda"]
            opcion_elegida2=st.sidebar.selectbox( "Menu elegir conversion ",list_menu3)
            number = st.number_input('Insertar un monto')
            st.subheader("Criptomoneda/USD")
            List_menu2=["LINK","MATIC","USDT","SRM","XRP","DOT","DAI","SOL","DOGE"]
            opcion_elegida4=st.sidebar.selectbox( "Menu para elegir Criptomoneda",List_menu2)
            
            df_moneda_elegida=df_stadistic[df_stadistic["moneda"]==opcion_elegida4]
            if(opcion_elegida2=="Conversion de Criptomoneda/USD"):
                
                USD_equivalencia=float(df_moneda_elegida["precio"].values)
                
                multiplicacion_monedas=number*USD_equivalencia
                st.write(number,"Criptomonedas equivalen a ",multiplicacion_monedas," USD")
            else:
                coin_precio=float(df_moneda_elegida["precio"].values)
                division_monedas=number/coin_precio
                st.write(number,"USD equivalen a ",division_monedas," Criptomoneda")
            with column2:   
                import plotly.express as px
                fig2 = px.bar(df_stadistic, x='moneda', y='precio',title="Precio en USD para cada Criptomoneda")
                st.plotly_chart(fig2)
                
    elif (opcion_elegida=="Volumen de transaccion para la moneda elegida"): 
        with st.sidebar:
            
            list_menu1=["LINK","MATIC","USDT","SRM","XRP","DOT","DAI","SOL","DOGE"]
            opcion_elegida1=st.sidebar.selectbox( "Menu para elegir Criptomoneda",list_menu1 )
            st.subheader("Volumen de transacciones en UDS")
            st.success("Grafico de linea")
            df_concat=funcion_crearDF_por_año(2019,opcion_elegida1)
            df_concat['date'] = pd.to_datetime(df_concat['date'], format="%Y %m/%d")
            df_concat=df_concat.drop(columns=["año","mes","dia","open","high","low","close"])
            max_year=df_concat['date'].dt.year.max()
            min_year=df_concat['date'].dt.year.min()
            max_year=int(max_year)
            min_year=int(min_year)
            with column1:
                
                year_slider = st.slider('Año precio historico:',min_year,  max_year, max_year)
                datos_año=df_concat[df_concat['date'].dt.year==year_slider]
                #
                datos_año=datos_año.set_index('date', inplace = False)
            
                import plotly_express as px
            
                fig=px.line(datos_año, x = datos_año.index, y = datos_año.columns)
            
                st.plotly_chart(fig)
                #st.write(start_date)
    elif (opcion_elegida=="Varianza"):      
        
        with col_1:
            st.success("La varianza de las ultimas 24 hs para las Criptomonedas es de:")   
            col_1.metric(label="Varianza", value=varianza_coin, 
             )
            st.write("Esto quiere decir que la diferencia entre los precios de las distintas monedas será de: Criptomonedas ",varianza_coin)    
        with col_1:
            st.success("La varianza de las ultimas 24 hs en UDS es de:")   
            col_1.metric(label="Varianza", value=varianza_USD,
             )    
            st.write("Esto quiere decir que la diferencia entre los precios de las distintas monedas será de: USD ",varianza_USD)
    elif (opcion_elegida=="Media Móvil"):
        import plotly.graph_objects as go
        list_menu3=["LINK","MATIC","USDT","NEAR","XRP","DOT","DAI","SOL","DOGE"]
        opcion_elegida3=st.sidebar.selectbox( "Menu para elegir Criptomoneda",list_menu3 )
        df_concat1=funcion_crearDF_por_año(2022,opcion_elegida3)
        df_concat1['date'] = pd.to_datetime(df_concat1['date'], format="%Y %m/%d")
        mayor_mes=df_concat1["mes"].max()
        df_mes=df_concat1[df_concat1["mes"]==mayor_mes]
        mayor_dia=df_mes["dia"].max()
        df_dia=df_mes[df_mes["dia"]==mayor_dia]
        

        array_open=df_dia["open"].values
        open=float(array_open[0])

        array_maximo=df_dia["high"].values
        maximo=float(array_maximo[0])

        array_minimo=df_dia["low"].values
        minimo=float(array_minimo[0])

        array_close=df_mes["close"].values
        cierre=float(array_close[0])

        with col1:
    
            st.subheader("Precio Medio")
            st.write("Precio Medio (PM). Cociente entre el precio máximo y el precio mínimo dividido entre dos, esto es:")
            #PM= (Máximo + Mínimo)/2
            PM= (maximo + minimo)/2
            #here x as height
            st.write("PM =",maximo,"+",minimo,"/2")
            st.write("El valor para Precio Medio (PM) es",PM)
           
            col1.metric(label="PM", value=PM
             )
        with col2:   
            st.subheader("Precio Típico")
            
            st.write("Precio Típico (PT). Cociente entre el precio máximo, precio mínimo y el cierre, dividido entre 3:")
            #PT= (Máximo + Mínimo + Cierre)/3
            PT= (maximo + minimo+cierre)/3
            #here x as height
         
            st.write("PT =",maximo,"+",minimo,"+",cierre,"/3")
            st.write("El valor para Precio Típico (PT) es",PT)
            
            col2.metric(label="PT", value=PT,
             )

        with col3:
            st.subheader("Precio Ponderado")
            
            st.write("Precio Ponderado (PP). Cociente entre el precio máximo, el precio mínimo, la apertura y el cierre, dividido entre 4:")
            #PT= (Máximo + Mínimo + Cierre)/3
            PP= (maximo + minimo+open+cierre)/4
            #here x as height
         
            st.write("PP =",maximo,"+",minimo,"+",open,"+",cierre,"/4")
            st.write("El valor para Precio Ponderado (PP) es",PP)
            
            col3.metric(label="PT", value=round(PP,2),
             )
    else:
        with col_1: 
            st.title("Breve descripcion de los datos")
            st.markdown(
                    "Para obtener los datos utilice 2 tipos de url"
                    "Con una obtuve ultimos datos de 24hs utilizando el nombre de la criptomoneda"
                    "**DESCRIPTION columnas y tipo de datos: "    
                    "**price:Float"
                        )
            st.markdown(
                    "Con una obtuve ultimos datos de 24hs utilizando el nombre de la criptomoneda"
                    "**DESCRIPTION columnas y tipo de datos: "    
                    "**open:Float ,"
                    "**high:Float ,"
                    "**low:Float ,"
                    "**date:datetime ,"
                    "Al poder utilizar los datos sin problemas puedo llegar a la conclusion de que tienen buena calidad"
                    "Es decir no me encontre con registros faltantes, ni caracteres extraños"
                        )   
                
           
        

                