# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

from juncaoDfs import getJuncao
from convert import getConvert
from scraperLattes import getnomecompleto
from scraperLattes import getformacao
from scraperLattes import getartigospublicados
from scraperLattes import getlocal
from scraperLattes import getatuacoes
from scraperLattes import getartigoseventos
from scraperLattes import getcapit
from lerListaIds import lerListaIds
from df_dedupe import getDedupe
from wordclouds import getWordcloud
import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile
import glob
import re
import rows

# ------------------------------------------------------------
# lendo a lista dos IDs e nome dos pesquisadores

df_idlist = lerListaIds()

# ------------------------------------------------------------
# roda as funcoes para pegar dados de cada pesquisador

for nid in range(len(df_idlist)):
    zipfilename = str(df_idlist.iloc[nid, 0]) + '.zip'
    getartigospublicados(zipfilename)
    #getnomecompleto(zipfilename)
    #getformacao(zipfilename)
    getartigoseventos(zipfilename)
    #getlocal(zipfilename)
    #getatuacoes(zipfilename)
    #getcapit(zipfilename)
getJuncao()
getConvert()
#getWordcloud()
#getDedupe() # Apenas vai ser usado após organização dos dados

#from grafo_coautoria_eventos import *

