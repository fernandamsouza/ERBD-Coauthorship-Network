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
edicoes = (FILE_DIR/"../dedupe_edicoes/edicoes.csv").resolve() 
pathfilename = (FILE_DIR/"../dedupe_edicoes/edicoes_parsed.csv").resolve()
# deduplicação de nomes com a biblioteca pandas_dedupe


df = pd.read_csv(edicoes)
data2 = pandas_dedupe.dedupe_dataframe(df,['evento_journal'], update_model= False)
data2.to_csv(pathfilename, index = False)
print("Dados deduplicados com sucesso")
print("------------------")
