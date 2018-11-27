import csv
from nltk import DefaultTagger, UnigramTagger, BigramTagger, word_tokenize
from nltk.probability import FreqDist
from nltk import word_tokenize
from nltk.util import ngrams
from nltk import bigrams
from nltk.tag.stanford import StanfordPOSTagger
import atexit

spanish_postagger = StanfordPOSTagger('/home/anton/Escritorio/TAGGER/stanford/models/spanish-distsim.tagger',
                                       '/home/anton/Escritorio/TAGGER/stanford/stanford-postagger.jar')

def exit_handler(unigramas, bigramas, trigramas, conteo):
    fileUnigramas = open('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasUnigramas.txt', 'w')
    escribirEnFichero(fileUnigramas, list(filter(lambda x: x[1] > 1, FreqDist(unigramas).most_common(len(unigramas)))))
    fileBigramas = open('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasBigramas.txt', 'w')
    escribirEnFichero(fileBigramas, list(filter(lambda x: x[1] > 1, FreqDist(unirNGramas(bigramas)).most_common(len(bigramas)))))
    fileTrigramas = open('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasTrigramas.txt', 'w')
    escribirEnFichero(fileTrigramas, list(filter(lambda x: x[1] > 1, FreqDist(unirNGramas(trigramas)).most_common(len(trigramas)))))

    print("Analizados " + str(conteo) + " tuits")

atexit.register(exit_handler)

def filtra_puntuacion(palabras):
    return [w for w in palabras if any(c.isalpha() or c.isdigit() for c in w)]

def extraeNGramas(texto):
    tagged = spanish_postagger.tag(filtra_puntuacion(word_tokenize(texto.lower())))

    unigramas = ngrams(tagged, 1)
    unigramasFiltro = [unigrama[0][0] for unigrama in unigramas if
                       unigrama[0][1].startswith('n')
                       or unigrama[0][1].startswith('a')
                       or unigrama[0][1].startswith('v')]

    bigramas = ngrams(tagged, 2)
    bigramasFiltro = [bigrama[0][0] + " " + bigrama[1][0] for bigrama in bigramas if
                      (bigrama[0][1].startswith('a') and bigrama[1][1].startswith('n'))
                      or (bigrama[0][1].startswith('n') and bigrama[1][1].startswith('a'))
                      or (bigrama[0][1].startswith('v') and bigrama[1][1].startswith('n'))
                      or (bigrama[0][1].startswith('v') and bigrama[1][1].startswith('r'))]

    trigramas = ngrams(tagged, 3)
    trigramasFiltro = [trigrama[0][0] + " " + trigrama[1][0] + " " + trigrama[2][0] for trigrama in trigramas if
                       (trigrama[0][1].startswith('n') and trigrama[1][1].startswith('sp') and trigrama[2][
                           1].startswith('n'))]

    return unigramasFiltro, bigramasFiltro, trigramasFiltro

def unirNGramas(gramas):
    lista = list()
    filtro = ('_', '+', ')', '&', '`', '-')
    for document in gramas:
        if all(s not in document for s in filtro):
            lista.append("_".join(palabra for palabra in document.split()))
    return lista

def escribirEnFichero(fichero, lista):
    for t in lista:
        fichero.write(t[0]+", "+str(t[1])+"\n")

def main(fichero):
    unigramas = []
    bigramas = []
    trigtamas = []
    conteo = 0
    with open(fichero, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        print('Comenzamos la extracción de ngramas')
        for registro in lector:
            try:
                u,b,t = extraeNGramas(registro['text'].lower())
                unigramas.extend(u)
                bigramas.extend(b)
                trigtamas.extend(t)
                conteo += 1
                if (conteo % 10 == 0):
                    print('Llevamos ' + str(conteo) + ' tuits')
            except:
                print("Error por parada")
                exit_handler(unigramas, bigramas, trigtamas, conteo)

    fileUnigramas = open('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasUnigramas.txt', 'w')
    escribirEnFichero(fileUnigramas, list(filter(lambda x: x[1] > 1, FreqDist(unigramas).most_common(len(unigramas)))))
    fileBigramas = open('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasBigramas.txt', 'w')
    escribirEnFichero(fileBigramas, list(filter(lambda x: x[1] > 1, FreqDist(unirNGramas(bigramas)).most_common(len(bigramas)))))
    fileTrigramas = open('/home/anton/Escritorio/FIN/CONTEOS/conteosDrogasTrigramas.txt', 'w')
    escribirEnFichero(fileTrigramas, list(filter(lambda x: x[1] > 1, FreqDist(unirNGramas(trigtamas)).most_common(len(trigtamas)))))

main('/home/anton/Escritorio/FIN/CORPUS/tuits_drogas_RT_EN.csv')