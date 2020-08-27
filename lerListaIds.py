import pandas as pd


def lerListaIds():
    df_idList = pd.read_csv('listaID.txt', dtype='str', skiprows=4, header=0, sep=',')
    return(df_idList)
