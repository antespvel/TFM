import glob
import csv
import ast

def filtraRT(path):

    files = glob.glob(path+"*.csv")

    for file in files:
        try:
            with open(file, newline='', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                drogas = []
                for registro in lector:
                    created = registro['created_at']
                    id = registro['id']
                    text = registro['text']
                    enlaces = 'http' in registro['text']
                    drogas.append((id, created, text, enlaces))

            drogasReducido = [[id, cr, te] for id, cr, te, en in drogas if not en]

            name = file.split('/')[-1]

            with open(path+'Filtrados/'+name, 'w') as archivo:
                cabeceras = ['id', 'created_at', 'text']
                writer = csv.writer(archivo)
                drogasReducido.insert(0, cabeceras)
                writer.writerows(drogasReducido)

            print('Filtrados los retweets de '+ name)

        except Exception as e:
            print(' Fallo al procesar ' + file)
            print(e)


filtraRT('/home/anton/Escritorio/FIN/EVALUACION/TUITS_UNIGRAMAS/')
