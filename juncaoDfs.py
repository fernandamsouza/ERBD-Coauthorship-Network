# This Python file uses the following encoding: utf-8
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import os
import sys
import glob
import re
import xlrd
import xlwt
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from pathlib import Path
import pandas_dedupe
import networkx as nx
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from pyexcel.cookbook import merge_all_to_a_book
import glob
FILE_DIR = Path(__file__).parent

caminho1 = (FILE_DIR/"../scraperXMLtoCSV/data/publicacoes_tudo/tudo_all.csv").resolve()
caminho4 = (FILE_DIR/"../scraperXMLtoCSV/Banco PostgreSQL/autores.csv").resolve()
caminho2 = (FILE_DIR/"../scraperXMLtoCSV/csv_producao/formacao_all.csv").resolve()
caminho3 = (FILE_DIR/"../scraperXMLtoCSV/csv_producao/teste.xlsx").resolve()
pathfilename2 = (FILE_DIR/"../scraperXMLtoCSV/Banco PostgreSQL/autoresartigo.csv").resolve()


def getJuncao():

    # ------------------------------------------------------------
    # Producao bibliografica
    # ------------------------------------------------------------
    # Parte para juntar todos os periódicos de todos os currículos.

    csv_periodicos = glob.glob('./data/periodicos/*artigoperiodico.csv') # Abertura de todos os periódicos de cada autor presente analisado (retorna uma lista)
    df_periodico = pd.DataFrame() # inicialização de um dataframe contando todos os periódicos
    for i in range(len(csv_periodicos)): # varrendo todos os csv individuais de cada autor analisado
        dataFrameAux = pd.read_csv(csv_periodicos[i], header=0) # cada csv_periodico será armazenado no dataFrame auxiliar
        df_periodico = df_periodico.append(dataFrameAux, ignore_index=False) # a partir do dataFrame auxiliar, os dados serão armazenadas no dataFrame do periódico

   # ------------------------------------------------------------
   # df com todos os trabalhos de eventos
   # Parte para juntar todos os trabalhos de eventos de todos os currículos, a mesma técnica utilizada para juntar os periódicos, foi utilizada aqui.

    csv_eventos = glob.glob('./data/trabeventos/*trabalhoeventos.csv')
    df_trabevento = pd.DataFrame()
    for i in range(len(csv_eventos)):
        dataFrameAux = pd.read_csv(csv_eventos[i], header=0)
        df_trabevento = df_trabevento.append(dataFrameAux, ignore_index=False)

    # ------------------------------------------------------------
    # Formação
    # ------------------------------------------------------------
    # Parte para juntar todas as formações de todos os currículos, a mesma técnica utilizada para juntar os periódicos, foi utilizada aqui.

    csv_formacao = glob.glob('./data/formacao/*formacao.csv')
    df_formacao = pd.DataFrame()
    for i in range(len(csv_formacao)):
        dataFrameAux = pd.read_csv(csv_formacao[i], header=0)
        df_formacao = df_formacao.append(dataFrameAux, ignore_index=False)
    pathfilename = str('./data/formacao/formacao_juncao/formacao_all.csv')
    df_formacao.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Afiliação
    # ------------------------------------------------------------
    # Parte para juntar todas as afiliações de todos os currículos

    csv_afiliacao = glob.glob('./data/afiliacao/*afiliacao.csv')
    df_afiliacao = pd.DataFrame()
    for i in range(len(csv_afiliacao)):
        dataFrameAux = pd.read_csv(csv_afiliacao[i], header=0)
        df_afiliacao = df_afiliacao.append(dataFrameAux, ignore_index=False)
    pathfilename = str('./data/afiliacao/afiliacao_juncao/afiliacoes_all.csv')
    df_afiliacao.to_csv(pathfilename, index=False)

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Nomes
    # ------------------------------------------------------------
    # Parte para juntar todos os nomes de pesquisadores

    csv_nome = glob.glob('./data/autores/*fullname.csv')
    df_nome = pd.DataFrame()
    for i in range(len(csv_nome)):
        dataFrameAux = pd.read_csv(csv_nome[i], header=0)
        df_nome = df_nome.append(dataFrameAux, ignore_index=False)
    pathfilename = str('./data/autores/autores_juncao/fullname_all.csv')
    df_nome.to_csv(pathfilename, index=False)

    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Atuação profissional
    # ------------------------------------------------------------

    csv_atuacao = glob.glob('./data/atuacoes/*atuacoes.csv')
    df_atuacao = pd.DataFrame()
    for i in range(len(csv_atuacao)):
        dataFrameAux = pd.read_csv(csv_atuacao[i], header=0)
        df_atuacao = df_atuacao.append(dataFrameAux, ignore_index=False)
    pathfilename = str('./data/atuacoes/atuacoes_juncao/atuacoes_all.csv')
    df_atuacao.to_csv(pathfilename, index=False)

    # ------------------------------------------------------------
    # Producao bibliografica CAPITULOS
    # ------------------------------------------------------------

    csv_capitulo_livro = glob.glob('./data/capitulos/*capitulo.csv')
    df_chapter = pd.DataFrame()
    for i in range(len(csv_capitulo_livro)):
        dataFrameAux = pd.read_csv(csv_capitulo_livro[i], header=0)
        df_chapter = df_chapter.append(dataFrameAux, ignore_index=False)
    pathfilename = str('./data/capitulos/capitulos_juncao/capitulos_all.csv')
    df_chapter.to_csv(pathfilename, index=False)

    # ------------------------------------------------------------
    # Capítulo de livro, periodico e trabalho em evento -> juncao
    # ------------------------------------------------------------

    pathfilename = str('./data/publicacoes_tudo/tudo_all.csv')
    frames = [df_periodico, df_trabevento, df_chapter]
    dffinal = pd.concat (frames)
    dffinal.to_csv(pathfilename, index=False)

    # Juntar pro bd
    df_tudo =  pd.read_csv(caminho1)
    df_nome =  pd.read_csv(caminho4)
    dftrabevento = pd.merge(df_tudo, df_nome, on='ID_LATTES')
    dftrabevento.to_csv(pathfilename2, index=False)

    # Planilha linha do tempo (titulação)
    # ------------------------------------------------------------
    # df_tudo =  pd.read_csv(caminho1)
    # df_formacao =  pd.read_csv(caminho2)
    # dftrabevento = pd.merge(df_tudo, df_formacao, on='ID')
    # pathfilename = str('./csv_producao/teste.csv')
    # dftrabevento.to_csv(pathfilename, index=False)
    # dftrabevento = pd.read_csv(pathfilename)
    # merge_all_to_a_book(glob.glob("csv_producao/teste.csv"), "csv_producao/teste.xlsx")
    # wb = xlrd.open_workbook(caminho3, on_demand = True, encoding_override='cp1252')
    # sheet = wb.sheet_by_index(0)

    # workbook = copy(wb)
    # sheet2 = workbook.get_sheet(0)

    # for row in range(1, sheet.nrows):
    #     if sheet.cell_value(row, 3) != 'VAZIO':
    #         if sheet.cell_value(row, 17) == 'SIM':
    #             if sheet.cell_value(row,3) > sheet.cell_value(row,20) and sheet.cell_value(row,3) < sheet.cell_value(row,21):
    #                 print('graduando')
    #                 sheet2.write(row, 37, 'GRADUANDO')
    #         if sheet.cell_value(row, 24) == 'SIM':
    #             if sheet.cell_value(row,3) > sheet.cell_value(row,28) and sheet.cell_value(row,3) <= sheet.cell_value(row,29):
    #                 print('mestrando')
    #                 sheet2.write(row, 37, 'MESTRANDO')
    #         if sheet.cell_value(row, 30) == 'SIM':
    #             if float(sheet.cell_value(row,3)) >= float(sheet.cell_value(row,35)) and float(sheet.cell_value(row,3)) <= float(sheet.cell_value(row,36)) :
    #                 print('doutorando')
    #                 sheet2.write(row, 37, 'DOUTORANDO')
    #         if sheet.cell_value(row, 30) == 'SIM':
    #             if sheet.cell_value(row,3) >= sheet.cell_value(row,36):
    #                 print('doutor')
    #                 sheet2.write(row, 37, 'DOUTOR')

    # workbook.save(caminho3)
    # wb.release_resources()
    # del wb

    # wb = xlrd.open_workbook(caminho3, on_demand = True, encoding_override='cp1252')
    # sheet = wb.sheet_by_index(0)

    # workbook = copy(wb)
    # sheet2 = workbook.get_sheet(0)
    # for row in range(1, sheet.nrows):
    #         if sheet.cell_value(row, 37) == '':
    #             print('mestre')
    #             sheet2.write(row, 37, 'MESTRE')
    # workbook.save(caminho3)
    # wb.release_resources()
    # del wb

    # wb = xlrd.open_workbook(caminho3, on_demand = True, encoding_override='cp1252')
    # sheet = wb.sheet_by_index(0)

    # workbook = copy(wb)
    # sheet2 = workbook.get_sheet(0)

    # for row in range(1, sheet.nrows):
    #     if sheet.cell_value(row, 37) == 'DOUTOR' or 'DOUTORANDO':
    #         sheet2.write(row, 38, sheet.cell_value(row, 31))
    #     if sheet.cell_value(row, 37) == 'MESTRANDO' or 'MESTRE':
    #         sheet2.write(row, 38, sheet.cell_value(row, 25))
    #     if sheet.cell_value(row, 37) == 'GRADUANDO':
    #         sheet2.write(row, 38, sheet.cell_value(row, 18))

    # workbook.save(caminho3)
    # wb.release_resources()
    # del wb
            


