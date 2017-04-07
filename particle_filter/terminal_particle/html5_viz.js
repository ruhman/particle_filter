define(["require", "exports", "./simple_particle"], function (require, exports, simple_particle_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    var estado_simulacao = {};
    function cria_tabela_mapa(mapa, id) {
        var tbl = document.getElementById(id);
        tbl.innerHTML = '';
        for (var i = 0; i < mapa.length; i++) {
            var linha = tbl.insertRow();
            for (var j = 0; j < mapa[i].length; j++) {
                var cel = linha.insertCell();
                if (mapa[i][j] == '#') {
                    cel.classList.add('parede');
                }
                else {
                    cel.classList.add('chao');
                }
            }
        }
    }
    function atualiza_robo_e_particulas(mapa, id_viz, id_probs, r, particulas) {
        var tbl_viz = document.getElementById(id_viz).children[0];
        var tbl_probs = document.getElementById(id_probs).children[0];
        for (var i = 0; i < mapa.length; i++) {
            for (var j = 0; j < mapa[i].length; j++) {
                tbl_viz.children[i].children[j].classList.remove('robo');
                tbl_probs.children[i].children[j].style.background = '';
            }
        }
        tbl_viz.children[r.i].children[r.j].classList.add('robo');
        particulas.forEach(function (part) {
            var r = part.prob_H * 255;
            var b = (1 - part.prob_H) * 255;
            tbl_probs.children[part.i].children[part.j].style.background = 'rgb(' + r + ', 0, ' + b + ')';
        });
    }
    function inicia_visualizacao(e) {
        var mapa = document.getElementById('mapa').value.trim().split('\n');
        estado_simulacao['mapa'] = mapa;
        estado_simulacao['particulas'] = simple_particle_1.cria_particulas(mapa);
        var vals = document.getElementById('robo').value.split(',');
        estado_simulacao['robo'] = { i: parseInt(vals[0]), j: parseInt(vals[1]) };
        cria_tabela_mapa(mapa, 'mapa_viz');
        cria_tabela_mapa(mapa, 'mapa_probs');
        $('ul.tabs').tabs('select_tab', 'viz');
        atualiza_robo_e_particulas(mapa, 'mapa_viz', 'mapa_probs', estado_simulacao['robo'], estado_simulacao['particulas']);
    }
    function movimenta_robo_click(e) {
        var mapa = estado_simulacao['mapa'];
        var robo = estado_simulacao['robo'];
        var particulas = estado_simulacao['particulas'];
        var delta = [0, 0];
        if (e.target.id == 'U') {
            delta = [-1, 0];
        }
        else if (e.target.id == 'D') {
            delta = [1, 0];
        }
        else if (e.target.id == 'W') {
            delta = [0, -1];
        }
        else if (e.target.id == 'E') {
            delta = [0, 1];
        }
        simple_particle_1.movimenta_robo_e_particulas(mapa, delta, robo, particulas);
        simple_particle_1.atualiza_probabilidades(mapa, robo, particulas);
        atualiza_robo_e_particulas(mapa, 'mapa_viz', 'mapa_probs', estado_simulacao['robo'], estado_simulacao['particulas']);
    }
    window.addEventListener('load', function (e) {
        // bind everything.    
        document.getElementById('iniciar').addEventListener('click', inicia_visualizacao);
        ['U', 'D', 'W', 'E'].forEach(function (p) {
            document.getElementById(p).addEventListener('click', movimenta_robo_click);
        });
    });
});
//# sourceMappingURL=html5_viz.js.map