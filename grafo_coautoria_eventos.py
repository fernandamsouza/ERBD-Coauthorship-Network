import networkx as nx
import xlrd
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------------------------------------------
# Arquivo para geração do grafo de coautoria.
# -------------------------------------------------------------------

FILE_DIR = Path(__file__).parent

excel_autores = (FILE_DIR/"../scraperXMLtoCSV/data/autores/autores_juncao/fullname_all.xlsx").resolve()
excel_artigos = (FILE_DIR/"../scraperXMLtoCSV/data/publicacoes_tudo/tudo_all.xlsx").resolve()
saida_grafo = (FILE_DIR/"../scraperXMLtoCSV/grafo/authors_graph_eventos.graphml").resolve()

# -------------------------------------------------------------------
# Informações sobre o grafo
# -------------------------------------------------------------------
'''
Informações sobre o grafo de coautoria:

Nós - autores específicos.
Edges - pelo menos um paper escrito em conjunto.
Atributos:
    weight = número de papers escritos juntos.
'''
# -------------------------------------------------------------------

grafo_autores = None

def init_nos():
    global grafo_autores
    wb = xlrd.open_workbook(excel_autores, on_demand = True)
    # Inicializando os nós do grafo como autores.
    for sheet in wb.sheets():
        for row in range(1, sheet.nrows):
            author = sheet.cell_value(row, 3).title() 
            grafo_autores.add_node(author)
    wb.release_resources()
    del wb

def init_arestas(autores):
    global grafo_autores
    autores = autores.replace('[', '')
    autores = autores.replace(']', '')
    autores = autores.replace(',', '')
    autores = autores.replace("'", '')
    autores = autores.split('and')
    # adicionando/atualizando as arestas para cada par de autores
    for i in range(0, len(autores)):
        for j in range(i + 1, len(autores)):
            if grafo_autores.has_edge(autores[i], autores[j]):
                grafo_autores[autores[i]][autores[j]]['weight'] += 1 # atualizando peso da aresta existente
            else:
                grafo_autores.add_edge(autores[i], autores[j], weight = 1) # adicionando nova aresta

def getcreate_graph_eventos():
    global grafo_autores
    grafo_autores = nx.Graph()
    paper_set = set()

    print("Inicializando os nós de autores do grafo: " + str(excel_autores))
    init_nos()

    wb = xlrd.open_workbook(excel_artigos, on_demand = True, encoding_override='cp1252')
    sheet = wb.sheet_by_index(0)
    dic_periodico = 'PERIODICO'
    dic_evento = 'TRABEVENTO'

    print("Inicializando as arestas " + str(excel_artigos))
    for row in range(1, sheet.nrows):
        linha = [sheet.cell_value(row, 0), # Fonte
                sheet.cell_value(row, 1), # Tipo
                sheet.cell_value(row, 2), # Doi
                sheet.cell_value(row, 3), # Título
                sheet.cell_value(row, 4), # Ano
                sheet.cell_value(row, 5), # Lang
                sheet.cell_value(row, 6), # Evento/journal
                sheet.cell_value(row, 7), # Autores
                sheet.cell_value(row, 8)] # ID
        # Verificando papers duplicados
        if linha[3].lower() in paper_set: 
            continue
        else:
            paper_set.add(linha[3].lower()) 
        init_arestas(linha[7]) 
        if linha[1] == 'PERIODICO':
            nx.set_edge_attributes(grafo_autores, 'SIM', dic_periodico)
        if linha[1] == 'TRABEVENTO':
            nx.set_edge_attributes(grafo_autores, 'SIM', dic_evento)
    print("Grafo dos autores gerado.")
    # labels
    nx.write_graphml(grafo_autores, saida_grafo)
    print("Grafo dos autores escrito em: " + str(saida_grafo))
    wb.release_resources()
    del wb

getcreate_graph_eventos()
