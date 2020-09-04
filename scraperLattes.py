# This Python file uses the following encoding: utf-8
# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
import zipfile



# ------------------------------------------------------------
# Artigos publicados
# ------------------------------------------------------------

def getartigospublicados(zipname):
    # Lendo os currículos Lattes da pasta lattes_autores
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml', from_encoding='ISO-8859-1')
    # ------------------------------------------------------------
    # Extraindo currículo vitae
    curriculo_vitae = bs.find_all('curriculo-vitae')
    # Verificação de existência do currículo vitae
    if len(curriculo_vitae) == 0:
        print("Curriculo nao encontrado")
    else:
        # Listas para armazenamento do nome do autor e id. 
        nome_completo = []
        id_lattes = []
        for i in range(len(curriculo_vitae)):
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrado')
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    data_dg = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', data_dg)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux) 
            # Extraindo todas as produções bibliográficas
            producao_bibliografica = bs.find_all('producao-bibliografica')
            # Verificando a existência de demais produções bibliográficas
            if len(producao_bibliografica) == 0:
                print('Producoes bibliograficas nao encontrada')
            else:
                # Da producao bibliografica extrair o grupo de artigos publicados
                artigos_publicados = producao_bibliografica[0].find_all('artigos-publicados')
                # Verificando se há artigos publicados
                if len(artigos_publicados) == 0:
                    print('Artigos publicados nao encontrado')
                else:
                    # Listas para armazenamento de dados dos periódicos
                    titulo_periodico = []
                    ano_periodico = []
                    doi_periodico = []
                    linguagem_periodico = []
                    journal_periodico = []
                    autores_periodico = []
                    cidade_evento = []
                    ano_evento = []
                    # A partir do grupo de artigos publicados extrair os artigos publicados
                    artigo_publicado = artigos_publicados[0].find_all('artigo-publicado')
                    id_lattes = np.repeat(id_lattes, len(artigo_publicado))
                    nome_completo = np.repeat(nome_completo, len(artigo_publicado))
                    # A partir de cada artigo publicado extrair as informações de interesse
                    for i in range(len(artigo_publicado)):
                        # dados basicos do periodico
                        dados_basicos_artigo = artigo_publicado[i].find_all('dados-basicos-do-artigo')
                        artigo_db = str(dados_basicos_artigo)
                        # definindo o nome do periodico
                        data_campo = re.search('titulo-do-artigo=\"(.*)\" titulo-do-artigo-i', artigo_db)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        titulo_periodico.append(resultado)
                        # definindo ano do periodico
                        data_campo = re.search('ano-do-artigo=\"(.*)\" doi', artigo_db)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        ano_periodico.append(resultado)
                        # definindo doi do periodico
                        data_campo = re.search('doi=\"(.*)\" flag-divulgacao-c', artigo_db)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        doi_periodico.append(resultado)
                        # definindo idioma do periodico
                        data_campo = re.search('idioma=\"(.*)\" meio-de-divulgacao=', artigo_db)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        linguagem_periodico.append(resultado)
                        # detalhamento do periodico
                        detalhamento_artigo = artigo_publicado[i].find_all('detalhamento-do-artigo')
                        dt_artigo = str(detalhamento_artigo)
                        # Definindo titulo do periodico
                        data_campo = re.search('titulo-do-periodico-ou-revista=\"(.*)\" volume', dt_artigo)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        journal_periodico.append(resultado)
                        # definindo cidade do evento
                        data_campo = re.search('cidade-do-evento=\"(.*)\" classificacao-do-evento', dt_artigo)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        cidade_evento.append(resultado)
                        # definindo ano do evento
                        data_campo = re.search('ano-de-realizacao=\"(.*)\" cidade-da-editora', dt_artigo)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        ano_evento.append(resultado)
                        # Autores do periodico
                        aux_autores = artigo_publicado[i].find_all('autores')
                        todos_autores = []
                        for j in range(len(aux_autores)):
                            aux2_autores = str(aux_autores[j])
                            data_campo = re.search('nome-para-citacao=\"(.*)\" nro-id-cnpq=', aux2_autores)
                            if data_campo is None:
                                resultado = 'SEM_DADOS'
                            else:
                                resultado = data_campo.group(1)
                            todos_autores.append("{0} {1}".format(resultado, 'and'))
                        autores_periodico.append(todos_autores)    
                    # DataFrame periodicos

                    periodico = 'PERIODICO'
                    lattes_lattes = 'LATTES'

                    df_nome = pd.DataFrame ({
                    'FONTE': lattes_lattes,
                    'TIPO': periodico,
                    'ID_LATTES': id_lattes,
                    'NOME': nome_completo })

                    df_periodicos = pd.DataFrame ({
                    'DOI': doi_periodico,
                    'TITULO': titulo_periodico,
                    'ANO': ano_periodico,
                    'LANG': linguagem_periodico,
                    'EVENTO/JOURNAL/LIVRO': journal_periodico,
                    'CIDADE_EVENTO': cidade_evento,
                    'ANO_EVENTO': ano_evento,
                    'AUTORES': autores_periodico })

                    lattes_id = zipname.split('.')[0]
                    frames = [df_nome, df_periodicos]
                    df_periodicos = pd.concat(frames,axis=1)
                    pathfilename = str('./data/periodicos/' + lattes_id + '_artigoperiodico'  '.csv')
                    df_periodicos.to_csv(pathfilename, index=False)
                    print('Artigo coletado com sucesso')
                    print('------------------')

# ------------------------------------------------------------
# Artigos completos publicados em Eventos
# ------------------------------------------------------------

def getartigoseventos(zipname):
    # Lendo do zipfile
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml', from_encoding='ISO-8859-1')
    # ------------------------------------------------------------
    # extrair curriculo vitae
    curriculo_vitae = bs.find_all('curriculo-vitae')
    # VERIFICANDO se ha demais tipos de producao
    if len(curriculo_vitae) == 0:
        print('curriculo nao encontrado')
    else:
        # listas para armazenamento de dados 
        nome_completo = []
        id_lattes = []
        for i in range(len(curriculo_vitae)):
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrado')
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    dg_nome_completo = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', dg_nome_completo)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux)
    # extrair todas as producoes bibliograficas
    producao_bibliografica = bs.find_all('producao-bibliografica')
    # VERIFICANDO se ha demais tipos de producao
    if len(producao_bibliografica) == 0:
        print('Producoes bibliograficas nao encontrada')
    else:
        # Da producao bibliografica extrair o grupo de trabalhos de Eventos
        trabalhos_eventos = producao_bibliografica[0].find_all('trabalhos-em-eventos')
        # VERIFICANDO se há trabalhos publicados
        if len(trabalhos_eventos) == 0:
            print('Artigos publicados nao encontrado')
        else:
            # listas para armazenamento de dados dos artigos de Evento
            natureza = [] 
            titulo_artigo_evento = [] 
            ano_artigo_evento = [] 
            linguagem_artigo_evento = [] 
            nome_evento = []
            cidade_evento = []
            ano_evento = []
            autores_artigo_evento = []
            # A partir do grupo de trabalhos em eventos extrair os mesmos
            trabalho_em_eventos = trabalhos_eventos[0].find_all('trabalho-em-eventos')
            id_lattes = np.repeat(id_lattes, len(trabalho_em_eventos))
            nome_completo = np.repeat(nome_completo, len(trabalho_em_eventos))
            # a partir de cada artigo publicado extrair informações de interesse
            for i in range(len(trabalho_em_eventos)):
                # dados basicos do trabalho
                dados_basicos_trabalho = trabalho_em_eventos[i].find_all('dados-basicos-do-trabalho')
                db_evento = str(dados_basicos_trabalho)
                # definindo a natureza do trabalho
                data_campo = re.search('natureza=\"(.*)\" pais-do-evento', db_evento)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                natureza.append(resultado)
                # definindo o nome do trabalho
                data_campo = re.search('titulo-do-trabalho=\"(.*)\" titulo-do-trabalho-i', db_evento)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                titulo_artigo_evento.append(resultado)
                # definindo ano do trabalho
                data_campo = re.search('ano-do-trabalho=\"(.*)\" doi', db_evento)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                ano_artigo_evento.append(resultado)
                # definindo idioma do trabalho
                data_campo = re.search('idioma=\"(.*)\" meio-de-divulgacao=', db_evento)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                linguagem_artigo_evento.append(resultado)
                # detalhamento do trabalho
                detalhamento_artigo = trabalho_em_eventos[i].find_all('detalhamento-do-trabalho')
                dt_trabalho = str(detalhamento_artigo)
                # definindo titulo do evento
                data_campo = re.search('titulo-dos-anais-ou-proceedings=\"(.*)\" volume', dt_trabalho)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                nome_evento.append(resultado)
                # definindo cidade do evento
                data_campo = re.search('cidade-do-evento=\"(.*)\" classificacao-do-evento', dt_trabalho)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                cidade_evento.append(resultado)
                # definindo ano do evento
                data_campo = re.search('ano-de-realizacao=\"(.*)\" cidade-da-editora', dt_trabalho)
                if data_campo is None:
                    resultado = 'SEM_DADOS'
                else:
                    resultado = data_campo.group(1)
                ano_evento.append(resultado)
                # autores 
                aux_autores = trabalho_em_eventos[i].find_all('autores')
                todos_autores = []
                for j in range(len(aux_autores)):
                    aux2_autores = str(aux_autores[j])
                    data_campo = re.search('nome-para-citacao=\"(.*)\" nro-id-cnpq=', aux2_autores)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    todos_autores.append("{0} {1}".format(resultado, 'and'))
                autores_artigo_evento.append(todos_autores)
            # DataFrame trabalhos de evento
            eventos = 'TRAB.EVENTO'
            lattes_lattes = 'LATTES'

            df_nome = pd.DataFrame ({
            'FONTE': lattes_lattes,
            'TIPO': eventos,
            'ID_LATTES': id_lattes,
            'NOME': nome_completo}) 

            df_artigos_eventos = pd.DataFrame ({
            'NATUREZA': natureza,
            'TITULO': titulo_artigo_evento,
            'ANO': ano_artigo_evento,
            'LANG': linguagem_artigo_evento,
            'EVENTO/JOURNAL/LIVRO': nome_evento,
            'CIDADE_EVENTO': cidade_evento,
            'ANO_EVENTO': ano_evento,
            'AUTORES': autores_artigo_evento})

            lattes_id = zipname.split('.')[0]
            frame = [df_nome, df_artigos_eventos]
            df_artigos_eventos = pd.concat(frame, axis=1)
            pathfilename = str('./data/trabeventos/' + lattes_id + '_trabalhoeventos'  '.csv')
            df_artigos_eventos.to_csv(pathfilename, index=False)
            print('Trabalhos em eventos coletado com sucesso.')
            print('------------------')

# ------------------------------------------------------------
# Nome completo, nome citacao, e bio
# ------------------------------------------------------------


def getnomecompleto(zipname):
    # lendo do zipfile
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml', from_encoding='ISO-8859-1')
    # extrair curriculo 
    curriculo_vitae = bs.find_all('curriculo-vitae')
    # VERIFICANDO se ha demais tipos de producao
    if len(curriculo_vitae) == 0:
        print('curriculo nao encontrado para', zipname)
    else:
        # listas para armazenamento de dados
        nome_completo = []
        id_lattes = []
        cidade = []
        estado = []
        resumo = []
        atualizacao_lattes = []
        nome_citacao = []
        for i in range(len(curriculo_vitae)):
            # definindo atualizacao
            cv_atualizacao = str(curriculo_vitae[i])
            data_campo = re.search('data-atualizacao=\"(.*)\" hora-atualizacao',
                               cv_atualizacao)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
                update = str(resultado[0:2]) + '-' + \
                    str(resultado[2:4]) + '-' + str(resultado[4:])
                resultado = update
                atualizacao_lattes.append(resultado)
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrado.')
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    dg_data = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', dg_data)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux)
                    # definindo cidade
                    dg_data = str(dados_gerais[j])
                    data_campo = re.search('cidade-nascimento=\"(.*)\" data-faleci', dg_data)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    cidade.append(resultado)
                    # definindo estado
                    dg_data = str(dados_gerais[j])
                    data_campo = re.search('uf-nascimento=\"(.*)\"><res', dg_data)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    estado.append(resultado)
                    # definindo nome em citações
                    dg_citacoes = str(dados_gerais[j])
                    data_campo = re.search('nome-em-citacoes-bibliograficas=\"(.*)\" orcid-id', dg_citacoes)
                    if data_campo is None:
                        data_campo = re.search('nome-em-citacoes-bibliograficas=\"(.*)\" pais-de-nacionalidade', dg_citacoes)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_citacao.append(resultado)
            resumo_curriculo_vitae = curriculo_vitae[i].find_all('resumo-cv')
            # VERIFICANDO se ha resumo
            if len(resumo_curriculo_vitae) == 0:
                print('Resumo curriculo_vitae nao encontrado.')
                data_campo2 = 'SEM_DADOS'
                resumo.append(data_campo2)
            else:
                for j in range(len(resumo_curriculo_vitae)):
                    # definindo resumo
                    data_cv = str(resumo_curriculo_vitae[j])
                    resultado = re.search('texto-resumo-cv-rh=\"(.*)\" texto-resumo-cv-rh-en=', data_cv, re.DOTALL)
                    if resultado is None:
                        data_campo2 = 'SEM_DADOS'
                    else:
                        data_campo2 = resultado.group(1)
                    resumo.append(data_campo2)
        # DataFrame nome completo e sobrenome

        df_fullname = pd.DataFrame({
        'ID_LATTES': id_lattes,
        'FULL_NAME': nome_completo,
        'CITADO': nome_citacao,
        'CITY': cidade,
        'STATE': estado,
        'RESUME': resumo,
        'UPDATE': atualizacao_lattes })

        lattes_id = zipname.split('.')[0]
        pathfilename = str('./data/autores/' + lattes_id + '_fullname'  '.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('Dados pessoais coletados.')
        print('------------------')


# Pega a formação dos currículos - GRAD, MES E DOUT
def getformacao(zipname):
    # lendo do zipfile
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml', from_encoding='ISO-8859-1')
    curriculo_vitae = bs.find_all('curriculo-vitae')
    if len(curriculo_vitae) == 0:
        print('curriculo vitae nao encontrado.')
    else:
        # listas para armazenamento do nome
        nome_completo = []
        id_lattes = []
        for i in range(len(curriculo_vitae)):
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    dg_nome_completo = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', dg_nome_completo)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux)
                df_id = pd.DataFrame({'ID': id_lattes})
    # ------------------------------------------------------------
    # extrair formação acadêmica.
    formacao_academica = bs.find_all('formacao-academica-titulacao')
    # VERIFICANDO se ha formação academica/titulacao
    if len(formacao_academica) == 0:
        print('Não encontrado formação acadêmica ou titulação para ', zipname)
    else:
        nome_instituicao = []
        nome_curso = []
        ano_inicio = []
        ano_termino = []
        var_grad = []
        titulacao = []
        # a partir da graduação veremos as infomações para adicionar.
        for i in range(len(formacao_academica)):
            # dados basicos da graduação
            graduacao = formacao_academica[0].find_all('graduacao')
            gradaux = str(graduacao[i])
            # verificação para existência de graduação.
            if (len(graduacao)==0):
                vargrad = 'NAO'
            else:
                vargrad = 'SIM'
            var_grad.append(vargrad)
            # definindo o nome da instituição
            data_campo = re.search('nome-instituicao=\"(.*)\" nome-instituicao-grad', gradaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            nome_instituicao.append(resultado)
            # definindo o nome do curso
            data_campo = re.search('nome-curso=\"(.*)\" nome-curso-ingles=', gradaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            nome_curso.append(resultado)
            # definindo o ano de começo
            data_campo = re.search('ano-de-inicio=\"(.*)\" codigo-agencia-financiadora=', gradaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'  
            else:
                resultado = data_campo.group(1)
            ano_inicio.append(resultado)
            # definindo o ano de fim
            data_campo = re.search('ano-de-conclusao=\"(.*)\" ano-de-inicio', gradaux)
            if data_campo is None: 
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            ano_termino.append(resultado)
        # Dataframe formação -- GRADUAÇÃO

        df_nome_e_vargrad = pd.DataFrame ({ 
        'NOME': nome_completo,
        'GRADUAÇÃO': var_grad})

        df_grad = pd.DataFrame ({
        'FACULDADE DE GRADUAÇÃO': nome_instituicao,
        'CURSO GRADUAÇÃO': nome_curso,
        'INICIO_GRADUACAO': ano_inicio,
        'TERMINO_GRADUACAO': ano_termino})

        lattes_id = zipname.split('.')[0]
        pathfilename2 = str('./data/formacao/' + lattes_id + '_formacao'  '.csv')
        frames = [df_grad, df_nome_e_vargrad, df_id]
        df_grad = pd.concat (frames, axis=1).drop_duplicates()
        df_grad.to_csv(pathfilename2, index=False)
        # começo da busca pelo mestrado
        mestrado = formacao_academica[i].find_all('mestrado')
        varmes = []
        # verificação para existência de mestrado.
        if (len(mestrado)==0):
            var_mes = 'NAO'
        else:
            var_mes = 'SIM'
        varmes.append(var_mes)
        nome_instituicao_mestrado = []
        nome_curso_mestrado = []
        ano_inicio_mestrado = []
        ano_fim_mestrado = []
        dissertacao_mestrado = []
        for j in range(len(mestrado)):
            mestaux = str(mestrado[j])
            data_campo = re.search('nome-instituicao=\"(.*)\" nome-instituicao-dout', mestaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            nome_instituicao_mestrado.append(resultado)
            # definindo o nome do curso de mestrado
            data_campo = re.search('nome-curso=\"(.*)\" nome-curso-ingles=', mestaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            nome_curso_mestrado.append(resultado)
            # definindo o nome da tese de mestrado
            data_campo = re.search('titulo-da-dissertacao-tese=\"(.*)\" titulo-da-dissertacao-tese-ingles', mestaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            dissertacao_mestrado.append(resultado)
            # definindo o nome da inicio do mestrado
            data_campo = re.search('ano-de-inicio=\"(.*)\" ano-de-obtencao-do-titulo=', mestaux)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            ano_inicio_mestrado.append(resultado)
            # definindo o nome da inicio do mestrado
            data_campo = re.search('ano-de-conclusao=\"(.*)\" ano-de-inicio', mestaux)
            if data_campo is None:  
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            ano_fim_mestrado.append(resultado)
        # Dataframe formação -- MESTRADO

        df_varmes = pd.DataFrame ({
        'MESTRADO': varmes})

        df_mestrado = pd.DataFrame ({
        'FACULDADE DE MESTRADO': nome_instituicao_mestrado,
        'CURSO DE MESTRADO': nome_curso_mestrado,
        'DISSERTAÇÃO DE MESTRADO': dissertacao_mestrado,
        'INICIO_MESTRADO': ano_inicio_mestrado,
        'TERMINO_MESTRADO': ano_fim_mestrado})

        lattes_id = zipname.split('.')[0]
        frames = [df_grad, df_mestrado]
        dfjuncao = pd.concat(frames, axis=1).drop_duplicates()
        pathfilename2 = str('./data/formacao/' + lattes_id + '_formacao'  '.csv')
        dfjuncao.to_csv(pathfilename2, index=False)
        # começo da busca pelo doutorado
        dout = formacao_academica[i].find_all('doutorado')
        var_dout = []
        # verificação para existência de doutorado.
        if (len(dout)==0):
            vardout = 'NAO'
        else:
            vardout = 'SIM'
        var_dout.append(vardout)
        nome_instituicao_doutorado = []
        nome_curso_doutorado = []
        ano_inicio_doutorado = []
        ano_fim_doutorado = []
        tese_doutorado = []
        orientador_doutorado = []
        for j in range(len(dout)):
            doutt = str(dout[j])
            data_campo = re.search('nome-instituicao=\"(.*)\" nome-instituicao-dout', doutt)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            nome_instituicao_doutorado.append(resultado)
            # definindo o nome do curso de doutorado
            data_campo = re.search('nome-curso=\"(.*)\" nome-curso-ingles=', doutt)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            nome_curso_doutorado.append(resultado)
            # definindo o nome da tese de doutorado
            data_campo = re.search('titulo-da-dissertacao-tese=\"(.*)\" titulo-da-dissertacao-tese-ingles', doutt)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            tese_doutorado.append(resultado)
            # definindo o nome da inicio do doutorado
            data_campo = re.search('ano-de-inicio=\"(.*)\" ano-de-obtencao-do-titulo=', doutt)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            ano_inicio_doutorado.append(resultado)
            # definindo o nome da inicio do mestrado
            data_campo = re.search('ano-de-conclusao=\"(.*)\" ano-de-inicio', doutt)
            if data_campo is None:  
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            ano_fim_doutorado.append(resultado)
            # definindo o nome do orientador da tese de doutorado
            data_campo = re.search('nome-completo-do-orientador=\"(.*)\" nome-curso=', doutt)
            if data_campo is None:
                resultado = 'SEM_DADOS'
            else:
                resultado = data_campo.group(1)
            orientador_doutorado.append(resultado)
        # DataFrame formação -- DOUTORADO

        df_vardout = pd.DataFrame ({
        'DOUTORADO': var_dout})

        df_doutorado = pd.DataFrame ({
        'FACULDADE DE DOUTORADO': nome_instituicao_doutorado,
        'CURSO DE DOUTORADO': nome_curso_doutorado,
        'TESE DE DOUTORADO': tese_doutorado,
        'ORIENTADOR DA TESE': orientador_doutorado,
        'INICIO_DOUTORADO': ano_inicio_doutorado,
        'TERMINO_DOUTORADO': ano_fim_doutorado}) 

        lattes_id = zipname.split('.')[0]
        ls_instituicao_titulacao = []
        df_titulacao = pd.DataFrame ({
        'TITULACAO': titulacao,
        'AFILIACAO': ls_instituicao_titulacao})
        frames2 = [df_nome_e_vargrad, df_grad, df_varmes, df_mestrado, df_vardout, df_doutorado, df_titulacao]
        df_juncao_final = pd.concat(frames2, axis=1).drop_duplicates()
        pathfilename2 = str('./data/formacao/' + lattes_id + '_formacao'  '.csv')
        df_juncao_final.to_csv(pathfilename2, index=False)
        print ('Formação coletada.')
        print('------------------')


# ------------------------------------------------------------
# Retirar local - afiliação - Não consegui um campo que represente bem o que queremos retirar. Ainda no estudo.
# ~ NÃO FINALIZADO ~
# ------------------------------------------------------------

def getlocal(zipname):
    # lendo do zipfile
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml', from_encoding='ISO-8859-1')
    # extrair curriculo vitae
    curriculo_vitae = bs.find_all('curriculo-vitae')
    # VERIFICANDO se ha demais tipos de producao
    if len(curriculo_vitae) == 0:
        print('curriculo nao encontrado para', zipname)
    else:
        # listas para armazenamento de dados 
        nome_completo = []
        id_lattes = []
        nome_instituicao = []
        for i in range(len(curriculo_vitae)):
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    dg_nome_completo = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', dg_nome_completo)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux)
            endereco = curriculo_vitae[i].find_all('endereco')
            # VERIFICANDO se ha endereço
            if len(endereco) == 0:
                print('Endereço nao encontrado.')
            else:
                endeprof = curriculo_vitae[i].find_all('endereco-profissional')
            # VERIFICANDO se ha endereço profissional
            if len(endeprof) == 0:
                print('Endereço profissional nao encontrado.')
            else:
                for j in range(len(endeprof)):
                    # definindo nome da instituição
                    data_ende = str(endeprof[j])
                    data_campo = re.search('nome-instituicao-empresa=\"(.*)\" nome-orgao', data_ende)
                    if data_campo is None:
                        resultado = 'NÃO'
                    else:
                        resultado = data_campo.group(1)
                    nome_instituicao.append(resultado)
                # DataFrame afiliacao

                df_afiliacao = pd.DataFrame ({
                'ID': id_lattes,
                'NOME COMPLETO': nome_completo,
                'INSTITUIÇÃO': nome_instituicao})

                lattes_id = zipname.split('.')[0]
                pathfilename = str('./data/afiliacao/' + lattes_id + '_afiliacao'  '.csv')
                df_afiliacao.to_csv(pathfilename, index=False)
                print('Afiliacao coletada.')
                print('------------------')

# ------------------------------------------------------------
# Busca por atuações profissionais
# ------------------------------------------------------------

def getatuacoes(zipname):
    # Lendo do zipfile
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml', from_encoding='ISO-8859-1')
    # ------------------------------------------------------------
    curriculo_vitae = bs.find_all('curriculo-vitae')
    if len(curriculo_vitae) == 0:
        print('curriculo vitae nao encontrado para', zipname)
    else:
        # listas para armazenamento do nome
        nome_completo = []
        id_lattes = []
        for i in range(len(curriculo_vitae)):
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    dg_nome_completo = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', dg_nome_completo)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux)
                atuacoes_profissionais = dados_gerais[0].find_all('atuacoes-profissionais')
                # VERIFICANDO se há atuações profissionais
                if len(atuacoes_profissionais) == 0:
                    print('Atuacoes profisionais nao encontrada.')
                else:
                    # listas para armazenamento de dados das atuações profissionais
                    nome_instituicao_profissional = [] 
                    ano_inicio_profissional = [] 
                    ano_fim_profissional = [] 
                    outro_enquadramento = []
                    atuacao_profissional = atuacoes_profissionais[0].find_all('atuacao-profissional')
                    id_lattes = np.repeat(id_lattes, len(atuacao_profissional))
                    # a partir de cada atuação profissional encontrada, os dados requeridos são extraídos
                    for i in range(len(atuacao_profissional)):
                        atuacao_aux = str(atuacao_profissional[i])
                        vinculos = atuacao_profissional[i].find_all('vinculos')
                        for j in range(len(vinculos)):
                            vinculos_aux = str(vinculos[j])
                            # definindo o nome da instituição
                            data_campo = re.search('nome-instituicao=\"(.*)\" sequencia-atividade=', atuacao_aux)    
                            if data_campo is None:
                                resultado = 'SEM_DADOS'
                            else:
                                resultado = data_campo.group(1)
                            nome_instituicao_profissional.append(resultado)
                            # definindo o ano de inicio
                            data_campo = re.search('ano-inicio=\"(.*)\" carga-horaria-semanal=', vinculos_aux)
                            if data_campo is None:
                                resultado = 'SEM_DADOS'
                            else:
                                resultado = data_campo.group(1)
                            ano_inicio_profissional.append(resultado)
                            # definindo o ano do fim 
                            data_campo = re.search('ano-fim=\"(.*)\" ano-inicio=', vinculos_aux)
                            if data_campo is None:
                                resultado = 'ATUAL'
                            else:
                                resultado = data_campo.group(1)
                            ano_fim_profissional.append(resultado)
                            # definindo a função
                            data_campo = re.search('outro-enquadramento-funcional-informado=\"(.*)\" outro-enquadramento-funcional-informado-ingles=', vinculos_aux)
                            if data_campo is None:
                                data_campo = re.search('outro-enquadramento-funcional-informado=\"(.*)\" outro-vinculo-informado=', vinculos_aux)
                            if data_campo is None:
                                resultado = 'SEM_DADOS'
                            else:
                                resultado = data_campo.group(1)
                            outro_enquadramento.append(resultado)
                    # DataFrame atuação profissional

                    df_id = pd.DataFrame ({
                    'ID': id_lattes})

                    df_insti = pd.DataFrame ({
                    'INSTITUICAO/EMPRESA': nome_instituicao_profissional})

                    df_atuacao_profissional = pd.DataFrame ({
                    'INÍCIO': ano_inicio_profissional,
                    'FIM': ano_fim_profissional,
                    'FUNCAO': outro_enquadramento})

                    lattes_id = zipname.split('.')[0]
                    pathfilename = str('./data/atuacoes/' + lattes_id + '_atuacoes'  '.csv')
                    frame = [df_id, df_insti, df_atuacao_profissional]
                    df_atuacao_profissional = pd.concat (frame, axis=1).drop_duplicates()
                    df_atuacao_profissional.to_csv(pathfilename, index=False)
                    print('Atuacoes coletadas.')
                    print('------------------')

# ------------------------------------------------------------
# Capitulos de livros
# ------------------------------------------------------------


def getcapit(zipname):
    # lendo do zipfile
    # zipname = '1292986021348016.zip'
    caminho = './lattes_autores' + '/' + str(zipname)
    arquivo = zipfile.ZipFile(caminho, 'r')
    data_xml = arquivo.open('curriculo.xml')
    bs = BeautifulSoup(data_xml, 'lxml',
                         from_encoding='ISO-8859-1')
    # ------------------------------------------------------------
    curriculo_vitae = bs.find_all('curriculo-vitae')
    if len(curriculo_vitae) == 0:
        print('curriculo vitae nao encontrado.')
    else:
        # listas para armazenamento do nome
        nome_completo = []
        id_lattes = []
        for i in range(len(curriculo_vitae)):
            dados_gerais = curriculo_vitae[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dados_gerais) == 0:
                print('Dados gerais nao encontrado.')
            else:
                for j in range(len(dados_gerais)):
                    # definindo nome completo
                    dg_nome_completo = str(dados_gerais[j])
                    data_campo = re.search('nome-completo=\"(.*)\" nome-em-citacoes', dg_nome_completo)
                    if data_campo is None:
                        resultado = 'SEM_DADOS'
                    else:
                        resultado = data_campo.group(1)
                    nome_completo.append(resultado)
                    id_aux = zipname.split('.')[0]
                    id_lattes.append(id_aux)
            # extrair todas as producoes livros e capitulos
            livros_e_capitulos = bs.find_all('livros-e-capitulos')
            # listas para armazenamento de dados livros e capitulos
            titulo_capitulo = []
            ano_capitulo = []
            linguagem_capitulo = []
            editora_capitulo = []
            autores_capitulo = []
            nome_livro = []
            # VERIFICANDO se ha livros e capitulos
            if len(livros_e_capitulos) == 0:
                print('Capitulos publicados nao encontrados.')
            else:
                capitulos_de_livros_publicados = livros_e_capitulos[0].find_all('capitulos-de-livros-publicados')
                # a partir de cada livro capitulo publicado extrair inf de interesse
                # VERIFICANDO se ha livros e capitulos
                if len(capitulos_de_livros_publicados) == 0:
                    print('Capitulos publicados nao encontrados.')
                else:
                    capitulo_de_livro_publicado = capitulos_de_livros_publicados[0].find_all('capitulo-de-livro-publicado')
                    id_lattes = np.repeat(id_lattes, len(capitulo_de_livro_publicado))
                    nome_completo = np.repeat(nome_completo, len(capitulo_de_livro_publicado))
                    for i in range(len(capitulo_de_livro_publicado)):
                        # dados basicos do livro
                        db_capitulo = capitulo_de_livro_publicado[i].find_all('dados-basicos-do-capitulo')
                        dados_basico_do_capitulo = str(db_capitulo)
                        # definindo o nome do capitulo
                        data_campo = re.search('titulo-do-capitulo-do-livro=\"(.*)\" titulo-do-capi', dados_basico_do_capitulo)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        titulo_capitulo.append(resultado)
                        # definindo ano do livro
                        data_campo = re.search('ano=\"(.*)\" doi', dados_basico_do_capitulo)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        ano_capitulo.append(resultado)
                        # definindo idioma do livro
                        data_campo = re.search('idioma=\"(.*)\" meio-de-divulgacao=', dados_basico_do_capitulo)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        linguagem_capitulo.append(resultado)
                        # detalhamento do livro
                        detalhamento_do_capitulo = capitulo_de_livro_publicado[i].find_all('detalhamento-do-capitulo')
                        det_aux = str(detalhamento_do_capitulo)
                        # definindo o nome do livro
                        data_campo = re.search('titulo-do-livro=\"(.*)\"', det_aux)
                        if data_campo is None:
                            resultado = 'SEM DADOS'
                        else:
                            resultado = data_campo.group(1)
                        nome_livro.append(resultado)
                        # definindo editora
                        data_campo = re.search('nome-da-editora=\"(.*)\" numero-da-edicao-r', det_aux)
                        if data_campo is None:
                            resultado = 'SEM_DADOS'
                        else:
                            resultado = data_campo.group(1)
                        editora_capitulo.append(resultado)
                        # print(resultado)
                        # autores do livro
                        aux_autores = capitulo_de_livro_publicado[i].find_all('autores')
                        todos_autores = []
                        for j in range(len(aux_autores)):
                            aux2_autores = str(aux_autores[j])
                            data_campo = re.search('nome-para-citacao=\"(.*)\" nro-id-cnpq=', aux2_autores)
                            if data_campo is None:
                                resultado = 'SEM_DADOS'
                            else:
                                resultado = data_campo.group(1)
                            todos_autores.append(resultado)
                        autores_capitulo.append(todos_autores)
                    # DataFrame livros publicados
                    capitulo = 'CAP.LIVRO'
                    lattes_lattes = 'LATTES'

                    df_id = pd.DataFrame ({
                    'FONTE': lattes_lattes,
                    'TIPO': capitulo,
                    'ID_LATTES': id_lattes,
                    'NOME': nome_completo})

                    df_capit = pd.DataFrame({
                    'TITULO': titulo_capitulo,
                    'EVENTO/JOURNAL/LIVRO': nome_livro,
                    'ANO': ano_capitulo,
                    'LANG': linguagem_capitulo,
                    'EDITORA': editora_capitulo,
                    'AUTORES': autores_capitulo})

                    lattes_id = zipname.split('.')[0]
                    pathfilename = str('./data/capitulos/' + lattes_id + '_capitulo'  '.csv')
                    frame = [df_id, df_capit]
                    df_capit2 = pd.concat (frame, axis=1)
                    df_capit2.to_csv(pathfilename, index=False)
                    print("Capitulos de livro coletados.")
