
export interface Particula {
    i:number,
    j:number,
    prob_H: number
}

export interface Robo {
    i:number,
    j:number
}

export function cria_particulas(mapa:string[]):Particula[] {
    let particulas:Particula[] = [];
    for (var i = 0; i < mapa.length; i++) {
        for(var j = 0; j < mapa[i].length; j++) {
            if (mapa[i][j] != '#') {
                let p = {i:i, j:j, prob_H: 0};
                particulas.push(p);
            }
        }
    }
    for (var i = 0; i < particulas.length; i++) {
        particulas[i].prob_H = 1/particulas.length;
    }
    return particulas;
}

export function leitura_sensores(mapa:string[], i:number, j:number):[boolean, boolean, boolean, boolean] {
    let x:number = i+1;
    let u = (i > 0)?mapa[i-1][j]!='#':false;
    let d = (i < mapa.length-1)?mapa[i+1][j]!='#':false;
    let w = (j > 0)?mapa[i][j-1]!='#':false;
    let e = (j < mapa[i].length-1)?mapa[i][j+1]!='#':false;
    return [u, d, w, e];
}

export function probabilidade_Dados_Hipotese(leitura_real:[boolean, boolean, boolean, boolean], leitura_particula:[boolean, boolean, boolean, boolean]):number {
    let c = 0
    for (var i = 0; i < 4; i++) {
        c += leitura_real[i]==leitura_particula[i]?1:0;
    }
    return c/4;
}

function movimento_valido(mapa:string[], r:Robo, delta:[number, number]):boolean{
    if (r.i + delta[0] < 0 || r.i + delta[0] >= mapa.length ||
        r.j + delta[1] < 0 || r.j + delta[1] >= mapa[0].length) {
            return false;
        }

    if (mapa[r.i + delta[0]][r.j + delta[1]] == '#') { 
        return false;
    }

    return true;
}

export function movimenta_robo_e_particulas(mapa:string[], delta:[number, number], r:Robo, particulas:Particula[]):Robo {
    if (!movimento_valido(mapa, r, delta)) {
        return r;
    }
    r.i += delta[0];
    r.j += delta[1];
    
    let excluir = [];
    for (var i = 0; i < particulas.length; i++) {
        let p = particulas[i];
        if (movimento_valido(mapa, p, delta)) {
            p.i += delta[0];
            p.j += delta[1];
        } else {
            excluir.push(i);
        }
    }

    for (var i = excluir.length-1; i >= 0; i--) {
        particulas.splice(excluir[i], 1);
    }

    atualiza_probabilidades(mapa, r, particulas);

    return r;
}

export function atualiza_probabilidades(mapa:string[], r:Robo, particulas:Particula[]):void {
    let acc = 0;
    for (var i = 0; i < particulas.length; i++) {
        let p = particulas[i];
        let l_real = leitura_sensores(mapa, r.i, r.j);
        let l_part = leitura_sensores(mapa, p.i, p.j);
        let prob = probabilidade_Dados_Hipotese(l_real, l_part) * p.prob_H;
        p.prob_H = prob;
        acc += prob;
    }

    for (var i = 0; i < particulas.length; i++) {
        let p = particulas[i];
        p.prob_H /= acc;
    }
}