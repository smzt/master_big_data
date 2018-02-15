#!/usr/bin/python
import argparse
import json
import re, string
import numpy as np

def sentimiento_tweet(texto_un_tweet, valores):
    valor_sentimiento = []
    #posicion_palabras_exiten = []
    palabras_no_lista=texto_un_tweet.lower()
    for palabras,puntuacion in valores.items():
        if bool(re.search(re.compile(r'\b'+palabras.lower()+r'\b'), texto_un_tweet.lower())):
            valor_sentimiento.append(puntuacion)
            #inicio_palabra=re.search(re.compile(r'\b' + palabras.lower() + r'\b'), texto_un_tweet.lower()).start()
            #final_palabra=re.search(re.compile(r'\b' + palabras.lower() + r'\b'), texto_un_tweet.lower()).end()
            #posicion_palabras_exiten.append(str(inicio_palabra)+"-"+str(final_palabra))
            palabras_no_lista=palabras_no_lista.replace(palabras,"")
    #lista_nuevos_sentimiento=nuevos_sentimientos(posicion_palabras_exiten,texto_un_tweet.lower())
    return np.median(valor_sentimiento), palabras_no_lista

def nuevos_sentimientos(posicion_palabras_existen, texto_un_tweet):
    for posicion in posicion_palabras_existen:
        pass
        #texto_un_tweet[]



def main(argumentos):
    sentimientos = open(argumentos.sentimientos,'r')
    print "Palabra\tValor_medio_sentimiento"
    valores = {}
    for linea in sentimientos:
        termino, valor = linea.split("\t")
        valores[termino] = int(valor)

    for line in open(argumentos.tweets, 'r'):
        one_tweet = json.loads(line)
        if "text" in one_tweet:
            #print str(one_tweet['id']) +"\t"+ str(sentimiento_tweet(one_tweet['text'].encode('utf-8').strip(),valores))
            valor_sentimiento_tweet=sentimiento_tweet(one_tweet['text'].encode('utf-8').strip(),valores)
            for palabra in re.split(r'\s+',valor_sentimiento_tweet[1]):
                print palabra.replace(';','').replace(':','').replace('\.','').replace(' ','') +"\t"+ str(valor_sentimiento_tweet[0])


    sentimientos.close()

parser = argparse.ArgumentParser(description='Este programa muestra por pantalla en cada linea, una palabra o '
                                             'conjunto de palabras y a continuacion un valor numerico que represente el '
                                             'sentimiento de dicha palabra o conjunto de palabras. Solo se muestra la '
                                             'palabra o conjunto de palabras que no aparecen con un valor en el '
                                             'archivo original')
parser.add_argument('--sentimientos', dest='sentimientos', action='store',
                    help='ruta completa al fichero de sentimientos')
parser.add_argument('--tweets', dest='tweets', action='store',
                    help='ruta completa al fichero de tweets')

argumentos = parser.parse_args()
main(argumentos)
