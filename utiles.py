
def escribirEnFichero(fichero, lista):
    for t in lista:
        fichero.write(t.split(',')[0]+", "+t.split(',')[1]+"\n")

def filtrarGramasEnglobados():

    with open('/home/anton/Escritorio/FIN/EVALUACION/rankingUnigramas.txt') as f:
        u = [line.strip() for line in f]

    with open('/home/anton/Escritorio/FIN/RANKING/rankingBigramas.txt') as f:
        b = [line.strip() for line in f]

    with open('/home/anton/Escritorio/FIN/RANKING/rankingTrigramas.txt') as f:
        t = [line.strip() for line in f]

    bigramas = list(set([w for w in b if all(x.split(',')[0] not in w.split(',')[0] for x in u)]))
    bigramas.sort(key=lambda u: u.split(',')[1], reverse=True)

    trigramas = list(set([w for w in t if all(x.split(',')[0] not in w.split(',')[0] for x in u)]))
    trigramas.sort(key=lambda u: u.split(',')[1], reverse=True)

    fileBigramas = open('/home/anton/Escritorio/FIN/EVALUACION/rankingBigramas.txt', 'w')
    escribirEnFichero(fileBigramas, bigramas)

    fileTrigramas = open('/home/anton/Escritorio/FIN/EVALUACION/rankingTrigramas.txt', 'w')
    escribirEnFichero(fileTrigramas, trigramas)


filtrarGramasEnglobados()