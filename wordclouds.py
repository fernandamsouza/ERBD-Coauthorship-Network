import numpy as np
import pandas as pd
import os
import sys
import glob
import re
from pathlib import Path
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
FILE_DIR = Path(__file__).parent

def getWordcloud():
    # geração da árvore de palavras para titulo de publicações
    df_publicacoes = pd.read_csv('./data/publicacoes_tudo/tudo_all.csv')
    df_publicacoes.dropna(subset=['TITULO'], axis=0, inplace = True)
    titulo = df_publicacoes['TITULO']
    all_titulo = " ".join(s for s in titulo)
    stopwords = set(STOPWORDS)
    # -- Falta atualizar stopwords --
    stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "para", "an"])
    wordcloud = WordCloud(stopwords=stopwords,
                      background_color='black', width=1600,                            
                      height=800).generate(all_titulo)
    fig, ax = plt.subplots(figsize=(16,8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file('wordcloud-ti.png')
    print('Nuvem de palavras para titulo de publicacoes gerada com sucesso.')
    print('------------------')

    # geração da árvore de palavras para titulo de evento/journal
    df_evenjour = pd.read_csv('./data/publicacoes_tudo/tudo_all.csv')
    df_evenjour.dropna(subset=['EVENTO/JOURNAL'], axis=0, inplace = True)
    ej = df_evenjour['EVENTO/JOURNAL']
    all_ej = " ".join(s for s in ej)
    stopwords = set(STOPWORDS)
    # -- Falta atualizar stopwords --
    stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "para", "an", "of", "do", "on", "Proceedings", "Conference", "anais", "Anais"
    , "Proceedings of", "Anais do", "Conference on"])
    wordcloud = WordCloud(stopwords=stopwords,
                      background_color='black', width=1600,                            
                      height=800).generate(all_ej)
    fig, ax = plt.subplots(figsize=(16,8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file('wordcloud-ej.png')
    print('Nuvem de palavras para titulo de evento/journal gerada com sucesso.')
    print('------------------')

    # geração da árvore de palavras para titulo de universidades
    df_universidades = pd.read_csv('./data/atuacoes/atuacoes_juncao/atuacoes_all.csv')
    df_universidades.dropna(subset=['INSTITUICAO/EMPRESA'], axis=0, inplace = True)
    instituicao = df_universidades['INSTITUICAO/EMPRESA']
    all_instituicao = " ".join(s for s in instituicao)
    stopwords = set(STOPWORDS)
    # -- Falta atualizar stopwords --
    stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "para", "an", "of", "do", "on", "Proceedings", "Conference", "anais", "Anais"
    , "Proceedings of", "Anais do", "Conference on"])
    wordcloud = WordCloud(stopwords=stopwords,
                      background_color='black', width=1600,                            
                      height=800).generate(all_instituicao)
    fig, ax = plt.subplots(figsize=(16,8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    plt.imshow(wordcloud)
    wordcloud.to_file('wordcloud-instituicao.png')
    print('Nuvem de palavras para nome de universidades gerada com sucesso.')
    print('------------------')