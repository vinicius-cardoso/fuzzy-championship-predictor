import csv
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from collections import defaultdict

CSV_DATASET = 'brasileirao_serie_a.csv'
CSV_CONFRONTOS = 'confrontos.csv'

# Funções auxiliares
def get_confrontos():
    confrontos = []
    with open(CSV_CONFRONTOS, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)  # Ignora o cabeçalho
        for row in reader:
            confrontos.append(row)
    
    return confrontos

def get_percentual_colocacao(time_mandante, time_visitante, colocacoes, percetual_dic):
    if percetual_dic[colocacoes[time_mandante], colocacoes[time_visitante]] == 0.0:
        return 1.0
    return percetual_dic[colocacoes[time_mandante], colocacoes[time_visitante]]

def get_media_gols_pro_mandantes(csv_filename, times_mandantes_especificados, ano_inicio, ano_fim):
    dados_gols_especificado = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    dados_gols_total = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_mandante = row['time_mandante']
            ano_campeonato_str = row['ano_campeonato']
            if time_mandante in times_mandantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_mandante_str = row['gols_mandante']
                if gols_mandante_str.isdigit():
                    gols_mandante = int(gols_mandante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_gols_especificado[time_mandante]['soma_gols'] += gols_mandante
                        dados_gols_especificado[time_mandante]['quantidade_jogos'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_gols_total[time_mandante]['soma_gols'] += gols_mandante
                        dados_gols_total[time_mandante]['quantidade_jogos'] += 1
    
    medias_gols = {}
    for time in times_mandantes_especificados:
        if dados_gols_especificado[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_especificado[time]['soma_gols'] / dados_gols_especificado[time]['quantidade_jogos']
        elif dados_gols_total[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_total[time]['soma_gols'] / dados_gols_total[time]['quantidade_jogos']
        else:
            medias_gols[time] = 0
    
    return medias_gols

def get_media_gols_contra_visitantes(csv_filename, times_mandantes_especificados, ano_inicio, ano_fim):
    dados_gols_especificado = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    dados_gols_total = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_visitante = row['time_visitante']
            ano_campeonato_str = row['ano_campeonato']
            if time_visitante in times_mandantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_mandante_str = row['gols_mandante']
                if gols_mandante_str.isdigit():
                    gols_mandante = int(gols_mandante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_gols_especificado[time_visitante]['soma_gols'] += gols_mandante
                        dados_gols_especificado[time_visitante]['quantidade_jogos'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_gols_total[time_visitante]['soma_gols'] += gols_mandante
                        dados_gols_total[time_visitante]['quantidade_jogos'] += 1
    
    medias_gols = {}
    for time in times_mandantes_especificados:
        if dados_gols_especificado[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_especificado[time]['soma_gols'] / dados_gols_especificado[time]['quantidade_jogos']
        elif dados_gols_total[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_total[time]['soma_gols'] / dados_gols_total[time]['quantidade_jogos']
        else:
            medias_gols[time] = 0
    
    return medias_gols

def get_media_gols_contra_mandantes(csv_filename, times_visitantes_especificados, ano_inicio, ano_fim):
    dados_gols_especificado = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    dados_gols_total = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_mandante = row['time_mandante']
            ano_campeonato_str = row['ano_campeonato']
            if time_mandante in times_visitantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_visitante_str = row['gols_visitante']
                if gols_visitante_str.isdigit():
                    gols_visitante = int(gols_visitante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_gols_especificado[time_mandante]['soma_gols'] += gols_visitante
                        dados_gols_especificado[time_mandante]['quantidade_jogos'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_gols_total[time_mandante]['soma_gols'] += gols_visitante
                        dados_gols_total[time_mandante]['quantidade_jogos'] += 1
    
    medias_gols = {}
    for time in times_visitantes_especificados:
        if dados_gols_especificado[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_especificado[time]['soma_gols'] / dados_gols_especificado[time]['quantidade_jogos']
        elif dados_gols_total[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_total[time]['soma_gols'] / dados_gols_total[time]['quantidade_jogos']
        else:
            medias_gols[time] = 0
    
    return medias_gols

def get_media_gols_pro_visitantes(csv_filename, times_visitantes_especificados, ano_inicio, ano_fim):
    dados_gols_especificado = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    dados_gols_total = {time: {'soma_gols': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_visitante = row['time_visitante']
            ano_campeonato_str = row['ano_campeonato']
            if time_visitante in times_visitantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_visitante_str = row['gols_visitante']
                if gols_visitante_str.isdigit():
                    gols_visitante = int(gols_visitante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_gols_especificado[time_visitante]['soma_gols'] += gols_visitante
                        dados_gols_especificado[time_visitante]['quantidade_jogos'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_gols_total[time_visitante]['soma_gols'] += gols_visitante
                        dados_gols_total[time_visitante]['quantidade_jogos'] += 1
    
    medias_gols = {}
    for time in times_visitantes_especificados:
        if dados_gols_especificado[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_especificado[time]['soma_gols'] / dados_gols_especificado[time]['quantidade_jogos']
        elif dados_gols_total[time]['quantidade_jogos'] > 0:
            medias_gols[time] = dados_gols_total[time]['soma_gols'] / dados_gols_total[time]['quantidade_jogos']
        else:
            medias_gols[time] = 0
    
    return medias_gols

def get_percentual_vitorias_mandantes(csv_filename, times_mandantes_especificados, ano_inicio, ano_fim):
    dados_vitorias_especificado = {time: {'vitorias': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    dados_vitorias_total = {time: {'vitorias': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_mandante = row['time_mandante']
            ano_campeonato_str = row['ano_campeonato']
            if time_mandante in times_mandantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_mandante_str = row['gols_mandante']
                gols_visitante_str = row['gols_visitante']
                if gols_mandante_str.isdigit() and gols_visitante_str.isdigit():
                    gols_mandante = int(gols_mandante_str)
                    gols_visitante = int(gols_visitante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_vitorias_especificado[time_mandante]['quantidade_jogos'] += 1
                        if gols_mandante > gols_visitante:
                            dados_vitorias_especificado[time_mandante]['vitorias'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_vitorias_total[time_mandante]['quantidade_jogos'] += 1
                        if gols_mandante > gols_visitante:
                            dados_vitorias_total[time_mandante]['vitorias'] += 1
    
    percentual_vitorias = {}
    for time in times_mandantes_especificados:
        if dados_vitorias_especificado[time]['quantidade_jogos'] > 0:
            percentual_vitorias[time] = (dados_vitorias_especificado[time]['vitorias'] / dados_vitorias_especificado[time]['quantidade_jogos']) * 100
        elif dados_vitorias_total[time]['quantidade_jogos'] > 0:
            percentual_vitorias[time] = (dados_vitorias_total[time]['vitorias'] / dados_vitorias_total[time]['quantidade_jogos']) * 100
        else:
            percentual_vitorias[time] = 0.0
    
    return percentual_vitorias

def get_percentual_vitorias_visitantes(csv_filename, times_visitantes_especificados, ano_inicio, ano_fim):
    dados_vitorias_especificado = {time: {'vitorias': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    dados_vitorias_total = {time: {'vitorias': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_visitante = row['time_visitante']
            ano_campeonato_str = row['ano_campeonato']
            if time_visitante in times_visitantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_mandante_str = row['gols_mandante']
                gols_visitante_str = row['gols_visitante']
                if gols_mandante_str.isdigit() and gols_visitante_str.isdigit():
                    gols_mandante = int(gols_mandante_str)
                    gols_visitante = int(gols_visitante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_vitorias_especificado[time_visitante]['quantidade_jogos'] += 1
                        if gols_visitante > gols_mandante:
                            dados_vitorias_especificado[time_visitante]['vitorias'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_vitorias_total[time_visitante]['quantidade_jogos'] += 1
                        if gols_visitante > gols_mandante:
                            dados_vitorias_total[time_visitante]['vitorias'] += 1
    
    percentual_vitorias = {}
    for time in times_visitantes_especificados:
        if dados_vitorias_especificado[time]['quantidade_jogos'] > 0:
            percentual_vitorias[time] = (dados_vitorias_especificado[time]['vitorias'] / dados_vitorias_especificado[time]['quantidade_jogos']) * 100
        elif dados_vitorias_total[time]['quantidade_jogos'] > 0:
            percentual_vitorias[time] = (dados_vitorias_total[time]['vitorias'] / dados_vitorias_total[time]['quantidade_jogos']) * 100
        else:
            percentual_vitorias[time] = 0.0
    
    return percentual_vitorias

def get_percentual_derrotas_mandantes(csv_filename, times_mandantes_especificados, ano_inicio, ano_fim):
    dados_derrotas_especificado = {time: {'derrotas': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    dados_derrotas_total = {time: {'derrotas': 0, 'quantidade_jogos': 0} for time in times_mandantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_mandante = row['time_mandante']
            ano_campeonato_str = row['ano_campeonato']
            if time_mandante in times_mandantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_mandante_str = row['gols_mandante']
                gols_visitante_str = row['gols_visitante']
                if gols_mandante_str.isdigit() and gols_visitante_str.isdigit():
                    gols_mandante = int(gols_mandante_str)
                    gols_visitante = int(gols_visitante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_derrotas_especificado[time_mandante]['quantidade_jogos'] += 1
                        if gols_mandante < gols_visitante:
                            dados_derrotas_especificado[time_mandante]['derrotas'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_derrotas_total[time_mandante]['quantidade_jogos'] += 1
                        if gols_mandante < gols_visitante:
                            dados_derrotas_total[time_mandante]['derrotas'] += 1
    
    percentual_derrotas = {}
    for time in times_mandantes_especificados:
        if dados_derrotas_especificado[time]['quantidade_jogos'] > 0:
            percentual_derrotas[time] = (dados_derrotas_especificado[time]['derrotas'] / dados_derrotas_especificado[time]['quantidade_jogos']) * 100
        elif dados_derrotas_total[time]['quantidade_jogos'] > 0:
            percentual_derrotas[time] = (dados_derrotas_total[time]['derrotas'] / dados_derrotas_total[time]['quantidade_jogos']) * 100
        else:
            percentual_derrotas[time] = 0.0
    
    return percentual_derrotas

def get_percentual_derrotas_visitantes(csv_filename, times_visitantes_especificados, ano_inicio, ano_fim):
    dados_derrotas_especificado = {time: {'derrotas': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    dados_derrotas_total = {time: {'derrotas': 0, 'quantidade_jogos': 0} for time in times_visitantes_especificados}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            time_visitante = row['time_visitante']
            ano_campeonato_str = row['ano_campeonato']
            if time_visitante in times_visitantes_especificados and ano_campeonato_str.isdigit():
                ano_campeonato = int(ano_campeonato_str)
                gols_mandante_str = row['gols_mandante']
                gols_visitante_str = row['gols_visitante']
                if gols_mandante_str.isdigit() and gols_visitante_str.isdigit():
                    gols_mandante = int(gols_mandante_str)
                    gols_visitante = int(gols_visitante_str)
                    if ano_inicio <= ano_campeonato <= ano_fim:
                        dados_derrotas_especificado[time_visitante]['quantidade_jogos'] += 1
                        if gols_visitante < gols_mandante:
                            dados_derrotas_especificado[time_visitante]['derrotas'] += 1
                    if 2003 <= ano_campeonato <= 2023:
                        dados_derrotas_total[time_visitante]['quantidade_jogos'] += 1
                        if gols_visitante < gols_mandante:
                            dados_derrotas_total[time_visitante]['derrotas'] += 1
    
    percentual_derrotas = {}
    for time in times_visitantes_especificados:
        if dados_derrotas_especificado[time]['quantidade_jogos'] > 0:
            percentual_derrotas[time] = (dados_derrotas_especificado[time]['derrotas'] / dados_derrotas_especificado[time]['quantidade_jogos']) * 100
        elif dados_derrotas_total[time]['quantidade_jogos'] > 0:
            percentual_derrotas[time] = (dados_derrotas_total[time]['derrotas'] / dados_derrotas_total[time]['quantidade_jogos']) * 100
        else:
            percentual_derrotas[time] = 0.0
    
    return percentual_derrotas

def get_percentual_vitorias_colocacao_mandantes(csv_filename):
    # Dicionário para armazenar contagens de jogos e vitórias dos mandantes
    vitorias_por_colocacao = defaultdict(lambda: {'jogos': 0, 'vitorias': 0})

    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            gols_mandante_str = row['gols_mandante']
            gols_visitante_str = row['gols_visitante']
            
            # Verifica se os gols são números válidos
            if gols_mandante_str.isdigit() and gols_visitante_str.isdigit():
                gols_mandante = int(gols_mandante_str)
                gols_visitante = int(gols_visitante_str)
                
                # Verifica se a linha tem os dados de colocação
                if 'colocacao_mandante' in row and 'colocacao_visitante' in row:
                    colocacao_mandante = row['colocacao_mandante']
                    colocacao_visitante = row['colocacao_visitante']
                    
                    # Verifica se os dados de colocação não estão vazios
                    if colocacao_mandante and colocacao_visitante:
                        key = (int(colocacao_mandante), int(colocacao_visitante))
                        vitorias_por_colocacao[key]['jogos'] += 1
                        if gols_mandante > gols_visitante:
                            vitorias_por_colocacao[key]['vitorias'] += 1
    
    # Calcular as porcentagens de vitórias dos mandantes para cada combinação de colocações
    porcentagens_vitorias = {}
    for (colocacao_mandante, colocacao_visitante), dados in vitorias_por_colocacao.items():
        if dados['jogos'] > 0:
            porcentagem = (dados['vitorias'] / dados['jogos']) * 100
            porcentagens_vitorias[(colocacao_mandante, colocacao_visitante)] = porcentagem
    
    return porcentagens_vitorias

def get_percentual_vitorias_colocacao_visitantes(csv_filename):
    # Dicionário para armazenar contagens de jogos e vitórias dos visitantes
    vitorias_por_colocacao = defaultdict(lambda: {'jogos': 0, 'vitorias': 0})

    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            gols_mandante_str = row['gols_mandante']
            gols_visitante_str = row['gols_visitante']
            
            # Verifica se os gols são números válidos
            if gols_mandante_str.isdigit() and gols_visitante_str.isdigit():
                gols_mandante = int(gols_mandante_str)
                gols_visitante = int(gols_visitante_str)
                
                # Verifica se a linha tem os dados de colocação
                if 'colocacao_mandante' in row and 'colocacao_visitante' in row:
                    colocacao_mandante = row['colocacao_mandante']
                    colocacao_visitante = row['colocacao_visitante']
                    
                    # Verifica se os dados de colocação não estão vazios
                    if colocacao_mandante and colocacao_visitante:
                        key = (int(colocacao_mandante), int(colocacao_visitante))
                        vitorias_por_colocacao[key]['jogos'] += 1
                        if gols_visitante > gols_mandante:  # Mudança: Comparação de gols do visitante com gols do mandante
                            vitorias_por_colocacao[key]['vitorias'] += 1
    
    # Calcular as porcentagens de vitórias dos visitantes para cada combinação de colocações
    porcentagens_vitorias = {}
    for (colocacao_mandante, colocacao_visitante), dados in vitorias_por_colocacao.items():
        if dados['jogos'] > 0:
            porcentagem = (dados['vitorias'] / dados['jogos']) * 100
            porcentagens_vitorias[(colocacao_mandante, colocacao_visitante)] = porcentagem
    
    return porcentagens_vitorias

# Variáveis globais
TIMES = [
    'Atlético-GO', 'Atlético-MG', 'Athletico-PR', 'EC Bahia', 'Botafogo', 
    'RB Bragantino', 'Corinthians', 'Criciúma EC', 'Cruzeiro', 'Cuiabá-MT', 
    'Flamengo', 'Fluminense', 'Fortaleza', 'Grêmio', 'Internacional', 
    'Juventude', 'Palmeiras', 'São Paulo', 'Vasco da Gama', 'EC Vitória'
]
VALORES_EQUIPES_2024 = {
    'Flamengo': 166, 'EC Bahia': 61, 'Botafogo': 70, 'São Paulo': 90, 'Athletico-PR': 67,
    'RB Bragantino': 75, 'Palmeiras': 220, 'Internacional': 96, 'Cruzeiro': 67, 'Atlético-MG': 86,
    'Fortaleza': 42, 'Grêmio': 76, 'Vasco da Gama': 69, 'Juventude': 17, 'Fluminense': 110,
    'Criciúma EC': 16, 'Corinthians': 109, 'Atlético-GO': 22, 'EC Vitória': 26, 'Cuiabá-MT': 27
}
IDADES_EQUIPES_2024 = {
    'Flamengo': 26, 'EC Bahia': 28.3, 'Botafogo': 26.9, 'São Paulo': 26.4, 'Athletico-PR': 25.2,
    'RB Bragantino': 24.1, 'Palmeiras': 25.4, 'Internacional': 27.9, 'Cruzeiro': 25.8, 'Atlético-MG': 26,
    'Fortaleza': 28.5, 'Grêmio': 27.3, 'Vasco da Gama': 26.8, 'Juventude': 26.9, 'Fluminense': 28,
    'Criciúma EC': 28, 'Corinthians': 24.8, 'Atlético-GO': 26.2, 'EC Vitória': 28.3, 'Cuiabá-MT': 25.9
}
CONFRONTOS = get_confrontos()

ano_inicio = 2018
ano_fim = 2023

MEDIA_GOLS_PRO_MANDANTES = get_media_gols_pro_mandantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
MEDIA_GOLS_CONTRA_VISITANTES = get_media_gols_contra_visitantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
MEDIA_GOLS_CONTRA_MANDANTES = get_media_gols_contra_mandantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
MEDIA_GOLS_PRO_VISITANTES = get_media_gols_pro_visitantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
PERCENTUAL_VITORIAS_MANDANTES = get_percentual_vitorias_mandantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
PERCENTUAL_DERROTAS_MANDANTES = get_percentual_derrotas_mandantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
PERCENTUAL_VITORIAS_VISITANTES = get_percentual_vitorias_visitantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
PERCENTUAL_DERROTAS_VISITANTES = get_percentual_derrotas_visitantes(CSV_DATASET, TIMES, ano_inicio, ano_fim)
PERCENTUAL_VITORIAS_COLOCACAO_MANDANTES =  get_percentual_vitorias_colocacao_mandantes(CSV_DATASET)
PERCENTUAL_VITORIAS_COLOCACAO_VISITANTES =  get_percentual_vitorias_colocacao_visitantes(CSV_DATASET)

# Variáveis fuzzy
valor_equipe_mandante = ctrl.Antecedent(np.arange(0, 221, 1), 'valor_equipe_mandante')
valor_equipe_visitante = ctrl.Antecedent(np.arange(0, 221, 1), 'valor_equipe_visitante')
idade_media_mandante = ctrl.Antecedent(np.arange(20, 31, 0.1), 'idade_media_mandante')
idade_media_visitante = ctrl.Antecedent(np.arange(20, 31, 0.1), 'idade_media_visitante')
media_gols_pro_mandante = ctrl.Antecedent(np.arange(0, 2.2, 0.05), 'media_gols_pro_mandante')
media_gols_contra_visitante = ctrl.Antecedent(np.arange(0, 3.5, 0.05), 'media_gols_contra_visitante')
media_gols_contra_mandante = ctrl.Antecedent(np.arange(0, 2, 0.05), 'media_gols_contra_mandante')
media_gols_pro_visitante = ctrl.Antecedent(np.arange(0, 1.4, 0.05), 'media_gols_pro_visitante')
percentual_vitorias_mandante = ctrl.Antecedent(np.arange(0, 76, 0.5), 'percentual_vitorias_mandante')
percentual_derrotas_mandante = ctrl.Antecedent(np.arange(0, 51, 0.5), 'percentual_derrotas_mandante')
percentual_vitorias_visitante = ctrl.Antecedent(np.arange(0, 41, 0.5), 'percentual_vitorias_visitante')
percentual_derrotas_visitante = ctrl.Antecedent(np.arange(0, 76, 0.5), 'percentual_derrotas_visitante')
percentual_vitorias_colocacao_mandante = ctrl.Antecedent(np.arange(0, 101, 0.5), 'percentual_vitorias_colocacao_mandante')
percentual_vitorias_colocacao_visitante = ctrl.Antecedent(np.arange(0, 76, 0.5), 'percentual_vitorias_colocacao_visitante')

gols = ctrl.Consequent(np.arange(0, 8, 1), 'gols')

# Funções de pertinência para valor da equipe mandante
valor_equipe_mandante['baixo'] = fuzz.trimf(valor_equipe_mandante.universe, [0, 30, 70])
valor_equipe_mandante['medio'] = fuzz.trimf(valor_equipe_mandante.universe, [40, 100, 110])
valor_equipe_mandante['alto'] = fuzz.trimf(valor_equipe_mandante.universe, [90, 150, 220])

# Funções de pertinência para valor da equipe visitante
valor_equipe_visitante['baixo'] = fuzz.trimf(valor_equipe_visitante.universe, [0, 30, 70])
valor_equipe_visitante['medio'] = fuzz.trimf(valor_equipe_visitante.universe, [40, 100, 110])
valor_equipe_visitante['alto'] = fuzz.trimf(valor_equipe_visitante.universe, [90, 150, 220])

# Funções de pertinência para idade média mandante
idade_media_mandante['jovem'] = fuzz.trimf(idade_media_mandante.universe, [20, 20, 23])
idade_media_mandante['media'] = fuzz.trimf(idade_media_mandante.universe, [23, 25, 27])
idade_media_mandante['experiente'] = fuzz.trimf(idade_media_mandante.universe, [26, 29, 31])

# Funções de pertinência para idade média visitante
idade_media_visitante['jovem'] = fuzz.trimf(idade_media_visitante.universe, [20, 20, 23])
idade_media_visitante['media'] = fuzz.trimf(idade_media_visitante.universe, [23, 25, 27])
idade_media_visitante['experiente'] = fuzz.trimf(idade_media_visitante.universe, [26, 29, 31])

# Funções de pertinência para media gols pro mandante
media_gols_pro_mandante['baixa'] = fuzz.trimf(media_gols_pro_mandante.universe, [0, 0.6, 1.2])
media_gols_pro_mandante['media'] = fuzz.trimf(media_gols_pro_mandante.universe, [1, 1.5, 1.8])
media_gols_pro_mandante['alta'] = fuzz.trimf(media_gols_pro_mandante.universe, [1.5, 1.85, 2.2])

# Funções de pertinência para media gols contra visitante
media_gols_contra_visitante['baixa'] = fuzz.trimf(media_gols_contra_visitante.universe, [0, 1, 1.5])
media_gols_contra_visitante['media'] = fuzz.trimf(media_gols_contra_visitante.universe, [1.3, 1.7, 2])
media_gols_contra_visitante['alta'] = fuzz.trimf(media_gols_contra_visitante.universe, [1.7, 2.2, 3.5])

# Funções de pertinência para media gols contra mandante
media_gols_contra_mandante['baixa'] = fuzz.trimf(media_gols_contra_mandante.universe, [0, 0.6, 1])
media_gols_contra_mandante['media'] = fuzz.trimf(media_gols_contra_mandante.universe, [0.9, 1.1, 1.2])
media_gols_contra_mandante['alta'] = fuzz.trimf(media_gols_contra_mandante.universe, [1.15, 1.4, 2])

# Funções de pertinência para media gols pro visitante
media_gols_pro_visitante['baixa'] = fuzz.trimf(media_gols_pro_visitante.universe, [0, 0.4, 1])
media_gols_pro_visitante['media'] = fuzz.trimf(media_gols_pro_visitante.universe, [0.85, 1, 1.1])
media_gols_pro_visitante['alta'] = fuzz.trimf(media_gols_pro_visitante.universe, [1, 1.2, 1.4])

# Funções de pertinência para percentual vitorias mandante
percentual_vitorias_mandante['baixo'] = fuzz.trimf(percentual_vitorias_mandante.universe, [0, 32, 46])
percentual_vitorias_mandante['medio'] = fuzz.trimf(percentual_vitorias_mandante.universe, [35, 50, 60])
percentual_vitorias_mandante['alto'] = fuzz.trimf(percentual_vitorias_mandante.universe, [52, 60, 75])

# Funções de pertinência para percentual derrotas mandante
percentual_derrotas_mandante['baixo'] = fuzz.trimf(percentual_derrotas_mandante.universe, [0, 14, 18])
percentual_derrotas_mandante['medio'] = fuzz.trimf(percentual_derrotas_mandante.universe, [14, 24, 30])
percentual_derrotas_mandante['alto'] = fuzz.trimf(percentual_derrotas_mandante.universe, [27, 38, 50])

# Funções de pertinência para percentual vitorias visitante
percentual_vitorias_visitante['baixo'] = fuzz.trimf(percentual_vitorias_visitante.universe, [0, 15, 20])
percentual_vitorias_visitante['medio'] = fuzz.trimf(percentual_vitorias_visitante.universe, [18, 25, 30])
percentual_vitorias_visitante['alto'] = fuzz.trimf(percentual_vitorias_visitante.universe, [28, 34, 40])

# Funções de pertinência para percentual derrotas visitante
percentual_derrotas_visitante['baixo'] = fuzz.trimf(percentual_derrotas_visitante.universe, [0, 39, 43])
percentual_derrotas_visitante['medio'] = fuzz.trimf(percentual_derrotas_visitante.universe, [39, 45, 52])
percentual_derrotas_visitante['alto'] = fuzz.trimf(percentual_derrotas_visitante.universe, [50, 66, 75])

# Funções de pertinência para percentual vitorias por colocção mandante
percentual_vitorias_colocacao_mandante['baixo'] = fuzz.trimf(percentual_vitorias_colocacao_mandante.universe, [0, 15, 40])
percentual_vitorias_colocacao_mandante['medio'] = fuzz.trimf(percentual_vitorias_colocacao_mandante.universe, [38, 50, 65])
percentual_vitorias_colocacao_mandante['alto'] = fuzz.trimf(percentual_vitorias_colocacao_mandante.universe, [60, 85, 100])

# Funções de pertinência para percentual vitorias por colocção visitante
percentual_vitorias_colocacao_visitante['baixo'] = fuzz.trimf(percentual_vitorias_colocacao_visitante.universe, [0, 15, 24])
percentual_vitorias_colocacao_visitante['medio'] = fuzz.trimf(percentual_vitorias_colocacao_visitante.universe, [17, 24, 32])
percentual_vitorias_colocacao_visitante['alto'] = fuzz.trimf(percentual_vitorias_colocacao_visitante.universe, [30, 69, 75])

# Funções de pertinência para gols
gols['poucos'] = fuzz.trimf(gols.universe, [0, 0, 2])
gols['moderados'] = fuzz.trimf(gols.universe, [0, 2, 4])
gols['muitos'] = fuzz.trimf(gols.universe, [3, 4, 7])


# Definir regras fuzzy
# Valor equipe - gols mandante
rule1 = ctrl.Rule(valor_equipe_mandante['alto'] & valor_equipe_visitante['alto'], gols['poucos'])
rule2 = ctrl.Rule(valor_equipe_mandante['alto'] & valor_equipe_visitante['medio'], gols['moderados'])
rule3 = ctrl.Rule(valor_equipe_mandante['alto'] & valor_equipe_visitante['baixo'], gols['muitos'])

rule4 = ctrl.Rule(valor_equipe_mandante['medio'] & valor_equipe_visitante['alto'], gols['poucos'])
rule5 = ctrl.Rule(valor_equipe_mandante['medio'] & valor_equipe_visitante['medio'], gols['poucos'])
rule6 = ctrl.Rule(valor_equipe_mandante['medio'] & valor_equipe_visitante['baixo'], gols['moderados'])

rule7 = ctrl.Rule(valor_equipe_mandante['baixo'] & valor_equipe_visitante['alto'], gols['poucos'])
rule8 = ctrl.Rule(valor_equipe_mandante['baixo'] & valor_equipe_visitante['medio'], gols['poucos'])
rule9 = ctrl.Rule(valor_equipe_mandante['baixo'] & valor_equipe_visitante['baixo'], gols['poucos'])

# Valor equipe - gols visitante
rule10 = ctrl.Rule(valor_equipe_mandante['alto'] & valor_equipe_visitante['alto'], gols['poucos'])
rule11 = ctrl.Rule(valor_equipe_mandante['alto'] & valor_equipe_visitante['medio'], gols['poucos'])
rule12 = ctrl.Rule(valor_equipe_mandante['alto'] & valor_equipe_visitante['baixo'], gols['poucos'])

rule13 = ctrl.Rule(valor_equipe_mandante['medio'] & valor_equipe_visitante['alto'], gols['moderados'])
rule14 = ctrl.Rule(valor_equipe_mandante['medio'] & valor_equipe_visitante['medio'], gols['poucos'])
rule15 = ctrl.Rule(valor_equipe_mandante['medio'] & valor_equipe_visitante['baixo'], gols['poucos'])

rule16 = ctrl.Rule(valor_equipe_mandante['baixo'] & valor_equipe_visitante['alto'], gols['muitos'])
rule17 = ctrl.Rule(valor_equipe_mandante['baixo'] & valor_equipe_visitante['medio'], gols['moderados'])
rule18 = ctrl.Rule(valor_equipe_mandante['baixo'] & valor_equipe_visitante['baixo'], gols['poucos'])

# Idade media - gols mandante
rule19 = ctrl.Rule(idade_media_mandante['experiente'] & idade_media_visitante['experiente'], gols['poucos'])
rule20 = ctrl.Rule(idade_media_mandante['experiente'] & idade_media_visitante['media'], gols['poucos'])
rule21 = ctrl.Rule(idade_media_mandante['experiente'] & idade_media_visitante['jovem'], gols['moderados'])

rule22 = ctrl.Rule(idade_media_mandante['media'] & idade_media_visitante['experiente'], gols['moderados'])
rule23 = ctrl.Rule(idade_media_mandante['media'] & idade_media_visitante['media'], gols['poucos'])
rule24 = ctrl.Rule(idade_media_mandante['media'] & idade_media_visitante['jovem'], gols['moderados'])

rule25 = ctrl.Rule(idade_media_mandante['jovem'] & idade_media_visitante['experiente'], gols['moderados'])
rule26 = ctrl.Rule(idade_media_mandante['jovem'] & idade_media_visitante['media'], gols['poucos'])
rule27 = ctrl.Rule(idade_media_mandante['jovem'] & idade_media_visitante['jovem'], gols['poucos'])

# Idade media - gols visitante
rule28 = ctrl.Rule(idade_media_mandante['experiente'] & idade_media_visitante['experiente'], gols['poucos'])
rule29 = ctrl.Rule(idade_media_mandante['experiente'] & idade_media_visitante['media'], gols['moderados'])
rule30 = ctrl.Rule(idade_media_mandante['experiente'] & idade_media_visitante['jovem'], gols['moderados'])

rule31 = ctrl.Rule(idade_media_mandante['media'] & idade_media_visitante['experiente'], gols['poucos'])
rule32 = ctrl.Rule(idade_media_mandante['media'] & idade_media_visitante['media'], gols['poucos'])
rule33 = ctrl.Rule(idade_media_mandante['media'] & idade_media_visitante['jovem'], gols['poucos'])

rule34 = ctrl.Rule(idade_media_mandante['jovem'] & idade_media_visitante['experiente'], gols['moderados'])
rule35 = ctrl.Rule(idade_media_mandante['jovem'] & idade_media_visitante['media'], gols['moderados'])
rule36 = ctrl.Rule(idade_media_mandante['jovem'] & idade_media_visitante['jovem'], gols['poucos'])

# Media gols - gols mandante
rule37 = ctrl.Rule(media_gols_pro_mandante['alta'] & media_gols_contra_visitante['alta'], gols['muitos'])
rule38 = ctrl.Rule(media_gols_pro_mandante['alta'] & media_gols_contra_visitante['media'], gols['moderados'])
rule39 = ctrl.Rule(media_gols_pro_mandante['alta'] & media_gols_contra_visitante['baixa'], gols['poucos'])

rule40 = ctrl.Rule(media_gols_pro_mandante['media'] & media_gols_contra_visitante['alta'], gols['moderados'])
rule41 = ctrl.Rule(media_gols_pro_mandante['media'] & media_gols_contra_visitante['media'], gols['moderados'])
rule42 = ctrl.Rule(media_gols_pro_mandante['media'] & media_gols_contra_visitante['baixa'], gols['poucos'])

rule43 = ctrl.Rule(media_gols_pro_mandante['baixa'] & media_gols_contra_visitante['alta'], gols['moderados'])
rule44 = ctrl.Rule(media_gols_pro_mandante['baixa'] & media_gols_contra_visitante['media'], gols['poucos'])
rule45 = ctrl.Rule(media_gols_pro_mandante['baixa'] & media_gols_contra_visitante['baixa'], gols['poucos'])

# Media gols - gols visitantes
rule46 = ctrl.Rule(media_gols_contra_mandante['alta'] & media_gols_pro_visitante['alta'], gols['muitos'])
rule47 = ctrl.Rule(media_gols_contra_mandante['alta'] & media_gols_pro_visitante['media'], gols['moderados'])
rule48 = ctrl.Rule(media_gols_contra_mandante['alta'] & media_gols_pro_visitante['baixa'], gols['moderados'])

rule49 = ctrl.Rule(media_gols_contra_mandante['media'] & media_gols_pro_visitante['alta'], gols['moderados'])
rule50 = ctrl.Rule(media_gols_contra_mandante['media'] & media_gols_pro_visitante['media'], gols['moderados'])
rule51 = ctrl.Rule(media_gols_contra_mandante['media'] & media_gols_pro_visitante['baixa'], gols['poucos'])

rule52 = ctrl.Rule(media_gols_contra_mandante['baixa'] & media_gols_pro_visitante['alta'], gols['poucos'])
rule53 = ctrl.Rule(media_gols_contra_mandante['baixa'] & media_gols_pro_visitante['media'], gols['poucos'])
rule54 = ctrl.Rule(media_gols_contra_mandante['baixa'] & media_gols_pro_visitante['baixa'], gols['poucos'])

# Percentual vitorias mandante - gols mandante
rule55 = ctrl.Rule(percentual_vitorias_mandante['alto'] & percentual_derrotas_visitante['alto'], gols['muitos'])
rule56 = ctrl.Rule(percentual_vitorias_mandante['alto'] & percentual_derrotas_visitante['medio'], gols['moderados'])
rule57 = ctrl.Rule(percentual_vitorias_mandante['alto'] & percentual_derrotas_visitante['baixo'], gols['poucos'])

rule58 = ctrl.Rule(percentual_vitorias_mandante['medio'] & percentual_derrotas_visitante['alto'], gols['moderados'])
rule59 = ctrl.Rule(percentual_vitorias_mandante['medio'] & percentual_derrotas_visitante['medio'], gols['poucos'])
rule60 = ctrl.Rule(percentual_vitorias_mandante['medio'] & percentual_derrotas_visitante['baixo'], gols['poucos'])

rule61 = ctrl.Rule(percentual_vitorias_mandante['baixo'] & percentual_derrotas_visitante['alto'], gols['moderados'])
rule62 = ctrl.Rule(percentual_vitorias_mandante['baixo'] & percentual_derrotas_visitante['medio'], gols['poucos'])
rule63 = ctrl.Rule(percentual_vitorias_mandante['baixo'] & percentual_derrotas_visitante['baixo'], gols['poucos'])

# Percentual vitorias visitante - gols visitantes
rule64 = ctrl.Rule(percentual_derrotas_mandante['alto'] & percentual_vitorias_visitante['alto'], gols['moderados'])
rule65 = ctrl.Rule(percentual_derrotas_mandante['alto'] & percentual_vitorias_visitante['medio'], gols['moderados'])
rule66 = ctrl.Rule(percentual_derrotas_mandante['alto'] & percentual_vitorias_visitante['baixo'], gols['poucos'])

rule67 = ctrl.Rule(percentual_derrotas_mandante['medio'] & percentual_vitorias_visitante['alto'], gols['moderados'])
rule68 = ctrl.Rule(percentual_derrotas_mandante['medio'] & percentual_vitorias_visitante['medio'], gols['poucos'])
rule69 = ctrl.Rule(percentual_derrotas_mandante['medio'] & percentual_vitorias_visitante['baixo'], gols['poucos'])

rule70 = ctrl.Rule(percentual_derrotas_mandante['baixo'] & percentual_vitorias_visitante['alto'], gols['poucos'])
rule71 = ctrl.Rule(percentual_derrotas_mandante['baixo'] & percentual_vitorias_visitante['medio'], gols['poucos'])
rule72 = ctrl.Rule(percentual_derrotas_mandante['baixo'] & percentual_vitorias_visitante['baixo'], gols['poucos'])

# Percentual vitorias colocação - gols mandantes
rule73 = ctrl.Rule(percentual_vitorias_colocacao_mandante['alto'] & percentual_vitorias_colocacao_visitante['alto'], gols['poucos'])
rule74 = ctrl.Rule(percentual_vitorias_colocacao_mandante['alto'] & percentual_vitorias_colocacao_visitante['medio'], gols['moderados'])
rule75 = ctrl.Rule(percentual_vitorias_colocacao_mandante['alto'] & percentual_vitorias_colocacao_visitante['baixo'], gols['muitos'])

rule76 = ctrl.Rule(percentual_vitorias_colocacao_mandante['medio'] & percentual_vitorias_colocacao_visitante['alto'], gols['poucos'])
rule77 = ctrl.Rule(percentual_vitorias_colocacao_mandante['medio'] & percentual_vitorias_colocacao_visitante['medio'], gols['poucos'])
rule78 = ctrl.Rule(percentual_vitorias_colocacao_mandante['medio'] & percentual_vitorias_colocacao_visitante['baixo'], gols['moderados'])

rule79 = ctrl.Rule(percentual_vitorias_colocacao_mandante['baixo'] & percentual_vitorias_colocacao_visitante['alto'], gols['poucos'])
rule80 = ctrl.Rule(percentual_vitorias_colocacao_mandante['baixo'] & percentual_vitorias_colocacao_visitante['medio'], gols['poucos'])
rule81 = ctrl.Rule(percentual_vitorias_colocacao_mandante['baixo'] & percentual_vitorias_colocacao_visitante['baixo'], gols['poucos'])

# Percentual vitorias colocação - gols visitantes
rule82 = ctrl.Rule(percentual_vitorias_colocacao_mandante['alto'] & percentual_vitorias_colocacao_visitante['alto'], gols['poucos'])
rule83 = ctrl.Rule(percentual_vitorias_colocacao_mandante['alto'] & percentual_vitorias_colocacao_visitante['medio'], gols['poucos'])
rule84 = ctrl.Rule(percentual_vitorias_colocacao_mandante['alto'] & percentual_vitorias_colocacao_visitante['baixo'], gols['poucos'])

rule85 = ctrl.Rule(percentual_vitorias_colocacao_mandante['medio'] & percentual_vitorias_colocacao_visitante['alto'], gols['poucos'])
rule86 = ctrl.Rule(percentual_vitorias_colocacao_mandante['medio'] & percentual_vitorias_colocacao_visitante['medio'], gols['poucos'])
rule87 = ctrl.Rule(percentual_vitorias_colocacao_mandante['medio'] & percentual_vitorias_colocacao_visitante['baixo'], gols['poucos'])

rule88 = ctrl.Rule(percentual_vitorias_colocacao_mandante['baixo'] & percentual_vitorias_colocacao_visitante['alto'], gols['moderados'])
rule89 = ctrl.Rule(percentual_vitorias_colocacao_mandante['baixo'] & percentual_vitorias_colocacao_visitante['medio'], gols['poucos'])
rule90 = ctrl.Rule(percentual_vitorias_colocacao_mandante['baixo'] & percentual_vitorias_colocacao_visitante['baixo'], gols['poucos'])


# Sistema de controle fuzzy mandante
sistema_controle_mandante = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45, rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63, rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80, rule81])
previsao_gols_mandante = ctrl.ControlSystemSimulation(sistema_controle_mandante)
previsao_gols_mandante.defuzzify_method = 'centroid'

# Sistema de controle fuzzy visitante
sistema_controle_visitante = ctrl.ControlSystem([rule10, rule11, rule12, rule13, rule14, rule14, rule15, rule16, rule17, rule18, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54, rule64, rule65, rule66, rule67, rule68, rule69, rule70, rule71, rule72, rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89, rule90])
previsao_gols_visitante = ctrl.ControlSystemSimulation(sistema_controle_visitante)
previsao_gols_visitante.defuzzify_method = 'centroid'


resultados = {time: 0 for time in TIMES}
rodada_atual = '1'
colocacoes = {
    'Atlético-GO': 1, 'Atlético-MG': 2, 'Athletico-PR': 3, 'Botafogo': 4, 'Corinthians': 5, 'Criciúma EC': 6, 'Cruzeiro': 7, 'Cuiabá-MT': 8, 
    'EC Bahia': 9, 'EC Vitória': 10, 'Flamengo': 11, 'Fluminense': 12, 'Fortaleza': 13, 'Grêmio': 14, 'Internacional': 15, 'Juventude': 16, 
    'Palmeiras': 17, 'RB Bragantino': 18, 'São Paulo': 19, 'Vasco da Gama': 20
}

# Simulação das partidas
for confronto in CONFRONTOS:
    rodada = confronto['rodada']
    time_mandante = confronto['time_mandante']
    time_visitante = confronto['time_visitante']

    # Armazena as colocações do campeonato
    if rodada != rodada_atual:
        resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        colocacoes = {time: i + 1 for i, (time, _) in enumerate(resultados_ordenados)}
        rodada_atual = rodada

    # Simulando gols do time mandante
    previsao_gols_mandante.input['valor_equipe_mandante'] = VALORES_EQUIPES_2024[time_mandante]
    previsao_gols_mandante.input['valor_equipe_visitante'] = VALORES_EQUIPES_2024[time_visitante]
    previsao_gols_mandante.input['idade_media_mandante'] = IDADES_EQUIPES_2024[time_mandante]
    previsao_gols_mandante.input['idade_media_visitante'] = IDADES_EQUIPES_2024[time_visitante]

    previsao_gols_mandante.input['media_gols_pro_mandante'] = MEDIA_GOLS_PRO_MANDANTES[time_mandante]
    previsao_gols_mandante.input['media_gols_contra_visitante'] = MEDIA_GOLS_CONTRA_VISITANTES[time_visitante]

    previsao_gols_mandante.input['percentual_vitorias_mandante'] = PERCENTUAL_VITORIAS_MANDANTES[time_mandante]
    previsao_gols_mandante.input['percentual_derrotas_visitante'] = PERCENTUAL_DERROTAS_VISITANTES[time_visitante]

    previsao_gols_mandante.input['percentual_vitorias_colocacao_mandante'] = get_percentual_colocacao(time_mandante, time_visitante, colocacoes, PERCENTUAL_VITORIAS_COLOCACAO_MANDANTES)
    previsao_gols_mandante.input['percentual_vitorias_colocacao_visitante'] = get_percentual_colocacao(time_mandante, time_visitante, colocacoes, PERCENTUAL_VITORIAS_COLOCACAO_VISITANTES)

    previsao_gols_mandante.compute()
    
    # Simulando gols do time visitante
    previsao_gols_visitante.input['valor_equipe_mandante'] = VALORES_EQUIPES_2024[time_mandante]
    previsao_gols_visitante.input['valor_equipe_visitante'] = VALORES_EQUIPES_2024[time_visitante]
    previsao_gols_visitante.input['idade_media_mandante'] = IDADES_EQUIPES_2024[time_mandante]
    previsao_gols_visitante.input['idade_media_visitante'] = IDADES_EQUIPES_2024[time_visitante]

    previsao_gols_visitante.input['media_gols_contra_mandante'] = MEDIA_GOLS_CONTRA_MANDANTES[time_mandante]
    previsao_gols_visitante.input['media_gols_pro_visitante'] = MEDIA_GOLS_PRO_VISITANTES[time_visitante]

    previsao_gols_visitante.input['percentual_derrotas_mandante'] = PERCENTUAL_DERROTAS_MANDANTES[time_mandante]
    previsao_gols_visitante.input['percentual_vitorias_visitante'] = PERCENTUAL_VITORIAS_VISITANTES[time_visitante]

    previsao_gols_mandante.input['percentual_vitorias_colocacao_mandante'] = get_percentual_colocacao(time_mandante, time_visitante, colocacoes, PERCENTUAL_VITORIAS_COLOCACAO_MANDANTES)
    previsao_gols_mandante.input['percentual_vitorias_colocacao_visitante'] = get_percentual_colocacao(time_mandante, time_visitante, colocacoes, PERCENTUAL_VITORIAS_COLOCACAO_VISITANTES)

    previsao_gols_visitante.compute()
    
    # Resultado da simulação
    gols_mandante_simulados = round(previsao_gols_mandante.output['gols'], 2)
    gols_visitante_simulados = round(previsao_gols_visitante.output['gols'], 2)
    
    # Atualização dos pontos
    if gols_mandante_simulados > 0.4 + gols_visitante_simulados:
        resultados[time_mandante] += 3
    elif gols_mandante_simulados + 0.4 < gols_visitante_simulados:
        resultados[time_visitante] += 3
    else:
        resultados[time_mandante] += 1
        resultados[time_visitante] += 1

# Determinação do campeão
campeao = max(resultados, key=resultados.get)

# Ordenação dos resultados
resultados_ordenados = dict(sorted(resultados.items(), key=lambda item: item[1], reverse=True))

# Exibição da tabela final
print("Tabela Final do Campeonato Brasileiro 2024:")
for time, pontos in resultados_ordenados.items():
    print(f"{time}: {pontos} pontos")

print("\nO campeão do Campeonato Brasileiro 2024 é:", campeao)
print("Pontuação final:", resultados[campeao])
