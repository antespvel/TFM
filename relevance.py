import pandas as pd
import math
import csv
import numpy as np
from nltk import word_tokenize

def relevance():
    # Cargamos las frecuencias de las drogas
    drogas = pd.read_csv('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasTrigramas.txt', sep=",", header=None)
    drogas.columns = ["Palabra", "Frecuencia"]
    print('***Se han cargado las frecuencias de drogas***')

    # Cargamos las frecuencias de control
    control = pd.read_csv('/home/anton/Escritorio/FIN/CONTEOS/conteosControlTrigramas.txt', sep=",", header=None)
    control.columns = ["Palabra", "Frecuencia"]
    print('***Se han cargado las frecuencias de crontol***')

    # Añadimos los ngramas de drogas que no aparecen en control en control
    aux = drogas.merge(control, on=['Palabra'])
    aux = drogas[(~drogas.Palabra.isin(aux.Palabra))]
    aux['Frecuencia'] = 1
    control['Frecuencia'] = control['Frecuencia'] + 1
    drogas['Frecuencia'] = drogas['Frecuencia'] + 1
    control = pd.concat([control, aux], ignore_index=True)


    # Calculamos el numero total de palabras de cada corpus
    nDrogas = drogas['Frecuencia'].sum()
    nControl = control['Frecuencia'].sum()

    # Calculamos el numero de documentos en los que aparece cada termino de drogas
    documentsByWord = []
    k = 0
    for i, droga in drogas.iterrows():
        if(len(droga['Palabra'].split('_'))>1):
            droga['Palabra'] = droga['Palabra'].replace('_', ' ')

        with open('/home/anton/Escritorio/FIN/CORPUS/tuits_drogas_RT_EN.csv', newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            contador = 0
            for registro in lector:
                if(droga['Palabra'] in registro['text'].lower()):
                    contador += 1
        documentsByWord.append(contador)
        f.close()
        k += 1
        if (k%10==0):
            print("Levamos "+ str(k)+" terminos")


    nDocuments = pd.DataFrame(documentsByWord)
    drogas['nDocuments'] = nDocuments[0]
    drogas['nDocuments'].round(0).astype(int)

    # Se calcula el relevance del corpus de drogas respecto al de control
    df = pd.merge(drogas, control, on=['Palabra'])
    print('***Se han unido ambas frecuencias***')
    df['aux'] = 2+((df['Frecuencia_x']/nDrogas)*df['nDocuments'])/(df['Frecuencia_y']/nControl)
    df['relevance'] = 1 - (np.log2(df.aux))**-1
    del df['Frecuencia_x']
    del df['Frecuencia_y']
    del df['nDocuments']
    del df['aux']
    df.sort_values('relevance', inplace=True, ascending=False)

    df.to_csv('/home/anton/Escritorio/FIN/RELEVANCE/relevanceTrigramas.txt', index=False, sep=',', header=None)


relevance()