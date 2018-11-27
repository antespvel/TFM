import gensim

w2v = gensim.models.KeyedVectors.load_word2vec_format("/home/anton/Escritorio/PRUEBA/UTILES/twitter.txt.bin", binary=True)

SEMILLAS = ['éxtasis',
	'extasis',
	'ketamina',
	'marihuana']

def similitud_semillas(palabra):
    similitudes = []
    for semilla in SEMILLAS:
        if palabra in w2v:
            similitud = w2v.similarity(palabra, semilla)
        else:
            similitud = 0
        similitudes.append(similitud)
    return sum(similitudes)/len(similitudes), max(similitudes)

# Mira similitud w2v entre semillas y cada unigrama, y utiliza la media y el máximo para
# recalcular la relevancia (se multiplican todos, ya que están en escala 0-1)
# Se reordena el ranking con esta nueva medida

print('****UNIGRAMAS*****')

with open("/home/anton/Escritorio/FIN/RELEVANCE/relevanceUnigramas.txt", encoding='utf-8') as f:
    info = [linea.split(",") for linea in f]
    unigramas_relevance = {u[0]:float(u[1]) for u in info}
    unigramas_ranking = []
    for palabra in unigramas_relevance:
        if(len(palabra) > 2):
            similitud = similitud_semillas(palabra)
            unigramas_ranking.append((palabra,similitud[1]*similitud[0]*unigramas_relevance[palabra]))
    unigramas_ranking.sort(key=lambda u:u[1], reverse=True)

    with open('/home/anton/Escritorio/FIN/RANKING/rankingUnigramas.txt', 'w') as f:
        for palabra, score in unigramas_ranking:
            f.write(palabra+"," + str(score)+'\n'   )

# Mira similitud w2v entre semillas y cada palabra de cada bigrama, y utiliza
# el máximo de la similitud media y de la similitud máxima de entre las palabras
# del bigrama para recalcular la relevancia (se multiplican todos,
# ya que están en escala 0-1)
# Se reordena el ranking con esta nueva medida

print('*****BIGRAMAS*****')

with open("/home/anton/Escritorio/FIN/RELEVANCE/relevanceBigramas.txt", encoding='utf-8') as f:
    info = [linea.split(",") for linea in f]
    bigramas_relevance = {u[0]:float(u[1]) for u in info}
    bigramas_ranking = []
    for bigrama in bigramas_relevance:
        similitudes = [similitud_semillas(palabra) for palabra in bigrama.split("_")]
        media_max = max([media for media,_ in similitudes])
        max_max = max([max for _,max in similitudes])
        bigramas_ranking.append((bigrama,media_max*max_max*bigramas_relevance[bigrama]))
    bigramas_ranking.sort(key=lambda u:u[1], reverse=True)

    with open('/home/anton/Escritorio/FIN/RANKING/rankingBigramas.txt', 'w') as f:
        for bigrama, score in bigramas_ranking:
            f.write(bigrama+","+ str(score)+'\n')

# Mira similitud w2v entre semillas y cada palabra de cada trigrama, y utiliza
# el máximo de la similitud media y de la similitud máxima de entre las palabras
# del trigrama para recalcular la relevancia (se multiplican todos,
# ya que están en escala 0-1)
# Se reordena el ranking con esta nueva medida

print('*****TRIGRAMAS*****')

with open("/home/anton/Escritorio/FIN/RELEVANCE/relevanceTrigramas.txt", encoding='utf-8') as f:
    info = [linea.split(",") for linea in f]
    trigramas_relevance = {u[0]:float(u[1]) for u in info}
    trigramas_ranking = []
    for trigrama in trigramas_relevance:
        similitudes = [similitud_semillas(palabra) for palabra in trigrama.split("_")]
        media_max = max([media for media,_ in similitudes])
        max_max = max([max for _,max in similitudes])
        trigramas_ranking.append((trigrama,media_max*max_max*trigramas_relevance[trigrama]))
    trigramas_ranking.sort(key=lambda u:u[1], reverse=True)

    with open('/home/anton/Escritorio/FIN/RANKING/rankingTrigramas.txt', 'w') as f:
        for trigrama, score in trigramas_ranking:
            f.write(trigrama+"," +str(score)+'\n')