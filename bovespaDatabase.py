__author__ = 'Ibis'

'''
Descrição do arquivo!

Esse documento trata os dados referentes a Bovespa.

Funções:
    downloadFiles - Realiza o download dos arquivos contendo as operações do ano
        Input - Ano
        Output - Arquivo txt dentro da pasta

'''

import wget
import zipfile
import os
import sqlite3

def createTable(papel):
    conn = sqlite3.connect('Bovespa.db')
    c = conn.cursor()

    str = '''CREATE TABLE IF NOT EXISTS papel (
    'datapr'	TEXT NOT NULL UNIQUE,
    'codbdi'	TEXT,
    'codneg'	TEXT,
    'tpmerc'	NUMERIC,
    'nomres'	TEXT,
    'especi'	TEXT,
    'prazot'	TEXT,
    'modref'	TEXT,
    'preabe'	NUMERIC,
    'premax'	NUMERIC,
    'premin'	NUMERIC,
    'premed'	NUMERIC,
    'preult'	NUMERIC,
    'preofc'	NUMERIC,
    'preofv'	NUMERIC,
    'totneg'	NUMERIC,
    'quatot'	NUMERIC,
    'voltot'	NUMERIC,
    'preexe'	NUMERIC,
    'indopc'	NUMERIC,
    'datven'	NUMERIC,
    'fatcot'	NUMERIC,
    'ptoexe'	NUMERIC,
    'codisi'	TEXT,
    'dismes'	NUMERIC,
    PRIMARY KEY(datapr))'''

    str = str.replace('papel', "'" + papel + "'")

    # Create table
    c.execute(str)

    # Save (commit) the changes
    conn.commit()
    conn.close()

def insertMany(papel, data):

    conn = sqlite3.connect('Bovespa.db')
    c = conn.cursor()

    str = 'INSERT INTO table VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    str = str.replace('table', "'" + papel + "'")
    c.executemany(str, data)

    conn.commit()
    conn.close()

    return

def downloadFiles(ano):
    file = 'COTAHIST_Aano.ZIP'
    file = file.replace('ano',ano)
    str = 'http://www.bmfbovespa.com.br/InstDados/SerHist/' + file

    # Download do arquivo zip
    print('Downloading ' + ano + '...')
    wget.download(str)

    # Extrai arquivo zip para a pasta Bovespa
    with zipfile.ZipFile(file, "r") as z:
        z.extractall("Bovespa/")
    print('File ' + ano + ' saved!')

    # Deleta arquivo zip
    os.remove(file)

def divideLine(line):
    datapr = int(line[2:10])                                   # Data do pregão
    codbdi = line[10:12].strip()                               # Código BDI
    codneg = line[12:24].strip()                               # Código de negociação do papel
    tpmerc = int(line[24:27])                                  # Código do mercado em que o papel está cadastrado
    nomres = line[27:39].strip()                               # Nome resumido da empresa emissora do papel
    especi = line[39:49].strip()                               # Especificação do papel
    prazot = line[49:52].strip()                               # Prazo em dias do mercado a termo
    modref = line[52:56].strip()                               # Moeda usada na tada do pregão
    preabe = float(line[56:67]+'.'+line[67:69])                # Preço de abertura do papel no pregão
    premax = float(line[69:80]+'.'+line[80:82])                # Preço máximo do papel no pregão
    premin = float(line[82:93]+'.'+line[93:95])                # Preço mínimo do papel no pregão
    premed = float(line[95:106]+'.'+line[106:108])             # Preço médio do papel no pregão
    preult = float(line[108:119]+'.'+line[119:121])            # Preço do último negócio do papel no pregão
    preofc = float(line[121:132]+'.'+line[132:134])            # Preço da melhor oferta de compra do papel no pregão
    preofv = float(line[134:145]+'.'+line[145:147])            # Preço da melhor oferta de venda do papel no pregão
    totneg = int(line[147:152])                                # Número de negócios efetuados com o papel no pregão
    quatot = int(line[152:170])                                # Quantidade total de títulos negociados neste papel
    voltot = float(line[170:186]+'.'+line[186:188])            # Volume total de títulos negociados neste papel
    preexe = float(line[188:199]+'.'+line[199:201])            # Preço de exercício para o mercado de opções ou valor do contrato para o mercado de termo secundário
    indopc = int(line[201:202])                                # Indicador de correção de preços de exercícios ou valores de contrato para os mercados de opções ou termo secundário
    datven = line[202:210].strip()                             # Data do vencimento para os mercados de opções ou termo secundário
    fatcot = int(line[210:217])                                # Fator de cotação do papel
    ptoexe = float(line[217:225]+'.'+line[225:230])            # Preço de exercício em pontos para opções referenciadas em dólar ou valor de contrato em pontos para termo secundário
    codisi = line[230:242].strip()                             # Código do papel no sistema ISIN ou código interno do papel
    dismes = line[242:245].strip()                             # Número de distribuição do papel

    '''print(voltot)
    print(dismes)
    print(codisi)
    print(ptoexe)
    print(fatcot)
    print(datven)
    print(indopc)
    print(preexe)
    print(voltot)
    print(quatot)
    print(totneg)
    print(preofv)
    print(preofc)
    print(preult)
    print(premed)
    print(premin)
    print(premax)
    print(preabe)
    print(modref)
    print(prazot)
    print(especi)
    print(nomres)
    print(tpmerc)
    print(codneg)
    print(codbdi)
    print(datapr)'''

    return [datapr, codbdi, codneg, tpmerc, nomres, especi, prazot, modref, preabe, premax, premin, premed,
        preult, preofc, preofv, totneg, quatot, voltot, preexe, indopc, datven, fatcot, ptoexe, codisi, dismes]

#downloadFiles('2015')
negociacoes = list()
with open('Bovespa/COTAHIST_A2015.txt','r') as file:
    for line in file:
        if line[0:2] == '01':
            #print(line)
            dados = divideLine(line)
            negociacoes.append(dados)

papel = list()

# Cria lista com todos os papéis diferentes negociados
for p in negociacoes:
    if p[2] not in papel:
        papel.append(p[2])

# Para cada papel cria uma tabela se não existir e salva no banco de dados
count = 1
erro = 0

for p in papel:
    createTable(p)

    a = [item for item in negociacoes if (item[2]== p)]

    try:
        insertMany(p, a)
        print('Inserido ' + p + ' - ' + str(count) + '/' + str(len(papel)))
    except:
        print('Erro em ' + p + ' - ' + str(count) + '/' + str(len(papel)))
        erro +=1

    count += 1

print('Total de entradas - ' + str(len(papel)))
print('Total de tabelas criadas - ' + str(len(papel) - erro))
print('Total de tabelas com erro - ' + str(erro))