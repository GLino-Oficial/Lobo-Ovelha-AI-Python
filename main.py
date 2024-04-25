import pygame
import random
import math

# Definindo cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
LARANJA = (255, 165, 0)
VERDE = (0, 128, 0)
VERMELHO = (255, 0, 0)

# Definindo configurações do ambiente
TAMANHO_GRADE = 10
TAMANHO_CELULA = 50
LARGURA = TAMANHO_GRADE * TAMANHO_CELULA
ALTURA = TAMANHO_GRADE * TAMANHO_CELULA

# Classe para representar a ovelha
class Ovelha:
    def __init__(self):
        self.x = random.randint(0, TAMANHO_GRADE - 1)
        self.y = random.randint(0, TAMANHO_GRADE - 1)
        self.grama_coletada = 0

    def mover_em_direcao_da_grama(self, posicoes_grama):
        if posicoes_grama:
            grama_mais_proxima = min(posicoes_grama, key=lambda pos: math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2))
            alvo_x, alvo_y = grama_mais_proxima
            dx = alvo_x - self.x
            dy = alvo_y - self.y

            if dx != 0:
                self.x += dx // abs(dx)
            if dy != 0:
                self.y += dy // abs(dy)

            self.x = max(0, min(self.x, TAMANHO_GRADE - 1))
            self.y = max(0, min(self.y, TAMANHO_GRADE - 1))

    def coletar_grama(self, posicoes_grama):
        if (self.x, self.y) in posicoes_grama:
            posicoes_grama.remove((self.x, self.y))
            self.grama_coletada += 1

# Classe para representar o lobo
class Lobo:
    def __init__(self):
        self.x = random.randint(0, TAMANHO_GRADE - 1)
        self.y = random.randint(0, TAMANHO_GRADE - 1)
        self.ovelhas_capturadas = 0

    def mover_em_direcao_da_ovelha(self, x_ovelha, y_ovelha):
        dx = x_ovelha - self.x
        dy = y_ovelha - self.y

        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        dx = abs(dx)
        dy = abs(dy)
        err = dx - dy

        if dx == 0 and dy == 0:
            return

        if dx > dy:
            self.x += sx
        else:
            self.y += sy

        self.x = max(0, min(self.x, TAMANHO_GRADE - 1))
        self.y = max(0, min(self.y, TAMANHO_GRADE - 1))

    def verificar_ovelha_capturada(self, ovelha):
        if self.x == ovelha.x and self.y == ovelha.y:
            self.ovelhas_capturadas += 1
            ovelha.x = random.randint(0, TAMANHO_GRADE - 1)
            ovelha.y = random.randint(0, TAMANHO_GRADE - 1)

# Inicializando o Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA + 50))  # Altura aumentada para exibir os contadores
pygame.display.set_caption("Ambiente de Ovelha e Lobo")

# Função para desenhar o ambiente
def desenhar_ambiente(ovelha, lobo, posicoes_grama):
    tela.fill(BRANCO)
    for x in range(TAMANHO_GRADE):
        for y in range(TAMANHO_GRADE):
            retangulo = pygame.Rect(x * TAMANHO_CELULA, y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
            pygame.draw.rect(tela, PRETO, retangulo, 1)
    for posicao_grama in posicoes_grama:
        pygame.draw.circle(tela, VERDE, (posicao_grama[0] * TAMANHO_CELULA + TAMANHO_CELULA // 2, posicao_grama[1] * TAMANHO_CELULA + TAMANHO_CELULA // 2), 5)
    pygame.draw.circle(tela, LARANJA, (ovelha.x * TAMANHO_CELULA + TAMANHO_CELULA // 2, ovelha.y * TAMANHO_CELULA + TAMANHO_CELULA // 2), 15)
    pygame.draw.circle(tela, VERMELHO, (lobo.x * TAMANHO_CELULA + TAMANHO_CELULA // 2, lobo.y * TAMANHO_CELULA + TAMANHO_CELULA // 2), 20)

# Função para gerar posições de grama
def gerar_posicoes_grama():
    return [(random.randint(0, TAMANHO_GRADE - 1), random.randint(0, TAMANHO_GRADE - 1)) for _ in range(20)]

# Inicialização da fonte
fonte = pygame.font.SysFont(None, 24)

# Instanciando a ovelha e o lobo
ovelha = Ovelha()
lobo = Lobo()

# Lista para armazenar as posições de grama
posicoes_grama = gerar_posicoes_grama()

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    ovelha.mover_em_direcao_da_grama(posicoes_grama)
    ovelha.coletar_grama(posicoes_grama)
    lobo.mover_em_direcao_da_ovelha(ovelha.x, ovelha.y)
    lobo.verificar_ovelha_capturada(ovelha)

    # Regenerar posições de grama se todas forem removidas
    if not posicoes_grama:
        posicoes_grama = gerar_posicoes_grama()

    desenhar_ambiente(ovelha, lobo, posicoes_grama)  # Desenhando o ambiente

    # Exibindo contadores
    texto_contador_ovelha = fonte.render("Ovelha -  Grama Coletada: " + str(ovelha.grama_coletada), True, PRETO)
    retangulo_contador_ovelha = texto_contador_ovelha.get_rect()
    retangulo_contador_ovelha.topleft = (10, ALTURA)  # Posição ajustada
    tela.blit(texto_contador_ovelha, retangulo_contador_ovelha)

    texto_contador_lobo = fonte.render("Lobo - Ovelha Capturada: " + str(lobo.ovelhas_capturadas), True, PRETO)
    retangulo_contador_lobo = texto_contador_lobo.get_rect()
    retangulo_contador_lobo.topleft = (10, ALTURA + 20)  # Posição ajustada
    tela.blit(texto_contador_lobo, retangulo_contador_lobo)

    pygame.display.flip()
    pygame.time.delay(250)  # Ajuste o atraso aqui para a velocidade de movimento

pygame.quit()
