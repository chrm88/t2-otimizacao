from random import randint
import numpy as np
import time

horario_inicio = time.time()
tempo_limite = 60 * 60
# entrada da PL
nvd = 10
funcaoobjetivo = [5, 4, 8, 3, 9, 2, 7, 6, 10, 1]
restricoes = [
    2, 1, 3, 1, 2, 1, 4, 2, 5, 1, 150,
    1, 2, 1, 2, 1, 3, 1, 4, 1, 2, 200,
    3, 1, 2, 3, 4, 1, 2, 1, 3, 3, 180,
    1, 3, 4, 1, 3, 2, 3, 2, 1, 4, 125,
    4, 2, 1, 4, 2, 3, 1, 3, 4, 1, 300,
    2, 4, 3, 1, 1, 4, 2, 1, 2, 2, 220,
    3, 1, 4, 2, 3, 1, 4, 3, 1, 3, 280,
    1, 2, 1, 3, 4, 2, 1, 4, 2, 4, 350,
    4, 3, 2, 1, 1, 3, 3, 1, 3, 1, 260,
    2, 1, 3, 4, 2, 1, 2, 2, 4, 2, 240
]
otimo = 80
solucao = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def viavel(sol):
    eviavel = 0
    for x in range(10):
        valorrest = 0
        for y in range(10):
            valorrest = valorrest + sol[y] * restricoes[x*11+y]
        if (valorrest > restricoes[x*11+10]):
            eviavel = 1
    return eviavel == 0

# código de cálculo da aptidão de uma solução.
def avaliacao(solucao):
    v = 0
    for x in range(10):
        v = v + (solucao.item(x) * funcaoobjetivo[x])
    return v

# avaliacao(solucao)
# viavel(solucao)

# Considere que o intervalo das variáveis de decisão seja de zero a dez.
# Parâmetros: 10 partículas, velocidade proporcional de 20% arredondada aleatoriamente para cima ou para baixo, busca local por escolha e troca de uma variável aleatoriamente. 
# Condições de parada: 1000 iterações ou 1 hora ou alcançar valor=78 ou 50 iterações sem melhorar. 
# Saídas: a cada 10 iterações mostrar a melhor solução encontrada completa.
vd_min = 0
vd_max = 10
n_particulas = 10
vel_prop = 0.2
max_iteracoes_geral = 1000
max_iteracoes_melhora = 50
valor_alvo = 78

def gerar_particula():
  nova_particula = [randint(vd_min, vd_max) for _ in range(nvd)]
  while not viavel(nova_particula):
    nova_particula = gerar_particula()
  
  return np.array(nova_particula)

def busca_local(ptc):
  troca_i = randint(0, nvd - 1)
  troca_val = randint(vd_min, vd_max)
  
  while troca_val == ptc[troca_i]:
    troca_val = randint(vd_min, vd_max)
    
  resultado = ptc.copy()
  resultado[troca_i] = troca_val
  
  if not viavel(resultado):
    return busca_local(ptc)
    
  return resultado

def calcular_deslocamento(ptc, melhor):  
  ptc_deslocada = ptc + np.rint(vel_prop * (melhor - ptc))
  ptc_deslocada = np.clip(ptc_deslocada, vd_min, vd_max).astype(int)
  return ptc_deslocada
  
particulas_iniciais = [gerar_particula() for _ in range(n_particulas)]
particulas_atuais = particulas_iniciais
index_melhor_particula = -1
melhor_particula_cpy = {}
melhor_fitness = 0
controle_ultima_melhora = -1

for it in range(max_iteracoes_geral):
  
  for i, ptc in enumerate(particulas_atuais):
    fitness_atual = avaliacao(ptc)
    if fitness_atual > melhor_fitness:
      melhor_fitness = fitness_atual
      index_melhor_particula = i
      melhor_particula_cpy = ptc.copy()
      controle_ultima_melhora = it
      
  ptc_deslocadas = [ptc.copy() for ptc in particulas_atuais]
  for i, ptc in enumerate(particulas_atuais):
    if i == index_melhor_particula:
      ptc_deslocadas[i] = busca_local(particulas_atuais[i])
      continue
    
    ptc_deslocadas[i] = calcular_deslocamento(ptc, particulas_atuais[index_melhor_particula])
  
  particulas_atuais = ptc_deslocadas.copy()
  
  if melhor_fitness == valor_alvo:
    print(f"Melhor fitness encontrado na iteração {it}")
    break
  
  if controle_ultima_melhora + max_iteracoes_melhora == it:
    print(f"Se passaram {max_iteracoes_melhora} iterações sem melhora, interrompendo...")
    break
  
  if time.time() > horario_inicio + tempo_limite:
    print("Tempo limite atingido...")
    break
    
  if it % 10 == 0:
    print(f"Iteração {it}: Melhor Solução {melhor_particula_cpy} com o melhor fitness: {melhor_fitness}")
    
print(f"Resultado final: Solução {melhor_particula_cpy} com fitness {melhor_fitness}")
