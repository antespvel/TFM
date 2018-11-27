import csv

with open('/home/anton/Escritorio/Datos/Crudo/drogas.csv', newline='', encoding='utf-8') as f:
    lector = csv.DictReader(f)
    drogas = []

    for registro in lector:
            created = registro['created_at']
            id = registro['id']
            text = registro['text']
            retweet = registro['retweeted_status'] != ''
            enlaces = 'http' in registro['text']
            filtro = 'marihuana' in text or 'ketamina' in text or 'extasis' in text or 'éxtasis' in text
            drogas.append((id,created,text, retweet, enlaces, filtro))

print('Cargados', len(drogas), 'tuits.')

drogasReducido = [[cr, id, te] for cr,id,te,re,en,fil in drogas if fil and not re and not en]

with open('/home/anton/Escritorio/FIN/CORPUS/tuits_drogas_RT_EN.csv', 'w') as archivo:
    cabeceras = ['created_at', 'id', 'text']
    writer = csv.writer(archivo)
    drogasReducido.insert(0, cabeceras)
    writer.writerows(drogasReducido)
