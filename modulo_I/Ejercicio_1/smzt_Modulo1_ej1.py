#!/usr/bin/python
import argparse
import json
import re
import sys

def calcular_sentimiento(texto_un_tweet, valores):
    valor_sentimiento = 0
    for palabras,puntuacion in valores.items():
        if bool(re.search(re.compile(r'\b'+palabras.lower()+r'\b'), texto_un_tweet.lower())):
            valor_sentimiento += puntuacion
    return valor_sentimiento


def main(argumentos):
    sentimientos = open(argumentos.sentimientos,'r')
    print "Tweet_ID\tSentimiento"
    valores = {}
    for linea in sentimientos:
        termino, valor = linea.split("\t")
        valores[termino] = int(valor)

    for line in open(argumentos.tweets, 'r'):
        one_tweet = json.loads(line)
        if "text" in one_tweet:
            print str(one_tweet['id']) +"\t"+ str(calcular_sentimiento(one_tweet['text'].encode('utf-8').strip(),valores))
    sentimientos.close()

parser = argparse.ArgumentParser(description='Este programa muestra pantalla un valor numerico en cada linea que '
                                             'representa el sentimiento de un tweet')
parser.add_argument('--sentimientos', dest='sentimientos', action='store',
                    help='ruta completa al fichero de sentimientos')
parser.add_argument('--tweets', dest='tweets', action='store',
                    help='ruta completa al fichero de tweets')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
argumentos = parser.parse_args()
main(argumentos)
