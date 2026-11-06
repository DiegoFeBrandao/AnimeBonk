# Ícones (fallback PIL do Polimento UI v2, 2026-10-30: o Canva não estava conectado).
# Folhas 3x3 de 1024x1024 (célula 341 px, ícone ~300 px centralizado), fundo transparente.
# Cada ícone: medalhão circular com gradiente na cor do elemento + símbolo geométrico claro com contorno escuro.
# Saída: imagens/icones_<grupo>.png + imagens/icones_indice.txt (grupo;indice;id).
import math, os
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'imagens')
W = 1024  # canvas de desenho por ícone (depois reduz)
CEL = 341
ICONE = 300

KI = ((255, 214, 70), (150, 80, 10))
KI_ULT = ((255, 96, 70), (110, 14, 30))
IMP = ((255, 150, 60), (120, 40, 10))
IMP_ULT = ((255, 190, 50), (130, 60, 0))
VEN = ((90, 235, 190), (10, 90, 90))
VEN_ULT = ((110, 170, 255), (30, 30, 120))
PERG = ((176, 132, 255), (52, 26, 110))
CLARO = (255, 252, 236)
ESCURO = (24, 16, 34)


_med = {}

def medalhao(cores):
    if cores in _med:
        return _med[cores].copy()
    _med[cores] = _medalhao(cores)
    return _med[cores].copy()


def _medalhao(cores):
    img = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    claro, escuro = cores
    # gradiente radial (luz vindo de cima-esquerda)
    grad = Image.new('RGBA', (W, W))
    px = grad.load()
    cx, cy = W * 0.38, W * 0.34
    for y in range(0, W, 2):
        for x in range(0, W, 2):
            d = min(1.0, math.hypot(x - cx, y - cy) / (W * 0.75))
            c = tuple(int(claro[i] * (1 - d) + escuro[i] * d) for i in range(3)) + (255,)
            px[x, y] = c
            if x + 1 < W:
                px[x + 1, y] = c
            if y + 1 < W:
                px[x, y + 1] = c
                if x + 1 < W:
                    px[x + 1, y + 1] = c
    mask = Image.new('L', (W, W), 0)
    ImageDraw.Draw(mask).ellipse((40, 40, W - 40, W - 40), fill=255)
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse((40, 40, W - 40, W - 40), outline=ESCURO + (255,), width=34)
    d.ellipse((74, 74, W - 74, W - 74), outline=tuple(min(255, c + 60) for c in claro) + (150,), width=10)
    return img


def com_contorno(desenho):
    """desenho(d, cor, extra) desenha o símbolo; faz uma passada escura grossa e outra clara."""
    sim = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    m = Image.new('L', (W, W), 0)
    desenho(ImageDraw.Draw(m), 255, 0)
    sombra = m.filter(ImageFilter.MaxFilter(31))
    sim.paste(Image.new('RGBA', (W, W), ESCURO + (255,)), (0, 0), sombra)
    sim.paste(Image.new('RGBA', (W, W), CLARO + (255,)), (0, 0), m)
    return sim


def poli(d, pts, f):
    d.polygon([(x * W, y * W) for x, y in pts], fill=f)


def circ(d, x, y, r, f):
    d.ellipse(((x - r) * W, (y - r) * W, (x + r) * W, (y + r) * W), fill=f)


def anel(d, x, y, r, f, larg):
    d.ellipse(((x - r) * W, (y - r) * W, (x + r) * W, (y + r) * W), outline=f, width=int(larg * W))


def linha(d, pts, f, larg):
    d.line([(x * W, y * W) for x, y in pts], fill=f, width=int(larg * W), joint='curve')
    for x, y in (pts[0], pts[-1]):
        circ(d, x, y, larg / 2, f)


def arco(d, x, y, r, a0, a1, f, larg):
    d.arc(((x - r) * W, (y - r) * W, (x + r) * W, (y + r) * W), a0, a1, fill=f, width=int(larg * W))


def retrot(d, cx, cy, w, h, ang, f):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    pts = []
    for (px_, py_) in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        pts.append((cx + px_ * c - py_ * s, cy + px_ * s + py_ * c))
    poli(d, pts, f)


def estrela(d, cx, cy, r1, r2, n, f, giro=-90):
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(giro + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    poli(d, pts, f)


def punho(d, cx, cy, t, f):
    # punho visto de frente: bloco arredondado + 4 nós dos dedos + polegar
    d.rounded_rectangle(((cx - t) * W, (cy - t * 0.7) * W, (cx + t) * W, (cy + t * 0.9) * W), radius=int(t * 0.35 * W), fill=f)
    for i in range(4):
        circ(d, cx - t * 0.75 + i * t * 0.5, cy - t * 0.7, t * 0.27, f)


def kunai(d, cx, cy, comp, ang, f):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    ponta = (cx + ux * comp * 0.5, cy + uy * comp * 0.5)
    base = (cx - ux * comp * 0.05, cy - uy * comp * 0.05)
    lw = comp * 0.14
    poli(d, [ponta, (base[0] + vx * lw, base[1] + vy * lw), (base[0] - vx * lw, base[1] - vy * lw)], f)
    linha(d, [base, (cx - ux * comp * 0.38, cy - uy * comp * 0.38)], f, comp * 0.07)
    anel(d, cx - ux * comp * 0.45, cy - uy * comp * 0.45, comp * 0.07, f, comp * 0.04)


def coracao(d, cx, cy, t, f):
    circ(d, cx - t * 0.5, cy - t * 0.25, t * 0.55, f)
    circ(d, cx + t * 0.5, cy - t * 0.25, t * 0.55, f)
    poli(d, [(cx - t * 1.02, cy - t * 0.1), (cx + t * 1.02, cy - t * 0.1), (cx, cy + t * 1.05)], f)


def escudo(d, cx, cy, t, f):
    poli(d, [(cx - t, cy - t * 0.8), (cx, cy - t * 1.05), (cx + t, cy - t * 0.8), (cx + t * 0.9, cy + t * 0.2), (cx, cy + t * 1.1), (cx - t * 0.9, cy + t * 0.2)], f)


def raio_simb(d, cx, cy, t, f):
    poli(d, [(cx + t * 0.15, cy - t), (cx - t * 0.6, cy + t * 0.1), (cx - t * 0.05, cy + t * 0.1), (cx - t * 0.25, cy + t), (cx + t * 0.6, cy - t * 0.15), (cx + t * 0.05, cy - t * 0.15)], f)


# ---------------- símbolos ----------------
S = {}

def s(nome):
    def reg(fn):
        S[nome] = fn
        return fn
    return reg

# Ryuga
@s('RajadaKi')
def _(d, f, e):
    circ(d, 0.56, 0.44, 0.17, f)
    for i, (dx, dy) in enumerate(((-0.2, 0.2), (-0.27, 0.1), (-0.12, 0.28))):
        linha(d, [(0.5 + dx * 0.5, 0.5 + dy * 0.5), (0.5 + dx * 1.35, 0.5 + dy * 1.35)], f, 0.05)

@s('ChuvaSocos')
def _(d, f, e):
    punho(d, 0.36, 0.38, 0.1, f)
    punho(d, 0.62, 0.36, 0.1, f)
    punho(d, 0.5, 0.62, 0.12, f)

@s('PassoInstantaneo')
def _(d, f, e):
    for i in range(2):
        x = 0.4 + i * 0.2
        linha(d, [(x - 0.1, 0.3), (x + 0.08, 0.5), (x - 0.1, 0.7)], f, 0.07)
    for y in (0.36, 0.5, 0.64):
        linha(d, [(0.18, y), (0.28, y)], f, 0.035)

@s('CanhaoKi')
def _(d, f, e):
    poli(d, [(0.3, 0.42), (0.82, 0.36), (0.82, 0.64), (0.3, 0.58)], f)
    circ(d, 0.3, 0.5, 0.15, f)

@s('OrbitaKi')
def _(d, f, e):
    anel(d, 0.5, 0.5, 0.25, f, 0.035)
    for a in (-90, 30, 150):
        r = math.radians(a)
        circ(d, 0.5 + 0.25 * math.cos(r), 0.5 + 0.25 * math.sin(r), 0.085, f)
    circ(d, 0.5, 0.5, 0.06, f)

@s('PilarAscendente')
def _(d, f, e):
    d.ellipse((0.24 * W, 0.66 * W, 0.76 * W, 0.8 * W), fill=f)
    poli(d, [(0.4, 0.73), (0.4, 0.38), (0.3, 0.38), (0.5, 0.18), (0.7, 0.38), (0.6, 0.38), (0.6, 0.73)], f)

@s('UltExplosaoKi')
def _(d, f, e):
    estrela(d, 0.5, 0.5, 0.33, 0.16, 8, f)

@s('UltMeteoroCarmesim')
def _(d, f, e):
    circ(d, 0.6, 0.6, 0.15, f)
    poli(d, [(0.5, 0.48), (0.2, 0.2), (0.72, 0.5)], f)
    poli(d, [(0.53, 0.62), (0.28, 0.48), (0.66, 0.46)], f)

@s('UltRaioCelestial')
def _(d, f, e):
    poli(d, [(0.4, 0.16), (0.6, 0.16), (0.56, 0.7), (0.44, 0.7)], f)
    d.ellipse((0.26 * W, 0.66 * W, 0.74 * W, 0.8 * W), fill=f)
    for x in (0.28, 0.72):
        linha(d, [(x, 0.3), (x + (0.5 - x) * 0.25, 0.46)], f, 0.03)

# Kaizo
@s('SocoEstilingue')
def _(d, f, e):
    linha(d, [(0.2, 0.7), (0.42, 0.55)], f, 0.07)
    for i in range(3):
        linha(d, [(0.22 + i * 0.07, 0.78 - i * 0.03), (0.28 + i * 0.07, 0.72 - i * 0.03)], f, 0.025)
    punho(d, 0.6, 0.42, 0.14, f)

@s('MetralhadoraSocos')
def _(d, f, e):
    for (x, y) in ((0.34, 0.34), (0.66, 0.34), (0.5, 0.5), (0.34, 0.66), (0.66, 0.66)):
        punho(d, x, y, 0.075, f)

@s('ChicotePerna')
def _(d, f, e):
    arco(d, 0.5, 0.55, 0.28, 200, 340, f, 0.09)
    poli(d, [(0.73, 0.32), (0.84, 0.47), (0.68, 0.46)], f)

@s('BalaMola')
def _(d, f, e):
    pts = [(0.22, 0.5)]
    for i in range(6):
        pts.append((0.27 + i * 0.05, 0.38 if i % 2 == 0 else 0.62))
    pts.append((0.55, 0.5))
    linha(d, pts, f, 0.04)
    d.rounded_rectangle((0.56 * W, 0.4 * W, 0.8 * W, 0.6 * W), radius=int(0.1 * W), fill=f)

@s('ChicoteMola')
def _(d, f, e):
    pts = []
    for i in range(41):
        t = i / 40
        pts.append((0.2 + 0.6 * t, 0.5 + 0.18 * math.sin(t * math.pi * 2.5)))
    linha(d, pts, f, 0.06)

@s('AncoraQueda')
def _(d, f, e):
    anel(d, 0.5, 0.25, 0.06, f, 0.035)
    linha(d, [(0.5, 0.31), (0.5, 0.74)], f, 0.06)
    linha(d, [(0.36, 0.42), (0.64, 0.42)], f, 0.05)
    arco(d, 0.5, 0.56, 0.22, 20, 160, f, 0.06)
    poli(d, [(0.25, 0.6), (0.33, 0.66), (0.24, 0.7)], f)
    poli(d, [(0.75, 0.6), (0.67, 0.66), (0.76, 0.7)], f)

@s('UltSocoCanhao')
def _(d, f, e):
    punho(d, 0.46, 0.52, 0.18, f)
    for a in (-40, 0, 40):
        r = math.radians(a)
        linha(d, [(0.5 + 0.3 * math.cos(r), 0.5 + 0.3 * math.sin(r)), (0.5 + 0.38 * math.cos(r), 0.5 + 0.38 * math.sin(r))], f, 0.04)

@s('UltChuvaPunhos')
def _(d, f, e):
    for (x, y) in ((0.32, 0.4), (0.68, 0.36), (0.5, 0.62)):
        linha(d, [(x, y - 0.24), (x, y - 0.12)], f, 0.03)
        punho(d, x, y, 0.09, f)

@s('UltMarteloCapitao')
def _(d, f, e):
    retrot(d, 0.55, 0.58, 0.08, 0.5, -40, f)
    retrot(d, 0.4, 0.4, 0.42, 0.22, -40, f)

# Haruto
@s('ChuvaKunai')
def _(d, f, e):
    for x, y in ((0.34, 0.45), (0.5, 0.55), (0.66, 0.45)):
        kunai(d, x, y, 0.42, 90, f)

@s('ShurikenVento')
def _(d, f, e):
    estrela(d, 0.5, 0.5, 0.32, 0.09, 4, f, giro=-45)
    circ(d, 0.5, 0.5, 0.05, 0)

@s('SeloExplosivo')
def _(d, f, e):
    retrot(d, 0.46, 0.55, 0.22, 0.4, -12, f)
    estrela(d, 0.66, 0.3, 0.12, 0.05, 6, f)

@s('LaminaVento')
def _(d, f, e):
    arco(d, 0.36, 0.5, 0.34, 300, 60, f, 0.12)
    arco(d, 0.3, 0.5, 0.24, 310, 50, f, 0.045)

@s('PassoSombra')
def _(d, f, e):
    linha(d, [(0.22, 0.78), (0.78, 0.22)], f, 0.05)
    circ(d, 0.38, 0.38, 0.08, f)
    poli(d, [(0.3, 0.48), (0.46, 0.48), (0.5, 0.7), (0.26, 0.7)], f)

@s('VoleioEspelho')
def _(d, f, e):
    for a in (-125, -90, -55):
        r = math.radians(a)
        kunai(d, 0.5 + 0.2 * math.cos(r), 0.66 + 0.2 * math.sin(r), 0.42, a, f)

@s('UltMilClones')
def _(d, f, e):
    for x, y, t in ((0.3, 0.52, 0.8), (0.7, 0.52, 0.8), (0.5, 0.5, 1.0)):
        circ(d, x, y - 0.14 * t, 0.075 * t, f)
        d.rounded_rectangle(((x - 0.1 * t) * W, (y - 0.05 * t) * W, (x + 0.1 * t) * W, (y + 0.25 * t) * W), radius=int(0.06 * t * W), fill=f)

@s('UltUivoLobo')
def _(d, f, e):
    poli(d, [(0.3, 0.3), (0.38, 0.42), (0.5, 0.38), (0.62, 0.42), (0.7, 0.3), (0.72, 0.55), (0.5, 0.75), (0.28, 0.55)], f)
    arco(d, 0.5, 0.52, 0.34, 200, 250, f, 0.03)
    arco(d, 0.5, 0.52, 0.34, 290, 340, f, 0.03)

@s('UltFeraLibertada')
def _(d, f, e):
    for i in range(3):
        x = 0.36 + i * 0.13
        poli(d, [(x, 0.22), (x + 0.05, 0.25), (x - 0.06, 0.8), (x - 0.09, 0.76)], f)

# Pergaminhos
@s('Dano')
def _(d, f, e):
    retrot(d, 0.47, 0.47, 0.08, 0.5, 45, f)
    poli(d, [(0.62, 0.22), (0.74, 0.26), (0.66, 0.36)], f)
    retrot(d, 0.33, 0.67, 0.22, 0.06, -45, f)
    linha(d, [(0.3, 0.7), (0.2, 0.8)], f, 0.05)

@s('VelAtaque')
def _(d, f, e):
    anel(d, 0.5, 0.52, 0.24, f, 0.05)
    linha(d, [(0.5, 0.52), (0.5, 0.36)], f, 0.05)
    linha(d, [(0.5, 0.52), (0.62, 0.6)], f, 0.05)
    linha(d, [(0.5, 0.22), (0.5, 0.26)], f, 0.08)

@s('Projeteis')
def _(d, f, e):
    for a in (-130, -90, -50):
        r = math.radians(a)
        circ(d, 0.5 + 0.24 * math.cos(r), 0.66 + 0.24 * math.sin(r) - 0.06, 0.07, f)
    circ(d, 0.5, 0.68, 0.06, f)

@s('Area')
def _(d, f, e):
    anel(d, 0.5, 0.5, 0.28, f, 0.04)
    anel(d, 0.5, 0.5, 0.16, f, 0.04)
    circ(d, 0.5, 0.5, 0.05, f)

@s('Duracao')
def _(d, f, e):
    poli(d, [(0.32, 0.24), (0.68, 0.24), (0.52, 0.5), (0.68, 0.76), (0.32, 0.76), (0.48, 0.5)], f)

@s('Critico')
def _(d, f, e):
    anel(d, 0.5, 0.5, 0.22, f, 0.045)
    for (a, b) in (((0.5, 0.2), (0.5, 0.36)), ((0.5, 0.64), (0.5, 0.8)), ((0.2, 0.5), (0.36, 0.5)), ((0.64, 0.5), (0.8, 0.5))):
        linha(d, [a, b], f, 0.045)
    circ(d, 0.5, 0.5, 0.04, f)

@s('HpMax')
def _(d, f, e):
    coracao(d, 0.5, 0.48, 0.26, f)

@s('Armadura')
def _(d, f, e):
    escudo(d, 0.5, 0.5, 0.27, f)

@s('Regen')
def _(d, f, e):
    coracao(d, 0.46, 0.5, 0.2, f)
    retrot(d, 0.7, 0.32, 0.18, 0.06, 0, f)
    retrot(d, 0.7, 0.32, 0.06, 0.18, 0, f)

@s('Velocidade')
def _(d, f, e):
    for i in range(3):
        x = 0.3 + i * 0.17
        linha(d, [(x, 0.32), (x + 0.12, 0.5), (x, 0.68)], f, 0.06)

@s('Coleta')
def _(d, f, e):
    arco(d, 0.5, 0.46, 0.2, 180, 360, f, 0.1)
    retrot(d, 0.35, 0.58, 0.1, 0.24, 0, f)
    retrot(d, 0.65, 0.58, 0.1, 0.24, 0, f)

@s('Xp')
def _(d, f, e):
    estrela(d, 0.5, 0.52, 0.3, 0.13, 5, f)

@s('Escudo')
def _(d, f, e):
    escudo(d, 0.5, 0.52, 0.2, f)
    arco(d, 0.5, 0.52, 0.32, 200, 340, f, 0.035)

@s('VelProjetil')
def _(d, f, e):
    linha(d, [(0.22, 0.62), (0.62, 0.38)], f, 0.06)
    poli(d, [(0.78, 0.28), (0.58, 0.3), (0.68, 0.46)], f)
    for i in range(2):
        linha(d, [(0.2 + i * 0.06, 0.48 + i * 0.1), (0.3 + i * 0.06, 0.42 + i * 0.1)], f, 0.03)

@s('Evasao')
def _(d, f, e):
    for i, y in enumerate((0.36, 0.5, 0.64)):
        pts = [(0.22 + 0.56 * t / 20, y + 0.04 * math.sin(t / 20 * math.pi * 3 + i)) for t in range(21)]
        linha(d, pts, f, 0.05)

@s('ChanceStatus')
def _(d, f, e):
    pts = [(0.5 + 0.28 * math.cos(math.radians(60 * i - 90)), 0.5 + 0.28 * math.sin(math.radians(60 * i - 90))) for i in range(6)]
    linha(d, pts + [pts[0]], f, 0.05)
    circ(d, 0.5, 0.5, 0.08, f)

@s('Moedas')
def _(d, f, e):
    circ(d, 0.5, 0.5, 0.26, f)
    d.rectangle((0.44 * W, 0.44 * W, 0.56 * W, 0.56 * W), fill=0)

@s('Sorte')
def _(d, f, e):
    for (x, y) in ((0.5, 0.36), (0.36, 0.5), (0.64, 0.5), (0.5, 0.64)):
        circ(d, x, y, 0.12, f)
    linha(d, [(0.5, 0.6), (0.6, 0.8)], f, 0.04)

@s('RouboVida')
def _(d, f, e):
    circ(d, 0.5, 0.58, 0.18, f)
    poli(d, [(0.5, 0.2), (0.34, 0.52), (0.66, 0.52)], f)

@s('Espinhos')
def _(d, f, e):
    for i in range(4):
        x = 0.27 + i * 0.155
        poli(d, [(x - 0.07, 0.72), (x, 0.3 + (i % 2) * 0.08), (x + 0.07, 0.72)], f)
    d.rectangle((0.2 * W, 0.7 * W, 0.8 * W, 0.78 * W), fill=f)

@s('Sobrecura')
def _(d, f, e):
    coracao(d, 0.5, 0.56, 0.2, f)
    poli(d, [(0.5, 0.14), (0.38, 0.3), (0.62, 0.3)], f)

@s('Elites')
def _(d, f, e):
    poli(d, [(0.24, 0.66), (0.24, 0.34), (0.37, 0.48), (0.5, 0.28), (0.63, 0.48), (0.76, 0.34), (0.76, 0.66)], f)
    d.rectangle((0.24 * W, 0.68 * W, 0.76 * W, 0.75 * W), fill=f)

@s('CargaUltimate')
def _(d, f, e):
    raio_simb(d, 0.5, 0.5, 0.3, f)

@s('Amaldicoado')
def _(d, f, e):
    d.ellipse((0.2 * W, 0.34 * W, 0.8 * W, 0.66 * W), fill=f)
    circ(d, 0.5, 0.5, 0.11, 0)
    circ(d, 0.5, 0.5, 0.05, f)


GRUPOS = [
    ('ryuga', KI, ['RajadaKi', 'ChuvaSocos', 'PassoInstantaneo', 'CanhaoKi', 'OrbitaKi', 'PilarAscendente'], KI_ULT, ['UltExplosaoKi', 'UltMeteoroCarmesim', 'UltRaioCelestial']),
    ('kaizo', IMP, ['SocoEstilingue', 'MetralhadoraSocos', 'ChicotePerna', 'BalaMola', 'ChicoteMola', 'AncoraQueda'], IMP_ULT, ['UltSocoCanhao', 'UltChuvaPunhos', 'UltMarteloCapitao']),
    ('haruto', VEN, ['ChuvaKunai', 'ShurikenVento', 'SeloExplosivo', 'LaminaVento', 'PassoSombra', 'VoleioEspelho'], VEN_ULT, ['UltMilClones', 'UltUivoLobo', 'UltFeraLibertada']),
]
PERGS = ['Dano', 'VelAtaque', 'Projeteis', 'Area', 'Duracao', 'Critico', 'HpMax', 'Armadura', 'Regen', 'Velocidade', 'Coleta', 'Xp',
         'Escudo', 'VelProjetil', 'Evasao', 'ChanceStatus', 'Moedas', 'Sorte', 'RouboVida', 'Espinhos', 'Sobrecura', 'Elites', 'CargaUltimate', 'Amaldicoado']
# Tom do medalhão por pergaminho (variação do roxo pra separar visualmente).
TOM_PERG = {
    'Dano': ((255, 110, 90), (110, 20, 40)), 'HpMax': ((255, 110, 140), (110, 20, 50)), 'Regen': ((120, 230, 140), (20, 90, 50)),
    'Moedas': ((255, 210, 80), (130, 80, 10)), 'Xp': ((120, 200, 255), (20, 60, 130)), 'Amaldicoado': ((120, 60, 140), (20, 6, 30)),
}

_cache = {}

def icone(nome, cores):
    chave = (nome, cores)
    if chave in _cache:
        return _cache[chave]
    base = medalhao(cores)
    sim = com_contorno(S[nome])
    base.alpha_composite(sim)
    pequeno = base.resize((ICONE, ICONE), Image.LANCZOS)
    _cache[chave] = pequeno
    return pequeno


def folha(nome, itens):
    img = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
    for i, (id_, cores) in enumerate(itens):
        ic = icone(id_, cores)
        cx, cy = i % 3, i // 3
        off = (CEL - ICONE) // 2
        img.alpha_composite(ic, (cx * CEL + off, cy * CEL + off))
    caminho = os.path.join(OUT, 'icones_' + nome + '.png')
    img.save(caminho, optimize=True)
    return caminho


if __name__ == '__main__':
    indice = []
    for nome, c1, golpes, c2, ults in GRUPOS:
        itens = [(g, c1) for g in golpes] + [(u, c2) for u in ults]
        folha(nome, itens)
        for i, (id_, _) in enumerate(itens):
            indice.append(f'{nome};{i};{id_}')
    for k, fatia in enumerate((PERGS[0:9], PERGS[9:18], PERGS[18:])):
        nome = f'pergaminhos{k + 1}'
        folha(nome, [(p, TOM_PERG.get(p, PERG)) for p in fatia])
        for i, p in enumerate(fatia):
            indice.append(f'{nome};{i};{p}')
    open(os.path.join(OUT, 'icones_indice.txt'), 'w').write('\n'.join(indice))
    print(len(indice), 'icones')
