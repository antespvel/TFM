# -*- coding: utf-8  -*-

from twitter import * 
import csv
import os    
from time import sleep
import atexit
import sys
import pandas as pd

def exit_handler():
    global tuits
    print('Writing','tuits-'+query+'.csv')
    fieldnames = set()
    for tuit in tuits:
        fieldnames|=set(tuit.keys())
    with open('/home/anton/Escritorio/FIN/EVALUACION/TUITS_UNIGRAMAS/tuits-'+query.replace('"','')+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(fieldnames))
        writer.writeheader();
        for tuit in tuits:
            tuit['text'] = tuit['text'].replace('\n',' ')
            writer.writerow(tuit)

atexit.register(exit_handler)

with open("/home/anton/Escritorio/FIN/EVALUACION/rankingUnigramas.txt", encoding='utf-8') as f:
    queries = [w.split(',')[0] for w in f]

    remove = ['éxtasis', 'extasis', 'ketamina', 'marihuana', 'mdma', 'codeína', 'anfetamina', 'droga',
              'marihuana.', 'lsd', 'nicotina', 'cocaína', 'cocaina', 'metanfetamina', 'clonazepam',
              'alcohol', 'cannabis', 'delirio', 'mariguana', 'placer', 'drogas', 'hachís', 'dolor',
              'cafeína', 'supositorios', 'adrenalina', 'antidepresivos', 'viagra', 'locura', 'cigarrillo',
              'sobredosis', 'pomada', 'frenesí', 'metanfetaminas', 'amoxicilina', 'cigarro', 'abstinencia',
              'orgasmo', 'esteroides']

    for w in remove:
        queries.remove(w)

print(queries)
tuits = []

def search(query):
    global tuits
    CONSUMER_KEY = "CebtHWOANtRCNGzON7YqlwgQr"
    CONSUMER_SECRET = "4YsNGOtCOJPQ0B7paBA2ylVzpSQUiPNFBnO8IdJCGEn1iozwbH"
    MY_TWITTER_CREDS = './my_app_credentials'
    if not os.path.exists(MY_TWITTER_CREDS):
        oauth_dance("UnusualBehaviorSearch", CONSUMER_KEY, CONSUMER_SECRET,
                    MY_TWITTER_CREDS)

    oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

    print('Buscando '+query)
    twitter_search = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))


    page = twitter_search.search.tweets(q=query+' -filter:retweets',lang='es', count=100, result_type='recent')["statuses"]
    maxId = -1
    while len(tuits)<50000:
        tuits += page
        if len(page)==0 or maxId == page[-1]["id"]:
            break
        maxId = page[-1]["id"]
        print(len(tuits), ' tuits... maxId:', maxId)
        page = None
        retry = 0
        while not page:
            retry+=1
            if retry==20:
                print("Abortando la búsqueda de "+query)
                break;
            try:
                page = twitter_search.search.tweets(q=query+' -filter:retweets',lang='es',count=100, max_id=maxId, result_type='recent')["statuses"]
            except:
                print('Error:', sys.exc_info()[0])
                print("Esperando 120 segundos para repetir la consulta...")
                exit_handler()
                sleep(120) # Time in seconds.
		
    print('TOTAL: ',len(tuits),' tuits.')
    fieldnames = set()
    for tuit in tuits:
        fieldnames|=set(tuit.keys())

    with open('/home/anton/Escritorio/FIN/EVALUACION/TUITS_UNIGRAMAS/tuits-'+query.replace('"','')+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(fieldnames))
        writer.writeheader();
        for tuit in tuits:
            tuit['text'] = tuit['text'].replace('\n',' ')
            writer.writerow(tuit)

for query in queries:
    tuits = []
    search(query.replace('_', ' '))

