# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 18:19:14 2022

@author: arias
"""
from lxml import html
import requests
from datetime import datetime
import pandas as pd
import os
import io
from fuzzywuzzy import fuzz
from sql import engine
import logging
import numpy as np
#%%
logging.basicConfig( level=logging.ERROR, filename='errores.log')

def save(file_name, records):
    """Funcion que realiza guardado del archivo,
    
    Returns:
        None
        archivo guardado segun ruta y los datos a guardar
    
    """
    check_dir(file_name)
    csv_file = open(file_name,'w', newline='', encoding='utf-8')
    csv_file.write(records)
    print(" record saved to ",file_name)
    csv_file.close()
    return  None

def check_dir(file_name):
    """Chequea si existe el directorio sino lo genera,
    
    Returns:
        Directorio
    
    """
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

def download(url, categoria):
    """genera una descargar segun url y guarda archivos segun nombre de la categoria
    
    Returns:
        Archivo segun nombre
    
    """
    response = requests.get(url)
    response.encoding='utf-8'
    
    año,mes,hoy_string=fecha()
    file= categoria + "/" + str(año) +'-'+ mes+ "/" + categoria+'-'+ hoy_string+ '.csv'
    save(file, response.text)# guarda datos segun el Path
    return file

def fecha():
    """
    calcula la fecha actual
    Returns:
        año
        mes
        hoy_string(format= dd-mm-yyyy)
        
    """
    hoy=datetime.now()
    año= hoy.year
    mes= meses[hoy.month]
    hoy_string=datetime.strftime(hoy, '%d-%m-%Y')
    return año,mes,hoy_string
        


# creacion de dict y listas necesarias
#Diccionario con los nombre de los meses
meses={1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio',7:'Julio', 8:'Agosto',9: 'Septiembre', 10:'Octubre', 11:'Noviembre', 12: 'Diciembre'}




#Se hace primer request de la pagina donde descargar los datasets
url='https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales'

page= requests.get(url)
extractedHtml = html.fromstring(page.content)


#%%

def obtener_dataframes():
    """ lista usada para definir a traves de XPath y pode descargar el link"""
    mat= [4,5,2]
    categorias=['museos', 'cine', 'bibliotecas']
    columns= ['Cod_Loc', 'IdProvincia', 'IdDepartamento', 
           'categoria', 'provincia', 'localidad', 'nombre',
           'direccion', 'CP', 'telefono', 'Mail', 'Web']
    df=pd.DataFrame(columns=columns)
    for i,v in enumerate(mat):
        
        link = extractedHtml.xpath(f'//*[@id="pkg-resources"]/div[{v}]/div/a[2]/@href')
        page1= requests.get(link[0])
        page1.encoding='utf-8'
        download(link[0],categorias[i])
        
        data =pd.read_csv(io.StringIO(page1.text))
        if categorias[i]=='cine':
            df_cine=data
        for column_df in data.columns:
            for column in columns:
                a=fuzz.WRatio(column,column_df)
                if a>92:
                    data.rename(columns={column_df:column}, inplace=True)
        if 'Domicilio' in data.columns:
            
            data.rename(columns={'Domicilio':'direccion'}, inplace=True)
        df=pd.concat([df,data[columns]])
    return df_cine, df
    
       


#corre la funcion para obtener los dos dataframes
df_cine,df=obtener_dataframes() 

# carga de Dataframe a base de datos
df.to_sql('tbl_data', con=engine, if_exists='replace')
df_cine.to_sql('tbl_cine', con=engine, if_exists='replace')   


#%%
posible={'si':1, 'SI':1, 'Si':1, 'Sí':1, 'no':0, 'No':0, '0':0}
df_cine.espacio_INCAA.replace(posible, inplace=True)

df_resumen_cine=df_cine.pivot_table(index='provincia', values=[ 'Pantallas', 'Butacas', 'espacio_INCAA'],aggfunc=np.sum)

df_resumen_cine.to_sql('tbl_resumen_cine', con=engine, if_exists='replace')

#%%
# sql_file=open("create.sql")    
# sql_string= sql_file.read()
# a=engine.execute(sql_string)
#%%
#Calculos de 
serie_cat=df.groupby(['categoria']).size()
serie_pro_cat=df.groupby(['provincia','categoria']).size()