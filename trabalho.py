from random import randint
import numpy as np
import time
import math

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
            valorrest = valorrest + (sol[y] * restricoes[x*11+y])
        if (valorrest > restricoes[x*11+10]):
            eviavel = 1
    return eviavel == 0

# código de cálculo da aptidão de uma solução.
def avaliacao(solucao):
    v = 0
    for x in range(10):
        v = v + (solucao.item(x) * funcaoobjetivo[x])
    return v

# Particle Swarm Optimization :: Grupo: Carlos, Matheus e Waldemar
# Considere que o intervalo das variáveis de decisão seja de zero a dez.
# Parâmetros: 10 partículas, velocidade proporcional de 20% arredondada aleatoriamente para cima ou para baixo, busca local por escolha e troca de uma variável aleatoriamente. 
# Condições de parada: 1000 iterações ou 1 hora ou alcançar valor=78 ou 50 iterações sem melhorar. 
# Saídas: a cada 10 iterações mostrar a melhor solução encontrada completa.

horario_inicio = time.time() # guarda o horário de início para o controle do limite de 1 hora
tempo_limite = 60 * 60 # em segundos, 60 minutos * 60 segundos

# intervalo mínimo-máximo para as variáveis de decisão
vd_min = 0
vd_max = 10

# parametros para o PSO pré-definidos no problema
n_particulas = 10
vel_prop = 0.20 # 20%
max_iteracoes_geral = 1000
max_iteracoes_melhora = 50
valor_alvo = 78

# gera uma nova particula com valores aleatorios dentro do intervalo limite para variaveis de decisão 
def gerar_particula():
  nova_particula = [randint(vd_min, vd_max) for _ in range(nvd)]
  
  # garante que a particula gerada seja viável
  while not viavel(nova_particula):
    nova_particula = gerar_particula()
  
  return np.array(nova_particula)


# executa a busca local em uma particula de acordo com as instruções 
def busca_local(ptc):
  # trocando o valor de uma variável de forma aleatória
  troca_i = randint(0, nvd - 1)
  troca_val = randint(vd_min, vd_max)
  
  # garantindo que o valor aleatorio nao seja igual ao atual
  while troca_val == ptc[troca_i]:
    troca_val = randint(vd_min, vd_max)
    
  resultado = ptc.copy()
  resultado[troca_i] = troca_val
  
  # garantindo que ainda seja viável
  if not viavel(resultado):
    return busca_local(ptc)
    
  return resultado


# calcula o deslocamento de uma partícula em direção ao melhor
def calcular_deslocamento(ptc, melhor):
  # utiliza a fórmula da velocidade proporcional A = A + vp * (vetor_B - vetor_A), executando a subtração e multiplicação primeiro
  subtr_vetores = vel_prop * (melhor - ptc)
  
  # arredonda o resultado da conta de forma aleatória
  nums_arredondados = [ (math.ceil(num) if (randint(0, 1) == 1) else math.floor(num)) for num in subtr_vetores ]
  
  # A + resultado arredondado
  ptc_deslocada = ptc + nums_arredondados
  
  # verifica se é viável, e caso não seja, gera uma nova particula aleatoriamente
  if viavel(ptc_deslocada):
    return ptc_deslocada
  else:
    return gerar_particula()


# gera um grupo inicial de N particulas
particulas_iniciais = [gerar_particula() for _ in range(n_particulas)]
particulas_atuais = particulas_iniciais

# variaveis para guargar o melhor resultado e fazer os controles de parada
index_melhor_particula = -1
melhor_particula = {}
melhor_fitness = 0
controle_ultima_melhora = -1

# inicia as iterações
for it in range(max_iteracoes_geral):
  
  # avalia o fitness de cada particula no grupo atual
  for i, ptc in enumerate(particulas_atuais):
    fitness_atual = avaliacao(ptc)

    # se o calculado for melhor, atualizamos os valores das variáveis
    if fitness_atual > melhor_fitness:
      melhor_fitness = fitness_atual
      melhor_particula = ptc.copy()
      index_melhor_particula = i
      controle_ultima_melhora = it
      
  # prepara uma cópia das partículas atuais para realizar o deslocamento
  ptc_deslocadas = [ptc.copy() for ptc in particulas_atuais]
  
  # calcula os deslocalmentos para cada partícula
  for i, ptc in enumerate(particulas_atuais):
    # se o ponto atual for o melhor, executamos uma busca local envés do deslocamento
    if i == index_melhor_particula:
      ptc_deslocadas[i] = busca_local(particulas_atuais[i])
      continue
    
    # para as demais partículas, se calcula o deslocamento em direção ao ponto melhor
    ptc_deslocadas[i] = calcular_deslocamento(ptc, melhor_particula)
  
  # verifica a condição de parada que é o valor do melhor fitness ter chegado no ideal
  # if melhor_fitness == valor_alvo:
  #   print(f"Fitness ideal encontrado na iteração {it}")
  #   break

  # verifica o limite máximo de iterações desde a ultima melhora
  # se a última melhora somada ao limite for igual a iteração atual, interrompe as iterações 
  if controle_ultima_melhora + max_iteracoes_melhora == it:
    print(f"Se passaram {max_iteracoes_melhora} iterações sem melhora, interrompendo...")
    break
  
  # verifica o limite de tempo de 1 hora
  # se o tempo atual for maior ou igual ao início, interrompe as iterações
  if time.time() >= horario_inicio + tempo_limite:
    print("Tempo limite atingido...")
    break
    
  # a cada 10 iterações exibe os resultados parciais
  # se o número da iteração atual for divisível por 10 (resto 0), exibe a mensagem
  if it % 10 == 0:
    print(f"Iteração {it}: Melhor Solução {melhor_particula} com o melhor fitness: {melhor_fitness}")
    
  # prepara para a próxima iteração, copiando as partículas deslocadas para o vetor das atuais
  particulas_atuais = ptc_deslocadas.copy()


# Fim da execução
print(f"Resultado final: Solução {melhor_particula} com fitness {melhor_fitness}")
