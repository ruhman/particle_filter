define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function cria_particulas(mapa) {
        var particulas = [];
        for (var i = 0; i < mapa.length; i++) {
            for (var j = 0; j < mapa[i].length; j++) {
                if (mapa[i][j] != '#') {
                    var p = { i: i, j: j, prob_H: 0 };
                    particulas.push(p);
                }
            }
        }
        for (var i = 0; i < particulas.length; i++) {
            particulas[i].prob_H = 1 / particulas.length;
        }
        return particulas;
    }
    exports.cria_particulas = cria_particulas;
    function leitura_sensores(mapa, i, j) {
        var x = i + 1;
        var u = (i > 0) ? mapa[i - 1][j] != '#' : false;
        var d = (i < mapa.length - 1) ? mapa[i + 1][j] != '#' : false;
        var w = (j > 0) ? mapa[i][j - 1] != '#' : false;
        var e = (j < mapa[i].length - 1) ? mapa[i][j + 1] != '#' : false;
        return [u, d, w, e];
    }
    exports.leitura_sensores = leitura_sensores;
    function probabilidade_Dados_Hipotese(leitura_real, leitura_particula) {
        var c = 0;
        for (var i = 0; i < 4; i++) {
            c += leitura_real[i] == leitura_particula[i] ? 1 : 0;
        }
        return c / 4;
    }
    exports.probabilidade_Dados_Hipotese = probabilidade_Dados_Hipotese;
    function movimento_valido(mapa, r, delta) {
        if (r.i + delta[0] < 0 || r.i + delta[0] >= mapa.length ||
            r.j + delta[1] < 0 || r.j + delta[1] >= mapa[0].length) {
            return false;
        }
        if (mapa[r.i + delta[0]][r.j + delta[1]] == '#') {
            return false;
        }
        return true;
    }
    function movimenta_robo_e_particulas(mapa, delta, r, particulas) {
        if (!movimento_valido(mapa, r, delta)) {
            return r;
        }
        r.i += delta[0];
        r.j += delta[1];
        var excluir = [];
        for (var i = 0; i < particulas.length; i++) {
            var p = particulas[i];
            if (movimento_valido(mapa, p, delta)) {
                p.i += delta[0];
                p.j += delta[1];
            }
            else {
                excluir.push(i);
            }
        }
        for (var i = excluir.length - 1; i >= 0; i--) {
            particulas.splice(excluir[i], 1);
        }
        atualiza_probabilidades(mapa, r, particulas);
        return r;
    }
    exports.movimenta_robo_e_particulas = movimenta_robo_e_particulas;
    function atualiza_probabilidades(mapa, r, particulas) {
        var acc = 0;
        for (var i = 0; i < particulas.length; i++) {
            var p = particulas[i];
            var l_real = leitura_sensores(mapa, r.i, r.j);
            var l_part = leitura_sensores(mapa, p.i, p.j);
            var prob = probabilidade_Dados_Hipotese(l_real, l_part) * p.prob_H;
            p.prob_H = prob;
            acc += prob;
        }
        for (var i = 0; i < particulas.length; i++) {
            var p = particulas[i];
            p.prob_H /= acc;
        }
    }
    exports.atualiza_probabilidades = atualiza_probabilidades;
});
//# sourceMappingURL=simple_particle.js.map