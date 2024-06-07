import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# CSV_DATASET = 'data/brasileirao_serie_a.csv'

# df = pd.read_csv(CSV_DATASET)

TIMES = [
    'Atlético-GO', 'Atlético-MG', 'Athletico-PR', 'Bahia', 'Botafogo', 
    'RB Bragantino', 'Corinthians', 'Criciúma', 'Cruzeiro', 'Cuiabá', 
    'Flamengo', 'Fluminense', 'Fortaleza', 'Grêmio', 'Internacional', 
    'Juventude', 'Palmeiras', 'São Paulo', 'Vasco da Gama', 'EC Vitória'
]
VALORES_EQUIPES_2024 = {
    'Flamengo': 166, 'Bahia': 61, 'Botafogo': 70, 'São Paulo': 90, 'Athletico-PR': 67,
    'RB Bragantino': 75, 'Palmeiras': 220, 'Internacional': 96, 'Cruzeiro': 67, 'Atlético-MG': 86,
    'Fortaleza': 42, 'Grêmio': 76, 'Vasco da Gama': 69, 'Juventude': 17, 'Fluminense': 110,
    'Criciúma': 16, 'Corinthians': 109, 'Atlético-GO': 22, 'EC Vitória': 26, 'Cuiabá': 27
}
IDADES_EQUIPES_2024 = {
    'Flamengo': 26, 'Bahia': 28.3, 'Botafogo': 26.9, 'São Paulo': 26.4, 'Athletico-PR': 25.2,
    'RB Bragantino': 24.1, 'Palmeiras': 25.4, 'Internacional': 27.9, 'Cruzeiro': 25.8, 'Atlético-MG': 26,
    'Fortaleza': 28.5, 'Grêmio': 27.3, 'Vasco da Gama': 26.8, 'Juventude': 26.9, 'Fluminense': 28,
    'Criciúma': 28, 'Corinthians': 24.8, 'Atlético-GO': 26.2, 'EC Vitória': 28.3, 'Cuiabá': 25.9
}

# def get_variaveis_fuzzy():
#     variavies_fuzzy = {
#         'valor_equipe_mandante': ctrl.Antecedent(np.arange(0, 250, 1), 'valor_equipe_mandante'),
#         'valor_equipe_visitante': ctrl.Antecedent(np.arange(0, 250, 1), 'valor_equipe_visitante'),
#         'idade_media_mandante': ctrl.Antecedent(np.arange(20, 40, 0.1), 'idade_media_mandante'),
#         'idade_media_visitante': ctrl.Antecedent(np.arange(20, 40, 0.1), 'idade_media_visitante'),
#         'gols': ctrl.Consequent(np.arange(0, 8, 1), 'gols')
#     }

#     return variavies_fuzzy

# def get_funcao_pertinencia_valor_equipe_mandante(valor_equipe_mandante):
#     valor_equipe_mandante['baixo'] = fuzz.trimf(valor_equipe_mandante.universe, [0, 0, 100])
#     valor_equipe_mandante['medio'] = fuzz.trimf(valor_equipe_mandante.universe, [50, 100, 150])
#     valor_equipe_mandante['alto'] = fuzz.trimf(valor_equipe_mandante.universe, [100, 250, 250])

#     return valor_equipe_mandante

# def get_funcao_pertinencia_valor_equipe_visitante(valor_equipe_visitante):
#     valor_equipe_visitante['baixo'] = fuzz.trimf(valor_equipe_visitante.universe, [0, 0, 100])
#     valor_equipe_visitante['medio'] = fuzz.trimf(valor_equipe_visitante.universe, [50, 100, 150])
#     valor_equipe_visitante['alto'] = fuzz.trimf(valor_equipe_visitante.universe, [100, 250, 250])

#     return valor_equipe_visitante

# def get_funcao_pertinencia_idade_media_mandante(idade_media_mandante):
#     idade_media_mandante['jovem'] = fuzz.trimf(idade_media_mandante.universe, [20, 20, 25])
#     idade_media_mandante['media'] = fuzz.trimf(idade_media_mandante.universe, [24, 27, 30])
#     idade_media_mandante['experiente'] = fuzz.trimf(idade_media_mandante.universe, [28, 40, 40])

#     return idade_media_mandante

# def get_funcao_pertinencia_idade_media_visitante(idade_media_visitante):
#     idade_media_visitante['jovem'] = fuzz.trimf(idade_media_visitante.universe, [20, 20, 25])
#     idade_media_visitante['media'] = fuzz.trimf(idade_media_visitante.universe, [24, 27, 30])
#     idade_media_visitante['experiente'] = fuzz.trimf(idade_media_visitante.universe, [28, 40, 40])

#     return idade_media_visitante

# def get_funcao_pertinencia_gols(gols):
#     gols['poucos'] = fuzz.trimf(gols.universe, [0, 0, 2])
#     gols['moderados'] = fuzz.trimf(gols.universe, [0, 2, 4])
#     gols['muitos'] = fuzz.trimf(gols.universe, [3, 4, 7])

#     return gols


# Variáveis fuzzy
valor_equipe_mandante = ctrl.Antecedent(np.arange(0, 250, 1), 'valor_equipe_mandante')
valor_equipe_visitante = ctrl.Antecedent(np.arange(0, 250, 1), 'valor_equipe_visitante')
idade_media_mandante = ctrl.Antecedent(np.arange(20, 40, 0.1), 'idade_media_mandante')
idade_media_visitante = ctrl.Antecedent(np.arange(20, 40, 0.1), 'idade_media_visitante')
gols = ctrl.Consequent(np.arange(0, 8, 1), 'gols')

# Funções de pertinência para valor da equipe mandante
valor_equipe_mandante['baixo'] = fuzz.trimf(valor_equipe_mandante.universe, [0, 0, 100])
valor_equipe_mandante['medio'] = fuzz.trimf(valor_equipe_mandante.universe, [50, 100, 150])
valor_equipe_mandante['alto'] = fuzz.trimf(valor_equipe_mandante.universe, [100, 250, 250])

# Funções de pertinência para valor da equipe visitante
valor_equipe_visitante['baixo'] = fuzz.trimf(valor_equipe_visitante.universe, [0, 0, 100])
valor_equipe_visitante['medio'] = fuzz.trimf(valor_equipe_visitante.universe, [50, 100, 150])
valor_equipe_visitante['alto'] = fuzz.trimf(valor_equipe_visitante.universe, [100, 250, 250])

# Funções de pertinência para idade média mandante
idade_media_mandante['jovem'] = fuzz.trimf(idade_media_mandante.universe, [20, 20, 25])
idade_media_mandante['media'] = fuzz.trimf(idade_media_mandante.universe, [24, 27, 30])
idade_media_mandante['experiente'] = fuzz.trimf(idade_media_mandante.universe, [28, 40, 40])

# Funções de pertinência para idade média visitante
idade_media_visitante['jovem'] = fuzz.trimf(idade_media_visitante.universe, [20, 20, 25])
idade_media_visitante['media'] = fuzz.trimf(idade_media_visitante.universe, [24, 27, 30])
idade_media_visitante['experiente'] = fuzz.trimf(idade_media_visitante.universe, [28, 40, 40])

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

# Sistema de controle fuzzy mandandte
sistema_controle_mandante = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
previsao_gols_mandante = ctrl.ControlSystemSimulation(sistema_controle_mandante)

# Sistema de controle fuzzy visitante
sistema_controle_visitante = ctrl.ControlSystem([rule10, rule11, rule12, rule13, rule14, rule14, rule15, rule16, rule17, rule18, rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36])
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
            previsao_gols_mandante.compute()
            
            # Simulando gols do time visitante
            previsao_gols_visitante.input['valor_equipe_mandante'] = VALORES_EQUIPES_2024[time_mandante]
            previsao_gols_visitante.input['valor_equipe_visitante'] = VALORES_EQUIPES_2024[time_visitante]
            previsao_gols_visitante.input['idade_media_mandante'] = IDADES_EQUIPES_2024[time_mandante]
            previsao_gols_visitante.input['idade_media_visitante'] = IDADES_EQUIPES_2024[time_visitante]
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

print("O campeão do Campeonato Brasileiro 2024 é:", campeao)
print("Pontuação final:", resultados[campeao])
