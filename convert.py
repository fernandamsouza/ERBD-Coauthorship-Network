from pyexcel.cookbook import merge_all_to_a_book
import glob

# -------------------------------------------------------------------
# Arquivo para realizar conversão csv -> xlsx (Objetivo: Geração do grafo)
# -------------------------------------------------------------------

def getConvert():
	merge_all_to_a_book(glob.glob("data/publicacoes_tudo/tudo_all.csv"), "data/publicacoes_tudo/tudo_all.xlsx")
	merge_all_to_a_book(glob.glob("data/autores/autores_juncao/fullname_all.csv"), "data/autores/autores_juncao/fullname_all.xlsx")
	merge_all_to_a_book(glob.glob("data/atuacoes/atuacoes_juncao/atuacoes_all.csv"), "data/atuacoes/atuacoes_juncao/atuacoes_all.xlsx")
	print ("Conversão para geração dos grafos feita com sucesso")
	print("------------------")
