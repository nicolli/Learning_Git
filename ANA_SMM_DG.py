#Trabalhando com arquivos da ANA para Delmiro Gouveia e Sao Miguel dos Milagres

""" Ferramentas utilizadas:
    - Tratamento de falhas
    - Visualização de série temporal
    - Redução de série e disponibilização
    - Leitura de dados
    - Aquisição de dados abertos 
    - Geração de gráficos interativos
    - Caracterização de disponibilidade de dados em série/séries (Gantt)
    - Gravação de dados 
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

#Definindo diretorio
try:
    cwd=os.chdir("C:\\Users\\albuq\\OneDrive\\UFAL\\ENGENHARIA_AMBIENTAL_E_SANITÁRIA\\QUINTO_PERIODO\\INTRODUCAO_A_CIENCIA DE DADOS\\CODANDO\\DADOS")
    files = os.listdir(cwd) 
    for i in files:
      print(i,end=" | ")
except:
    pass

#Importando os arquivos 
chuvas_smm = pd.read_csv("CHUVASMM.zip", compression='zip',header=0,skiprows=14,decimal=",",sep=";",parse_dates=True,index_col=["Data"],dayfirst=True)
chuvas_dg= pd.read_csv("CHUVADG.zip", compression='zip', header=0,skiprows=14,decimal=",",sep=";", parse_dates=True,index_col=["Data"],dayfirst=True)

#Observando os dados para SMM
chuvas_smm.shape
chuvas_smm.columns 
chuvas_smm.head()
chuvas_smm.tail()
chuvas_dg.info()
chuvas_smm.describe()
chuvas_smm["Maxima"].describe()

#Observando os dados para DG
chuvas_dg.shape
chuvas_dg.columns 
chuvas_dg.head()
chuvas_dg.tail()
chuvas_dg.info()
chuvas_dg.describe()
chuvas_dg["Maxima"].describe()

#Mudar o nome da coluna pelo nome
chuvas_dg=chuvas_dg.rename(columns = {'//EstacaoCodigo':'CodigoEstacao'})
chuvas_smm=chuvas_smm.rename(columns = {'//EstacaoCodigo':'CodigoEstacao'})

#Colocando o índice na ordem
chuvas_smm.sort_index(ascending=False, inplace=True)
chuvas_dg.sort_index(ascending=False, inplace=True)

#Pegando máximo e mínimo valor do índice (datas)
chuvas_smm.index.get_values().max()
chuvas_smm.index.get_values().min()
chuvas_dg.index.get_values().max()
chuvas_dg.index.get_values().min()

#Criando novo indice com frequência mensal (primeiro dia do mês como no dataframe original) e reindexando
index_general = pd.date_range('01/01/1963','01/01/2001', freq="MS",format="%d/%m/%Y") 
chuvas_smm=chuvas_smm.reindex(index_general)
chuvas_smm_interpolate=chuvas_smm.reindex(index_general).interpolate(how="polinomial",order=3)
chuvas_dg=chuvas_dg.reindex(index_general)
chuvas_dg_interpolate=chuvas_dg.reindex(index_general).interpolate(how="polinomial",order=3)


#Redução de série
    #Media anual (sem intepolação)
    smm_anual=chuvas_smm.resample("A").mean()
    dg_anual=chuvas_dg.resample("A").mean()
    #Media anual (com interpolação)
    smm_anual_interpolate=chuvas_smm_interpolate.resample("A").mean()
    dg_anual_interpolate=chuvas_dg_interpolate.resample("A").mean()
    #Media trimestral (sem intepolação)
    smm_trimestral=chuvas_smm.resample("3MS").mean()
    dg_trimestral=chuvas_dg.resample("3MS").mean()
    #Media trimestral (com intepolação)
    smm_trimestral_interpolate=chuvas_smm_interpolate.resample("A").mean()
    dg_trimestral_interpolate=chuvas_dg_interpolate.resample("A").mean()


#Plotando
  #Sao Miguel dos Milagres
    #Simples
    chuvas_smm.plot(x=chuvas_smm.index, y=['Total', 'Maxima'])
    #Boxplot (Gráficos interativos via Plotly)
        total1= go.Box(
        y=chuvas_smm["Total"]
    )
    maxima1 = go.Box(
        y=chuvas_smm["Maxima"]
    )
    smm_box_mt= [total1, maxima1]
    py.offline.plot(smm_box_mt, filename="chuvas_smm_box.html")
    
    #Visualização de Série Temporal (GI)
      #Maxima Mensal
      chuvas_dg_max= [go.Scatter(x=chuvas_smm.index, y=chuvas_smm['Maxima'] )]
      py.iplot(chuvas_dg_max, filename='chuvas_dg_max.html')
      #Dias de chuva
      chuvas_smm_dias= [go.Scatter(x=chuvas_smm.index, y=chuvas_smm['NumDiasDeChuva'] )]
      py.offline.plot(chuvas_smm_dias, filename='chuvas_smm_dias.html')
      
    #Gantt (GI)

  #Delmiro Gouveia
    #Simples
    chuvas_dg.plot(x='Data', y=['Total', 'Maxima'])
    #Boxplot (Graficos interativos via Plotly)
    total2= go.Box(
        y=chuvas_dg["Total"]
    )
    maxima2 = go.Box(
        y=chuvas_dg["Maxima"]
    )
    dg_box_mt= [total1, maxima1]
    py.offline.plot(dg_box_mt,filename='chuvas_dg_box.html')
  
    #Visualização de Serie Temporal (GI)
    #Maxima Mensal
      chuvas_dg_max= [go.Scatter(x=chuvas_dg.index, y=chuvas_dg['Maxima'] )]
      py.iplot(chuvas_dg_max, filename='chuvas_dg_max.html')
      #Dias de chuva
      chuvas_dg_dias= [go.Scatter(x=chuvas_dg.index, y=chuvas_dg['NumDiasDeChuva'] )]
      py.offline.plot(chuvas_dg_dias, filename='chuvas_dg_dias.html')
    
    #Gantt (GI)
    

#Exportando
  #Gráficos OK
  
  #Dados
    #Tabelas com missing values
    #Tabelas com dados interpolados
