# Gera os PNGs dos mapas das 4 zonas (Polimento UI v2, 2026-10-30).
# Entrada: recebidos/Alturas.lua (Source de Shared/Mapa/Alturas), recebidos/mat_<zona>.txt (material do Terrain
# por amostra, 1 char = índice em mat_legenda.txt), lagoas de partida/S.Definicoes.Zonas.lua, pontos-chave fixos.
# Saída: imagens/mapa_<zona>.png (1024x1024). Orientação igual ao MapaController: +X à direita, +Z pra baixo.
import re, math, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REC = os.path.join(BASE, 'recebidos')
OUT = os.path.join(BASE, 'imagens')
TAM = 1024
ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
VAL = {c: i for i, c in enumerate(ALF)}

src = open(os.path.join(REC, 'Alturas.lua'), encoding='utf-8').read()
zonas_src = open(os.path.join(BASE, 'partida', 'S.Definicoes.Zonas.lua'), encoding='utf-8').read()
legenda = open(os.path.join(REC, 'mat_legenda.txt')).read().split('\n')

# Pontos-chave (Workspace/Mapa/Zonas/<zona>, lidos em Edit) — usados só pra trilhas sutis.
PONTOS = {
    # 1º = Mercador (centro dos corredores do terreno), depois Spawn, Portal, Altar e Baús.
    'Vila': [(-180, -60), (-360, 0), (270, 142), (270, 180), (-180, 240), (120, -270), (-90, -150), (330, -330), (-330, -300), (105, 307)],
    'Bambuzal': [(3820, -60), (3640, 0), (4270, -172), (4270, -210), (3820, 240), (4120, -270), (3910, -150), (4330, -330), (3670, -300), (4060, 300)],
    'Templo': [(7820, -60), (7640, 0), (8270, 142), (8270, 180), (7820, 240), (8120, -270), (7910, -150), (8330, -330), (7670, -300), (8060, 300)],
    'Santuario': [(11904, -33), (11850, 0), (12000, 37), (12000, 0), (11904, 129), (12063, -144), (11952, -81), (12177, -177), (11823, -159), (12033, 159)],
}
CENTRO = {'Vila': (0, 450), 'Bambuzal': (4000, 450), 'Templo': (8000, 450), 'Santuario': (12000, 240)}

# Paleta por zona: (baixo, alto) da cor do chão, cor da rocha, cor da trilha.
PALETA = {
    'Vila': dict(baixo=(64, 128, 62), alto=(156, 206, 96), rocha=(150, 112, 78), trilha=(214, 190, 140)),
    'Bambuzal': dict(baixo=(40, 98, 52), alto=(118, 180, 82), rocha=(120, 104, 90), trilha=(196, 170, 120)),
    'Templo': dict(baixo=(112, 98, 66), alto=(176, 160, 104), rocha=(96, 80, 72), trilha=(206, 186, 146)),
    'Santuario': dict(baixo=(70, 62, 92), alto=(132, 122, 156), rocha=(56, 50, 66), trilha=(176, 160, 200)),
}
# Materiais do Terrain: cor própria (mistura com a rampa) — None = usa a rampa.
COR_MAT = {
    'Grass': None, 'LeafyGrass': None, 'Slate': None,
    'Ground': 'trilha_ou_rampa', 'Mud': (122, 98, 70), 'Sandstone': 'rocha', 'Rock': 'rocha', 'Basalt': 'rocha',
    'Cobblestone': (150, 146, 140), 'Pavement': (150, 140, 170),
}


def grade(zona):
    m = re.search(r'grades\.' + zona + r' = \{ x0 = (-?\d+), z0 = (-?\d+), passo = (\d+), colunas = (\d+), linhas = (\d+), dados = decodificar\("([^"]+)"\)', src)
    x0, z0, passo, col, lin, s = int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]), m[6]
    d = np.array([(VAL[s[2 * i]] * 64 + VAL[s[2 * i + 1]] - 2048) / 10 for i in range(len(s) // 2)], dtype=np.float32)
    return x0, z0, passo, col, lin, d.reshape(lin, col)


def lagoas(zona):
    linha = [l for l in zonas_src.split('\n') if 'id = "' + zona + '"' in l][0]
    return [tuple(float(v) for v in t) for t in re.findall(r'\{ x = (-?[\d.]+), z = (-?[\d.]+), sx = ([\d.]+), sz = ([\d.]+), r = (-?[\d.]+) \}', linha)]


def redimensionar(a, tam, metodo=Image.BICUBIC):
    return np.asarray(Image.fromarray(a.astype(np.float32), mode='F').resize((tam, tam), metodo), dtype=np.float32)


def gerar(zona):
    cx, L = CENTRO[zona]
    x0, z0, passo, col, lin, h = grade(zona)
    # A grade cobre [x0, x0 + (col-1)*passo] = [cx-L, cx+L] (900 → 150 passos de 6).
    H = redimensionar(h, TAM)
    k = (2 * L) / TAM  # studs por pixel
    gz, gx = np.gradient(H, k)
    incl = np.degrees(np.arctan(np.hypot(gx, gz)))
    # Materiais (nearest).
    mats = open(os.path.join(REC, 'mat_' + zona + '.txt')).read().split('\n')
    M = np.array([[ord(c) - 64 for c in linha] for linha in mats if linha], dtype=np.int32)
    pal = PALETA[zona]
    # Rampa por altura dentro da área jogável (percentis pra não estourar com a borda).
    lo, hi = np.percentile(H, 3), np.percentile(H, 97)
    t = np.clip((H - lo) / max(1e-3, hi - lo), 0, 1)[..., None]
    cor = np.array(pal['baixo'], np.float32) * (1 - t) + np.array(pal['alto'], np.float32) * t
    # Ruído leve de textura (grama).
    rng = np.random.default_rng(7)
    ruido = redimensionar(rng.normal(0, 1, (128, 128)).astype(np.float32), TAM)
    cor *= (1 + 0.035 * ruido)[..., None]
    for idx, nome in enumerate(legenda):
        regra = COR_MAT.get(nome)
        if regra is None:
            continue
        bruto = (M == (idx + 1)).astype(np.float32)
        if not bruto.any():
            continue
        # Máscara suave (a grade é de 6 studs: sem bloquinhos).
        w = np.clip(redimensionar(bruto, TAM, Image.BILINEAR), 0, 1)
        w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
        w = np.clip((w - 0.35) / 0.3, 0, 1)[..., None]
        if regra == 'rocha':
            alvo = np.array(pal['rocha'], np.float32)
            cor = cor * (1 - 0.65 * w) + alvo * 0.65 * w
        elif regra == 'trilha_ou_rampa':
            # Ground é o chão principal no Templo; nas outras zonas é trilha/terra batida.
            if zona == 'Templo':
                continue
            alvo = np.array(pal['trilha'], np.float32)
            cor = cor * (1 - 0.6 * w) + alvo * 0.6 * w
        else:
            alvo = np.array(regra, np.float32)
            cor = cor * (1 - 0.6 * w) + alvo * 0.6 * w
    # Faces íngremes (> 25°): rocha.
    face = incl > 25
    fsuave = np.clip((incl - 22) / 8, 0, 1)[..., None]
    cor = cor * (1 - fsuave) + np.array(pal['rocha'], np.float32) * fsuave
    # Hillshade (luz do noroeste, 45° de elevação).
    az, el = math.radians(315), math.radians(45)
    lx, ly, lz = math.cos(el) * math.sin(az), math.sin(el), -math.cos(el) * math.cos(az)
    # normal = (-gx, 1, -gz) normalizado; X → leste, Z → sul (pra baixo na imagem); luz do NO = (-x, -z)
    nx, ny, nzz = -gx, np.ones_like(gx), -gz
    nn = np.sqrt(nx * nx + ny * ny + nzz * nzz)
    lum = (nx * (-0.5) + ny * 0.7 + nzz * (-0.5)) / nn / math.sqrt(0.25 + 0.49 + 0.25)
    sombra = np.clip(0.55 + 0.6 * lum, 0.45, 1.25)[..., None]
    cor = cor * sombra
    # Traço escuro no topo dos degraus (borda das faces).
    borda = face & ~np.asarray(Image.fromarray((face * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)), dtype=bool)
    img = Image.fromarray(np.clip(cor, 0, 255).astype(np.uint8), 'RGB')
    dr = ImageDraw.Draw(img, 'RGBA')
    ys, xs = np.nonzero(borda)
    escuro = tuple(int(c * 0.45) for c in pal['rocha'])
    for x, y in zip(xs[::1], ys[::1]):
        dr.point((int(x), int(y)), fill=escuro + (200,))

    def px(x, z):
        return ((x - (cx - L)) / (2 * L) * TAM, (z + L) / (2 * L) * TAM)

    # Água: retângulos girados (mesma conta do MapaChao.naLagoa: local = R(r) * delta).
    agua = Image.new('L', (TAM, TAM), 0)
    da = ImageDraw.Draw(agua)
    for (lx_, lz_, sx, sz, r) in lagoas(zona):
        rr = math.radians(r)
        c, s = math.cos(rr), math.sin(rr)
        cantos = []
        for (a, b) in ((-sx / 2, -sz / 2), (sx / 2, -sz / 2), (sx / 2, sz / 2), (-sx / 2, sz / 2)):
            # inverso: delta = R(-r) * local → dx = a*c + b*s ; dz = -a*s + b*c
            dx = a * c + b * s
            dz = -a * s + b * c
            cantos.append(px(lx_ + dx, lz_ + dz))
        da.polygon(cantos, fill=255)
    agua = agua.filter(ImageFilter.GaussianBlur(1.2))
    a = np.asarray(agua, np.float32)[..., None] / 255
    base = np.asarray(img, np.float32)
    azul = np.array((70, 140, 220), np.float32)
    claro = np.array((150, 205, 245), np.float32)
    margem = np.asarray(agua.filter(ImageFilter.MaxFilter(5)), np.float32)[..., None] / 255
    base = base * (1 - margem * 0.35) + claro * margem * 0.35
    base = base * (1 - a) + azul * a
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB')
    # Trilhas: do Mercador (centro dos corredores) até os outros pontos-chave.
    trilha = Image.new('L', (TAM, TAM), 0)
    dt = ImageDraw.Draw(trilha)
    pts = [px(x, z) for (x, z) in PONTOS[zona]]
    larg = max(5, int(8 / k))
    for p in pts[1:]:
        dt.line([pts[0], p], fill=255, width=larg)
    for p in pts:
        dt.ellipse((p[0] - larg, p[1] - larg, p[0] + larg, p[1] + larg), fill=255)
    trilha = trilha.filter(ImageFilter.GaussianBlur(1.5))
    tm = np.asarray(trilha, np.float32)[..., None] / 255 * 0.42
    contorno = np.asarray(trilha.filter(ImageFilter.MaxFilter(5)), np.float32)[..., None] / 255 * 0.25
    base = np.asarray(img, np.float32)
    base = base * (1 - contorno) + base * 0.6 * contorno
    base = base * (1 - tm) + np.array(pal['trilha'], np.float32) * tm
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB')
    # Vinheta nas bordas (fora das paredes = escuro).
    yy, xx = np.mgrid[0:TAM, 0:TAM].astype(np.float32)
    dborda = np.minimum(np.minimum(xx, TAM - 1 - xx), np.minimum(yy, TAM - 1 - yy))
    vin = np.clip(dborda / 40, 0, 1)[..., None]
    arr = np.asarray(img, np.float32) * (0.35 + 0.65 * vin)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB')
    dr = ImageDraw.Draw(img, 'RGBA')
    dr.rectangle((1, 1, TAM - 2, TAM - 2), outline=(30, 24, 20, 230), width=3)
    caminho = os.path.join(OUT, 'mapa_' + zona + '.png')
    img.save(caminho, optimize=True)
    print(zona, caminho, 'faces%', round(face.mean() * 100, 1))


if __name__ == '__main__':
    for z in (sys.argv[1:] or ['Vila', 'Bambuzal', 'Templo', 'Santuario']):
        gerar(z)
