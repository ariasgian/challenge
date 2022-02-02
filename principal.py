# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 18:19:14 2022

@author: arias
"""
from lxml import html
import requests
from datetime import datetime

import csv
import os

#Funcion que realiza guardado del archivo
def save(file_name, records):
    """Retorna None,
    
    Returns:
        None
        archivo guardado segun ruta y los datos a guardar
    
    """
    check_dir(file_name)
    csv_file = open(file_name,'a', newline='')
    csvWriter = csv.writer(csv_file,delimiter=',')
    for record in records:
        csvWriter.writerow(record.decode('utf-8').split(','))
    print(" record saved to ",file_name)
    csv_file.close()
    return  None

# Funcion que chequea si existe el directory y si no existe lo crea
def check_dir(file_name):
    """Chequea si existe el directorio sino lo genera,
    
    Returns:
        Directorio
    
    """
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)


#Recibe la repuesta del request y pide guardar el csv
def download(url, categoria):
    """genera una descargar segun url y guarda archivos segun nombre de la categoria
    
    Returns:
        Archivo segun nombre
    
    """
    response = requests.get(url)
    año,mes,hoy_string=fecha()
    path= categoria + "/" + str(año) +'-'+ mes+ "/" + categoria+ hoy_string+ '.csv'
    save(path, response.iter_lines())# guarda datos segun el Path


#Obtener la fecha en el formato dd-mm-yyyy
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
    hoy_string='-'+datetime.strftime(hoy, '%d-%m-%Y')
    return año,mes,hoy_string
        


# creacion de dict y listas necesarias
#Diccionario con los nombre de los meses
meses={1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio',7:'Julio', 8:'Agosto',9: 'Septiembre', 10:'Octubre', 11:'Noviembre', 12: 'Diciembre'}

# lista usada para definir a traves de XPath y pode descargar el link
mat= [4,5,2]
categorias=['museos', 'cine', 'bibliotecas']


#Se hace primer request de la pagina donde descargar los datasets
url='https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales'
page= requests.get(url)


#se hace un para descargar las 3 categorias 
for i,v in enumerate(mat):
    extractedHtml = html.fromstring(page.content)
    link = extractedHtml.xpath(f'//*[@id="pkg-resources"]/div[{v}]/div/a[2]/@href')
    download(link[0],categorias[i])
    
#sadadad









