import pandas_dedupe
import numpy as np
import pandas as pd  
import os
import sys
import glob
import re
import networkx as nx
from pathlib import Path
FILE_DIR = Path(__file__).parent

# Apenas tirar as deduplicações após limpar os dados com CytoScape e Gephi.
# Peguei em formato .csv o grafo gerado em 'grafo_coautoria_eventos'
# Apenas os nomes dos autores para fazer a deduplicação
autores = (FILE_DIR/"../scraperXMLtoCSV/data/dedupe/autores_extraidos_raw.csv").resolve() 
pathfilename = (FILE_DIR/"../scraperXMLtoCSV/data/dedupe/autores_extraidos_parsed.csv").resolve()
# deduplicação de nomes com a biblioteca pandas_dedupe

def getDedupe():
    df = pd.read_csv(autores)
    data2 = pandas_dedupe.dedupe_dataframe(df,['shared name'], update_model= False)
    data2.to_csv(pathfilename, index = False)
    print("Dados deduplicados com sucesso")
    print("------------------")