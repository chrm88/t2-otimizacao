from pyswarms.single.global_best import GlobalBestPSO

# código de inicialização da PL
#variável que guarda o número de variáveis de decisão
nvd=10 

#guarda os coeficientes da função objetivo
funcaoobjetivo=[5, 4, 8, 3, 9, 2, 7, 6, 10, 1]  

#guarda os coeficientes das restrições
restrições=[2, 1, 3, 1, 2, 1, 4, 2, 5, 1, 15,
            1, 2, 1, 2, 1, 3, 1, 4, 1, 2, 20,
            3, 1, 2, 3, 4, 1, 2, 1, 3, 3, 18,
            1, 3, 4, 1, 3, 2, 3, 2, 1, 4, 25,
            4, 2, 1, 4, 2, 3, 1, 3, 4, 1, 30,
            2, 4, 3, 1, 1, 4, 2, 1, 2, 2, 22,
            3, 1, 4, 2, 3, 1, 4, 3, 1, 3, 28,
            1, 2, 1, 3, 4, 2, 1, 4, 2, 4, 35,
            4, 3, 2, 1, 1, 3, 3, 1, 3, 1, 26,
            2, 1, 3, 4, 2, 1, 2, 2, 4, 2, 24]

#guarda o provável valor ótimo
otimo=80

#guarda o vetor de solução gerado
solucao=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#os códigos abaixo ainda não foram verificados
#código de verificação se uma solução proposta é viável
def verificar_solucao():
  inv=0
  for i in range(9):
    v=0
    for j in range(1,10):
      v=v+solucao[j]*restrições[i*11+j]
      if v > restrições[i*11+11]:
        inv=1
    if inv == 0:
      return v
    #aceitar

#código de cálculo da aptidão de uma solução.
def verificar_aptidao():
  for i in range(9):
    v=v+solucao[i]*funcaoobjetivo[i]
    print(v)

def objetivo(*args):
  obj = 0
  for i in range(len(args)):
    obj = obj + (funcaoobjetivo[i] * args[i])
  
  return obj

optimizer = GlobalBestPSO(
    n_particles = 50,
    dimensions = 2,
    bounds= (0, nvd),
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9},
)

cost, pos = optimizer.optimize(objetivo, iters=10)
print(cost, "abcd", pos)
# velocidade proporcional de 20%, 1.2
# 1000 iteracoes

# busca local
# fazer o encadeamento em direcao ao melhor
