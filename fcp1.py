import csv
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

CSV_DATASET = 'brasileirao_serie_a.csv'

# Funções auxiliares
def get_media_gols_pro_mandante(csv_filename, times_mandantes_especificados, ano_inicio, ano_fim):
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

def get_media_gols_contra_visitante(csv_filename, times_mandantes_especificados, ano_inicio, ano_fim):
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

def get_media_gols_contra_mandante(csv_filename, times_visitantes_especificados, ano_inicio, ano_fim):
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

def get_media_gols_pro_visitante(csv_filename, times_visitantes_especificados, ano_inicio, ano_fim):
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

ano_inicio = 2006
ano_fim = 2009

MEDIA_GOLS_PRO_MANDANTES = get_media_gols_pro_mandante(CSV_DATASET, TIMES, ano_inicio, ano_fim)
MEDIA_GOLS_CONTRA_VISITANTES = get_media_gols_contra_visitante(CSV_DATASET, TIMES, ano_inicio, ano_fim)
MEDIA_GOLS_CONTRA_MANDANTES = get_media_gols_contra_mandante(CSV_DATASET, TIMES, ano_inicio, ano_fim)
MEDIA_GOLS_PRO_VISITANTES = get_media_gols_pro_visitante(CSV_DATASET, TIMES, ano_inicio, ano_fim)

# Variáveis fuzzy
valor_equipe_mandante = ctrl.Antecedent(np.arange(0, 221, 1), 'valor_equipe_mandante')
valor_equipe_visitante = ctrl.Antecedent(np.arange(0, 221, 1), 'valor_equipe_visitante')
idade_media_mandante = ctrl.Antecedent(np.arange(20, 31, 0.1), 'idade_media_mandante')
idade_media_visitante = ctrl.Antecedent(np.arange(20, 31, 0.1), 'idade_media_visitante')
media_gols_pro_mandante = ctrl.Antecedent(np.arange(0, 2.2, 0.05), 'media_gols_pro_mandante')
media_gols_contra_visitante = ctrl.Antecedent(np.arange(0, 3.5, 0.05), 'media_gols_contra_visitante')
media_gols_contra_mandante = ctrl.Antecedent(np.arange(0, 2, 0.05), 'media_gols_contra_mandante')
media_gols_pro_visitante = ctrl.Antecedent(np.arange(0, 1.4, 0.05), 'media_gols_pro_visitante')

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


# Sistema de controle fuzzy mandandte
sistema_controle_mandante = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45])
previsao_gols_mandante = ctrl.ControlSystemSimulation(sistema_controle_mandante)

# Sistema de controle fuzzy visitante
sistema_controle_visitante = ctrl.ControlSystem([rule10, rule11, rule12, rule13, rule14, rule14, rule15, rule16, rule17, rule18, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54])
previsao_gols_visitante = ctrl.ControlSystemSimulation(sistema_controle_visitante)

resultados = {time: 0 for time in TIMES}

# Simulação das partidas
for time_mandante in TIMES:
    for time_visitante in TIMES:
        if time_mandante != time_visitante:
            # Simulando gols do time mandante
            previsao_gols_mandante.input['valor_equipe_mandante'] = VALORES_EQUIPES_2024[time_mandante]
            previsao_gols_mandante.input['valor_equipe_visitante'] = VALORES_EQUIPES_2024[time_visitante]
            previsao_gols_mandante.input['idade_media_mandante'] = IDADES_EQUIPES_2024[time_mandante]
            previsao_gols_mandante.input['idade_media_visitante'] = IDADES_EQUIPES_2024[time_visitante]

            previsao_gols_mandante.input['media_gols_pro_mandante'] = MEDIA_GOLS_PRO_MANDANTES[time_mandante]
            previsao_gols_mandante.input['media_gols_contra_visitante'] = MEDIA_GOLS_CONTRA_VISITANTES[time_visitante]

            previsao_gols_mandante.compute()
            
            # Simulando gols do time visitante
            previsao_gols_visitante.input['valor_equipe_mandante'] = VALORES_EQUIPES_2024[time_mandante]
            previsao_gols_visitante.input['valor_equipe_visitante'] = VALORES_EQUIPES_2024[time_visitante]
            previsao_gols_visitante.input['idade_media_mandante'] = IDADES_EQUIPES_2024[time_mandante]
            previsao_gols_visitante.input['idade_media_visitante'] = IDADES_EQUIPES_2024[time_visitante]

            previsao_gols_visitante.input['media_gols_contra_mandante'] = MEDIA_GOLS_CONTRA_MANDANTES[time_mandante]
            previsao_gols_visitante.input['media_gols_pro_visitante'] = MEDIA_GOLS_PRO_VISITANTES[time_visitante]

            previsao_gols_visitante.compute()
            
            # Resultado da simulação
            gols_mandante_simulados = round(previsao_gols_mandante.output['gols'], 2)
            gols_visitante_simulados = round(previsao_gols_visitante.output['gols'], 2)
            
            # Atualização dos pontos
            if gols_mandante_simulados > gols_visitante_simulados:
                resultados[time_mandante] += 3
            elif gols_mandante_simulados < gols_visitante_simulados:
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