#!/usr/bin/python
import argparse, json, re, string, sys
from numpy import median


def sentimiento_tweet(texto_un_tweet, valores):
    valor_sentimiento = []
    palabras_existen = []
    palabras_existen = []
    nuevo_texto = []
    formateo_caracteres = set(string.letters)
    formateo_caracteres.update(['\'', '/'])
    for trozo in texto_un_tweet.split(' '):
        trozo = filter(lambda x: x in formateo_caracteres, trozo)
        nuevo_texto.append(trozo)
    eliminar_palabras_existen = ' '.join(nuevo_texto)
    for palabras, puntuacion in valores.items():
        if bool(re.search(re.compile(r'\b' + palabras + r'\b'), texto_un_tweet)):
            valor_sentimiento.append(puntuacion)
            palabras_existen.append(palabras)
    if len(valor_sentimiento) > 0:
        for palabra in palabras_existen:
            eliminar_palabras_existen = (re.sub(r'\b' + palabra + r'\b', r'', eliminar_palabras_existen))
        if len(valor_sentimiento) == 1:
            return valor_sentimiento[0], eliminar_palabras_existen
        else:
            return median(valor_sentimiento), eliminar_palabras_existen


def palabras_unicas(palabras_todos_tweets):
    conjunto_palabras = []
    for unicas in palabras_todos_tweets:
        conjunto_palabras.append(unicas.split("\t")[0])
    palabras_unicas = list(set(conjunto_palabras))
    palabras_unicas.sort()
    for palabra in palabras_unicas:
        nuevo_valor = []
        # Solo dejo las palabras con mas de una letra y que no sean espacios vacios
        if palabra != '' and len(palabra) > 1:
            for palabra_nueva in palabras_todos_tweets:
                una_palabra, puntuacion = palabra_nueva.split("\t")
                if palabra == una_palabra:
                    nuevo_valor.append(float(puntuacion))
            if len(nuevo_valor) == 1:
                print palabra + "\t" + str(nuevo_valor[0])
            else:
                print palabra + "\t" + str(median(nuevo_valor))


def main(argumentos):
    sentimientos = open(argumentos.sentimientos, 'r')
    palabras_todos_tweets = []
    valores = {}
    for linea in sentimientos:
        termino, valor = linea.split("\t")
        valores[termino] = int(valor)

    for line in open(argumentos.tweets, 'r'):
        one_tweet = json.loads(line)
        if "text" in one_tweet:
            texto = one_tweet['text'].encode('utf_8').strip().lower()
            valor_sentimiento_tweet = sentimiento_tweet(texto, valores)
            if valor_sentimiento_tweet is not None:
                for palabra in re.split(r'\s', valor_sentimiento_tweet[1]):
                    palabras_todos_tweets.append(palabra + "\t" + str(valor_sentimiento_tweet[0]))

    sentimientos.close()
    palabras_unicas(palabras_todos_tweets)


parser = argparse.ArgumentParser(description='Este programa muestra por pantalla en cada linea, una palabra y a '
                                             'continuacion un valor numerico que represente el sentimiento de dicha '
                                             'palabra o conjunto de palabras. Solo se muestra la palabra o conjunto de '
                                             'palabras que no aparecen con un valor en el archivo original')
parser.add_argument('--sentimientos', dest='sentimientos', action='store',
                    help='ruta completa al fichero de sentimientos')
parser.add_argument('--tweets', dest='tweets', action='store',
                    help='ruta completa al fichero de tweets')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

argumentos = parser.parse_args()
main(argumentos)
