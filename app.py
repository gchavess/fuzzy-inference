import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

sabor = ctrl.Antecedent(np.arange(0, 11, 1), 'sabor')
servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
tempo = ctrl.Antecedent(np.arange(0, 16, 1), 'tempo')

gorjeta = ctrl.Consequent(np.arange(0, 21, 1), 'gorjeta')

sabor['insossa'] = fuzz.trimf(sabor.universe, [0, 0, 5])
sabor['saborosa'] = fuzz.trimf(sabor.universe, [5, 10, 10])

servico['ruim'] = fuzz.trimf(servico.universe, [0, 0, 5])
servico['excelente'] = fuzz.trimf(servico.universe, [5, 10, 10])

tempo['demorado'] = fuzz.trimf(tempo.universe, [0, 0, 5])
tempo['mediano'] = fuzz.trimf(tempo.universe, [5, 10, 10])
tempo['rapido'] = fuzz.trimf(tempo.universe, [10, 15, 15])

gorjeta['pouca'] = fuzz.trimf(gorjeta.universe, [0, 0, 5])
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [5, 10, 15])
gorjeta['generosa'] = fuzz.trimf(gorjeta.universe, [15, 20, 20])

regra1 = ctrl.Rule(sabor['insossa'] & servico['ruim'], gorjeta['pouca'])
regra2 = ctrl.Rule(sabor['saborosa'] & servico['excelente'], gorjeta['generosa'])
regra3 = ctrl.Rule(tempo['demorado'], gorjeta['pouca'])
regra4 = ctrl.Rule(tempo['mediano'] | tempo['rapido'], gorjeta['media'])
regra5 = ctrl.Rule(tempo['demorado'] & (sabor['insossa'] | servico['ruim']), gorjeta['pouca']) 

gorjeta_ctrl = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])
gorjeta_sim = ctrl.ControlSystemSimulation(gorjeta_ctrl)

def calcular_gorjeta(nota_sabor, nota_servico, tempo_atendimento):
    gorjeta_sim.input['sabor'] = nota_sabor
    gorjeta_sim.input['servico'] = nota_servico
    gorjeta_sim.input['tempo'] = tempo_atendimento
    gorjeta_sim.compute()
    return gorjeta_sim.output['gorjeta']

gorjeta_calculada = calcular_gorjeta(8, 9, 0)
print(f'Gorjeta calculada: {gorjeta_calculada}%')
