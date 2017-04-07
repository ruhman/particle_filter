import {cria_particulas, atualiza_probabilidades, movimenta_robo_e_particulas, Particula, Robo } from "./simple_particle"

let estado_simulacao = {};

function cria_tabela_mapa(mapa:string[], id:string):void {
    let tbl = (<HTMLTableElement>document.getElementById(id));
    tbl.innerHTML = '';

    for (var i = 0; i < mapa.length; i++) {
        let linha = tbl.insertRow();
        for (var j = 0; j < mapa[i].length; j++) {
            let cel = linha.insertCell();
            if (mapa[i][j] == '#') {
                cel.classList.add('parede');
            } else {
                cel.classList.add('chao');
            }
        }
    }
}

function atualiza_robo_e_particulas(mapa:string[], id_viz:string, id_probs:string, r:Robo, particulas:Particula[]):void {
    let tbl_viz = <HTMLTableElement>document.getElementById(id_viz).children[0];
    let tbl_probs = <HTMLTableElement>document.getElementById(id_probs).children[0];
    for (var i = 0; i < mapa.length; i++) {
        for (var j=0; j < mapa[i].length; j++){
            tbl_viz.children[i].children[j].classList.remove('robo');
            tbl_probs.children[i].children[j].style.background = '';
        }
    }

    tbl_viz.children[r.i].children[r.j].classList.add('robo');
    particulas.forEach(part => {
        let r = part.prob_H * 255;
        let b = (1 - part.prob_H) * 255
        tbl_probs.children[part.i].children[part.j].style.background = 'rgb(' + r + ', 0, ' + b + ')';
    });
}

function inicia_visualizacao(e) {
    let mapa:string[] = (<HTMLTextAreaElement>document.getElementById('mapa')).value.trim().split('\n');
    estado_simulacao['mapa'] = mapa;
    estado_simulacao['particulas'] = cria_particulas(mapa);
    let vals = (<HTMLInputElement>document.getElementById('robo')).value.split(',');
    estado_simulacao['robo'] = {i:parseInt(vals[0]),j:parseInt(vals[1])};

    cria_tabela_mapa(mapa, 'mapa_viz');
    cria_tabela_mapa(mapa, 'mapa_probs');

    $('ul.tabs').tabs('select_tab', 'viz');

    atualiza_robo_e_particulas(mapa, 'mapa_viz', 'mapa_probs', estado_simulacao['robo'], estado_simulacao['particulas']);
}

function movimenta_robo_click(e:Event):void {
    let mapa = estado_simulacao['mapa'];
    let robo = estado_simulacao['robo'];
    let particulas = estado_simulacao['particulas'];

    let delta = [0, 0];
    if (e.target.id == 'U') {
        delta = [-1, 0];
    } else if (e.target.id == 'D') {
        delta = [1, 0];
    } else if (e.target.id == 'W') {
        delta = [0, -1];
    } else if (e.target.id == 'E') {
        delta = [0, 1];
    }

    movimenta_robo_e_particulas(mapa, delta, robo, particulas);
    atualiza_probabilidades(mapa, robo, particulas);
    
    atualiza_robo_e_particulas(mapa, 'mapa_viz', 'mapa_probs', estado_simulacao['robo'], estado_simulacao['particulas']);
}


window.addEventListener('load', function (e) {
    // bind everything.    
    document.getElementById('iniciar').addEventListener('click', inicia_visualizacao);

    ['U', 'D', 'W', 'E'].forEach(p => {
        document.getElementById(p).addEventListener('click', movimenta_robo_click);
    });
});