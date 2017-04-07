# coding: utf8
#import browser

def cria_particulas(mapa):
    '''
    Cria uma partícula para cada posição vazia no grid. 
    '''
    particulas = []
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] != '#':
                part = {'posicao': (i, j), 'prob_H': 0}
                particulas.append(part)

    n = len(particulas)
    for part in particulas:
        part['prob_H'] = 1 / n

    return particulas

def posicao_mais_provavel(particulas):
    '''
    Devolve uma lista com as posições das hipóteses de maior probabilidade.
    '''
    ordenado = list(reversed(sorted(particulas, key=lambda t: t['prob_H'])))
    return [part['posicao'] for part in particulas if part['prob_H'] == ordenado[0]['prob_H']]

def mostra_mapa(mapa, robo, particulas):
    '''
    Mostra mapa no console, incluindo posicao do robo e das particulas mais provaveis.
    '''
    str_mapa = ''
    mais_provavel = posicao_mais_provavel(particulas)
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if (i,j) == robo:
                str_mapa += 'o' if not robo in mais_provavel else '='
            elif (i, j) in mais_provavel:
                str_mapa += '+'
            else:
                str_mapa += mapa[i][j]
        str_mapa += '\n'
    print(str_mapa)

def mostra_particulas(particulas):
    for part in particulas:
        print(part)

def leitura_sensores(mapa, pos):
    '''
    Devolve a leitura dos sensores na posição (pos_i, pos_j) do mapa.
    A leitura é uma tupla de quatro elementos indicando se cada uma das 
    casas adjacentes está vazia ou não. 
    '''
    pos_i, pos_j = pos

    u = mapa[pos_i-1][pos_j] != '#' if pos_i >= 1 else False
    d = mapa[pos_i+1][pos_j] != '#' if pos_i < len(mapa)-1 else False
    w = mapa[pos_i][pos_j-1] != '#' if pos_j >= 1 else False
    e = mapa[pos_i][pos_j+1] != '#' if pos_j < len(mapa[pos_i])-1 else False
    return (u, d, w, e)

def probabilidade_Dados_Hipotese(leitura_real, leitura_part):
    '''
    Calcula a probabilidade P(D|H), que representa a probabilidade dos
    dados terem sido capturados na posiç!ao de cada uma das particulas.
    Definimos isto como sendo a proporção de casas que tiveram leitura
    igual (vazia ou não vazia) na posição do robo e na da partícula
    '''
    return sum([leitura_real[i] == leitura_part[i] for i in range(4)])/4

def movimenta_particulas_e_robo(mapa, particulas, robo, delta):
    '''
    Movimenta o robô e as partículas. Se uma particula bate na 
    parede ela não é mais plausível (prob_H=0) e podemos removê-la.
    '''
    if mapa[robo[0]+delta[0]][robo[1]+delta[1]] == '#':
        print('movimento inválido')
        return particulas, robo
    else:
        particulas_vivas = []
        for part in particulas:
            pos = part['posicao']
            if mapa[pos[0]+delta[0]][pos[1]+delta[1]] != '#':
                part['posicao'] = (pos[0]+delta[0], pos[1]+delta[1])
                particulas_vivas.append(part)
            else:
                pass # particula bateu na parede e morreu.

        return particulas_vivas, (robo[0]+delta[0], robo[1]+delta[1])

def atualiza_prob_H(mapa, particulas, robo):
    '''
    Calcula P(D|H) P(H) e atualiza a probabilidade de cada hipótese/partícula.
    '''
    novo_prob_H = []
    for part in particulas:
        prob_Dados_Hipotese = probabilidade_Dados_Hipotese(
            leitura_sensores(mapa, robo),
            leitura_sensores(mapa, part['posicao'])
        )
        novo_prob_H.append(prob_Dados_Hipotese * part['prob_H'])
    
    alpha = sum(novo_prob_H)

    for i, part in enumerate(particulas):
        part['prob_H'] = novo_prob_H[i]/alpha

    return particulas

def loop_principal_console():
    mapa = \
    '''
###########
#  #      #
#      #  #
###########
    '''
    # transforma mapa em uma matriz. 
    mapa = mapa.split('\n')[1:-1]
    posicao_real = (2, 2)
    particulas = cria_particulas(mapa)

    while True:
        mostra_mapa(mapa, posicao_real, particulas)
        print('robo', posicao_real)
        mostra_particulas(particulas)
        print('-----------------------')
        movimento = input('Movimento do robo: ')
        if movimento == 'U':
            delta = (-1, 0)
        elif movimento == 'D':
            delta = (+1, 0)
        elif movimento == 'W':
            delta = (0, -1)
        elif movimento == 'E':
            delta = (0, +1)
        else:
            delta = (0, 0)

        particulas, posicao_real = movimenta_particulas_e_robo(mapa, particulas, posicao_real, delta)
        particulas = atualiza_prob_H(mapa, particulas, posicao_real)


if __name__ == '__main__':
    loop_principal_console()