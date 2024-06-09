import csv
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

TIMES = [
    'Atlético-GO', 'Atlético-MG', 'Athletico-PR', 'Bahia', 'Botafogo', 
    'RB Bragantino', 'Corinthians', 'Criciúma', 'Cruzeiro', 'Cuiabá', 
    'Flamengo', 'Fluminense', 'Fortaleza', 'Grêmio', 'Internacional', 
    'Juventude', 'Palmeiras', 'São Paulo', 'Vasco da Gama', 'EC Vitória'
]

CSV_DATASET = 'data/brasileirao_serie_a.csv'
CSV_CONFRONTOS = 'data/confrontos.csv'

def get_confrontos():
    confrontos = []

    with open(CSV_CONFRONTOS) as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=',')

        # Pular o cabeçalho
        next(leitor_csv)

        for linha in leitor_csv:
            confrontos.append((linha[0], linha[1], linha[2]))

    return confrontos

def get_caracteristicas_relevantes():
    caracteristicas_relevantes = [
        'time_mandante',
        'time_visitante',
        'valor_equipe_titular_mandante',
        'valor_equipe_titular_visitante',
        'idade_media_titular_mandante',
        'idade_media_titular_visitante',
        'gols_mandante', 
        'gols_visitante'
    ]

    return caracteristicas_relevantes

def get_variaveis_fuzzy():
    variavies_fuzzy = {
        'valor_mandante': ctrl.Antecedent(np.arange(0, 50e6, 1e6), 'valor_mandante'),
        'valor_visitante': ctrl.Antecedent(np.arange(0, 50e6, 1e6), 'valor_visitante'),
        'idade_mandante': ctrl.Antecedent(np.arange(20, 41, 1), 'idade_mandante'),
        'idade_visitante': ctrl.Antecedent(np.arange(20, 41, 1), 'idade_visitante'),
        'gols': ctrl.Consequent(np.arange(0, 7, 1), 'gols')
    }

    return variavies_fuzzy

def get_funcao_pertinencia_valor_mandante(valor_mandante):
    valor_mandante['baixo'] = fuzz.trimf(valor_mandante.universe, [0, 0, 15e6])
    valor_mandante['medio'] = fuzz.trimf(valor_mandante.universe, [10e6, 15e6, 20e6])
    valor_mandante['alto'] = fuzz.trimf(valor_mandante.universe, [15e6, 50e6, 50e6])

    return valor_mandante

def get_funcao_pertinencia_valor_visitante(valor_visitante):
    valor_visitante['baixo'] = fuzz.trimf(valor_visitante.universe, [0, 0, 15e6])
    valor_visitante['medio'] = fuzz.trimf(valor_visitante.universe, [10e6, 15e6, 20e6])
    valor_visitante['alto'] = fuzz.trimf(valor_visitante.universe, [15e6, 50e6, 50e6])

    return valor_visitante

def get_funcao_pertinencia_idade_mandante(idade_mandante):
    idade_mandante['jovem'] = fuzz.trimf(idade_mandante.universe, [20, 20, 30])
    idade_mandante['experiente'] = fuzz.trimf(idade_mandante.universe, [25, 30, 35])
    idade_mandante['veterano'] = fuzz.trimf(idade_mandante.universe, [30, 40, 40])

    return idade_mandante

def get_funcao_pertinencia_idade_visitante(idade_visitante):
    idade_visitante['jovem'] = fuzz.trimf(idade_visitante.universe, [20, 20, 30])
    idade_visitante['experiente'] = fuzz.trimf(idade_visitante.universe, [25, 30, 35])
    idade_visitante['veterano'] = fuzz.trimf(idade_visitante.universe, [30, 40, 40])

    return idade_visitante

def get_funcao_pertinencia_gols(gols):
    gols['baixo'] = fuzz.trimf(gols.universe, [0, 0, 2])
    gols['medio'] = fuzz.trimf(gols.universe, [0, 2, 4])
    gols['alto'] = fuzz.trimf(gols.universe, [2, 4, 6])

    return gols

def get_regras_fuzzy(funcoes_pertinencia):
    valor_mandante = funcoes_pertinencia['valor_mandante']
    valor_visitante = funcoes_pertinencia['valor_visitante']
    idade_mandante = funcoes_pertinencia['idade_mandante']
    idade_visitante = funcoes_pertinencia['idade_visitante']
    gols = funcoes_pertinencia['gols']

    regras_fuzzy = {
        'regra1': ctrl.Rule(valor_mandante['alto'] & valor_visitante['baixo'], gols['alto']),
        'regra2': ctrl.Rule(valor_mandante['baixo'] & valor_visitante['alto'], gols['baixo']),
        'regra3': ctrl.Rule(valor_mandante['medio'] & valor_visitante['medio'], gols['medio']),
        'regra4': ctrl.Rule(idade_mandante['jovem'] & idade_visitante['veterano'], gols['medio']),
        'regra5': ctrl.Rule(idade_mandante['veterano'] & idade_visitante['jovem'], gols['medio']),
        'regra6': ctrl.Rule(valor_mandante['alto'] & valor_visitante['alto'], gols['medio']),
        'regra7': ctrl.Rule(valor_mandante['baixo'] & valor_visitante['baixo'], gols['baixo']),
        'regra8': ctrl.Rule(valor_mandante['alto'] & idade_visitante['jovem'], gols['alto']),
        'regra9': ctrl.Rule(valor_mandante['baixo'] & idade_mandante['veterano'], gols['baixo']),
        'regra10': ctrl.Rule(idade_mandante['experiente'] & idade_visitante['experiente'], gols['medio']),
        # Regras adicionais para evitar área zero
        'regra11': ctrl.Rule(valor_mandante['alto'] | valor_visitante['alto'], gols['medio']),
        'regra12': ctrl.Rule(idade_mandante['jovem'] | idade_visitante['jovem'], gols['medio']),
        'regra13': ctrl.Rule(idade_mandante['veterano'] | idade_visitante['veterano'], gols['medio'])
    }

    return regras_fuzzy

def get_sistema_de_controle(regras_fuzzy):    
    gols_ctrl = ctrl.ControlSystem([
        regras_fuzzy['regra1'], regras_fuzzy['regra2'], 
        regras_fuzzy['regra3'], regras_fuzzy['regra4'], 
        regras_fuzzy['regra5'], regras_fuzzy['regra6'], 
        regras_fuzzy['regra7'], regras_fuzzy['regra8'], 
        regras_fuzzy['regra9'], regras_fuzzy['regra10'],
        regras_fuzzy['regra11'], regras_fuzzy['regra12'], 
        regras_fuzzy['regra13']
    ])

    gols_sim = ctrl.ControlSystemSimulation(gols_ctrl)

    return gols_sim

def prever_gols(gols_sim, valores):
    gols_sim.input['valor_mandante'] = valores['valor_mandante']
    gols_sim.input['valor_visitante'] = valores['valor_visitante']
    gols_sim.input['idade_mandante'] = valores['idade_mandante']
    gols_sim.input['idade_visitante'] = valores['idade_visitante']

    gols_sim.compute()

    return gols_sim.output['gols']

def prever_campeonato_brasileiro():
    # Leitura e preparação dos dados
    confrontos = get_confrontos()

    caracteristicas_relevantes = get_caracteristicas_relevantes()

    df = pd.read_csv(CSV_DATASET)
    df = df[caracteristicas_relevantes]

    # Verifica se as colunas 'time_mandante' e 'time_visitante' estão presentes
    # if 'time_mandante' not in df.columns or 'time_visitante' not in df.columns:
    #     raise KeyError("'time_mandante' ou 'time_visitante' não estão presentes no dataset.")

    variavies_fuzzy = get_variaveis_fuzzy()

    valor_mandante = get_funcao_pertinencia_valor_mandante(variavies_fuzzy['valor_mandante'])
    valor_visitante = get_funcao_pertinencia_valor_visitante(variavies_fuzzy['valor_visitante'])
    idade_mandante = get_funcao_pertinencia_idade_mandante(variavies_fuzzy['idade_mandante'])
    idade_visitante = get_funcao_pertinencia_idade_visitante(variavies_fuzzy['idade_visitante'])
    gols = get_funcao_pertinencia_gols(variavies_fuzzy['gols'])

    funcoes_pertinencia = {
        'valor_mandante': valor_mandante, 
        'valor_visitante': valor_visitante, 
        'idade_mandante': idade_mandante, 
        'idade_visitante': idade_visitante, 
        'gols': gols
    }

    regras_fuzzy = get_regras_fuzzy(funcoes_pertinencia)
    sistema_de_controle = get_sistema_de_controle(regras_fuzzy)

    # Previsão dos gols para todas as partidas no dataset
    gols_previstos = []

    for index, row in df.iterrows():
        caracteristicas_relevantes_df = {
            'valor_mandante': row['valor_equipe_titular_mandante'], 
            'valor_visitante': row['valor_equipe_titular_visitante'], 
            'idade_mandante': row['idade_media_titular_mandante'], 
            'idade_visitante': row['idade_media_titular_visitante']
        }

        try:
            gols = prever_gols(sistema_de_controle, caracteristicas_relevantes_df)
        except ValueError as e:
            print(f"Erro na partida índice {index}: {e}")

            # Atribui 0 gols caso ocorra um erro
            gols = 0

        gols_previstos.append(gols)

    df['gols_previstos'] = gols_previstos

    # Simulação do campeonato atual
    resultados = {time: 0 for time in TIMES}

    rodada_anterior = 0

    for rodada, time_mandante, time_visitante in confrontos:
        # Verifica se time_mandante e time_visitante estão presentes no DataFrame
        df_mandante = df[df['time_mandante'] == time_mandante]
        df_visitante = df[df['time_visitante'] == time_visitante]

        if df_mandante.empty:
            # print(f"Dados insuficientes para {time_mandante}. Pulando este confronto.")

            continue

        if df_visitante.empty:
            # print(f"Dados insuficientes para {time_visitante}. Pulando este confronto.")

            continue

        valores_time_mandante = df_mandante.iloc[0]
        valores_time_visitante = df_visitante.iloc[0]

        valores_mandante = {
            'valor_mandante': valores_time_mandante['valor_equipe_titular_mandante'], 
            'valor_visitante': valores_time_visitante['valor_equipe_titular_visitante'], 
            'idade_mandante': valores_time_mandante['idade_media_titular_mandante'], 
            'idade_visitante': valores_time_visitante['idade_media_titular_visitante']
        }

        valores_visitante = {
            'valor_mandante': valores_time_visitante['valor_equipe_titular_visitante'], 
            'valor_visitante': valores_time_mandante['valor_equipe_titular_mandante'], 
            'idade_mandante': valores_time_visitante['idade_media_titular_visitante'], 
            'idade_visitante': valores_time_mandante['idade_media_titular_mandante']
        }

        # Previsao dos gols para a partida
        try:
            gols_mandante = prever_gols(sistema_de_controle, valores_mandante)

            if np.isnan(gols_mandante):
                gols_mandante = 0
            else:
                gols_mandante = int(round(gols_mandante))
        except ValueError as e:
            # Atribui 0 gols caso ocorra um erro
            gols_mandante = 0

        try:
            gols_visitante = prever_gols(sistema_de_controle, valores_visitante)
            if np.isnan(gols_visitante):
                gols_visitante = 0
            else:
                gols_visitante = int(round(gols_visitante))
        except ValueError as e:
            # Atribui 0 gols caso ocorra um erro
            gols_visitante = 0

        # Atualização dos pontos
        if gols_mandante > gols_visitante:
            resultados[time_mandante] += 3
        elif gols_mandante < gols_visitante:
            resultados[time_visitante] += 3
        else:
            resultados[time_mandante] += 1
            resultados[time_visitante] += 1

        if rodada != rodada_anterior:
            print('\n')
            print(50 * '-')
            print(f'Rodada {rodada}:')
            print(50 * '-')

            rodada_anterior = rodada

        print(f'{time_mandante} - {gols_mandante} x {gols_visitante} - {time_visitante}')

    campeao = max(resultados, key=resultados.get)

    print(50 * '-')
    print(f'\nO campeão previsto é: {campeao}')

if __name__ == '__main__':
    prever_campeonato_brasileiro()
