import browser
from browser import html, window
import simple_particle

simulacao_atual = {}

def adiciona_classe(el, cls):
    classes = set(el.class_name.split(' '))
    classes.add(cls)
    el.class_name = ' '.join(classes)

def remove_classe(el, cls):
    classes = set(el.class_name.split(' '))
    try:
        classes.remove(cls)
    except KeyError:
        pass
    el.class_name = ' '.join(classes)

def cria_tabela(mapa, id):
    tbl = browser.document[id]
    tbl.innerHTML = ''

    for i in range(len(mapa)):
        linha = html.TR()
        for j in range(len(mapa[i])):
            celula = html.TD()
            celula.class_name = 'parede' if mapa[i][j] == '#' else 'chao'
            linha <= celula
        tbl <= linha

def atualiza_tabela(mapa, robo, delta, particulas):
    tbl = browser.document['mapa_viz']
    remove_classe(tbl.children[robo[0]-delta[0]].children[robo[1]-delta[1]], 'robo')
    adiciona_classe(tbl.children[robo[0]].children[robo[1]], 'robo')

def atualiza_tabela_prob(mapa, particulas):
    tbl = browser.document['mapa_probs']
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            tbl.children[i].children[j].style.background = ''
    
    for part in particulas:
        i, j = part['posicao']
        blue = int((1-part['prob_H']) * 16) * 16
        red = int(part['prob_H'] * 16) * 16
        print(blue, red)
        tbl.children[i].children[j].style.background = 'rgb(%f, 0, %f)'%(red,blue)

def inicia_visualizacao(ev):
    mapa = browser.document['mapa'].value
    robo = tuple([int(i) for i in browser.document['robo'].value.split(',')])
    mapa = mapa.split('\n')
    particulas = simple_particle.cria_particulas(mapa)
    simple_particle.mostra_mapa(mapa, robo, particulas)

    window.jQuery('ul.tabs').tabs('select_tab', 'viz')

    cria_tabela(mapa, 'mapa_viz')
    cria_tabela(mapa, 'mapa_probs')
    atualiza_tabela(mapa, robo, (0, 0), particulas)
    atualiza_tabela_prob(mapa, particulas)

    simulacao_atual['mapa'] = mapa
    simulacao_atual['robo'] = robo
    simulacao_atual['particulas'] = particulas

def movimenta_robo(ev):
    mapa = simulacao_atual['mapa']
    robo = simulacao_atual['robo']
    particulas = simulacao_atual['particulas']

    movimento = ev.target.id
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

    particulas, robo = simple_particle.movimenta_particulas_e_robo(mapa, particulas, robo, delta)
    particulas = simple_particle.atualiza_prob_H(mapa, particulas, robo)

    simulacao_atual['mapa'] = mapa
    simulacao_atual['robo'] = robo
    simulacao_atual['particulas'] = particulas

    atualiza_tabela(mapa, robo, delta, particulas)
    atualiza_tabela_prob(mapa, particulas)

if __name__ == '__main__':
    browser.document['iniciar'].bind('click', inicia_visualizacao)
    for id in ['U', 'D', 'W', 'E']:
        browser.document[id].bind('click', movimenta_robo)
    