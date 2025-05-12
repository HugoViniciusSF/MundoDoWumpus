import pygame
import random
import sys

# --- Inicialização do Pygame ---
pygame.init()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 36)
clock = pygame.time.Clock()

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 120, 255)
BREEZE = (173, 216, 230)
STENCH = (200, 255, 200)
RED = (255, 100, 100)
GRAY = (40, 40, 40)
GREEN = (0, 255, 100)

# --- Estados do Jogo ---
TELA_MENU = "menu"
JOGANDO = "jogando"
GAME_OVER = "game_over"
WIN = "win"


# --- Funções auxiliares ---
def desenhar_texto_centralizado(texto, y, screen, fonte, cor=WHITE):
    rendered = fonte.render(texto, True, cor)
    rect = rendered.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(rendered, rect)


def botao(texto, x, y, w, h, screen, callback):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = (
        (70, 70, 70) if x < mouse[0] < x + w and y < mouse[1] < y + h else (50, 50, 50)
    )
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)
    txt = font.render(texto, True, WHITE)
    screen.blit(txt, (x + 10, y + 10))

    if x < mouse[0] < x + w and y < mouse[1] < y + h and click[0]:
        callback()


# --- Classe principal ---
class JogoWumpus:
    def __init__(self, grid=4):
        self.grid = grid
        self.cell_size = 80
        self.width = self.grid * self.cell_size + 600
        self.height = self.grid * self.cell_size + 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mundo do Wumpus")
        self.estado = TELA_MENU
        self.reset()

    def reset(self):
        self.agent_pos = [0, 0]
        self.wumpus = self.random_pos(exclude=[(0, 0)])
        self.gold = self.random_pos(exclude=[(0, 0), self.wumpus])
        self.pits = []
        while len(self.pits) < 3:
            p = self.random_pos(exclude=[(0, 0), self.wumpus, self.gold] + self.pits)
            self.pits.append(p)
        self.ouro_pego = False
        self.morto = False

    def random_pos(self, exclude=[]):
        while True:
            pos = (random.randint(0, self.grid - 1), random.randint(0, self.grid - 1))
            if pos not in exclude:
                return pos

    def get_perceptions(self):
        x, y = self.agent_pos
        percep = []
        if (x, y) == self.gold:
            percep.append("brilho")
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid and 0 <= ny < self.grid:
                if (nx, ny) == self.wumpus:
                    percep.append("cheiro")
                if (nx, ny) in self.pits:
                    percep.append("brisa")
        return percep

    def desenhar_grid(self):
        for i in range(self.grid):
            for j in range(self.grid):
                rect = pygame.Rect(
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, GRAY, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)

    def desenhar_objeto(self, pos, cor, texto):
        x = pos[1] * self.cell_size + self.cell_size // 2
        y = pos[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, cor, (x, y), 15)
        self.screen.blit(font.render(texto, True, BLACK), (x - 8, y - 10))

    def desenhar_agente(self):
        x = self.agent_pos[1] * self.cell_size + self.cell_size // 2
        y = self.agent_pos[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, BLUE, (x, y), 20)

    def desenhar_hud(self, percep):
        pygame.draw.rect(self.screen, BLACK, (0, self.height - 100, self.width, 100))
        texto = font.render("Percepções: " + ", ".join(percep), True, WHITE)
        self.screen.blit(texto, (10, self.height - 80))

    def mover_agente(self, dx, dy):
        if self.morto:
            return
        novo_x = self.agent_pos[0] + dx
        novo_y = self.agent_pos[1] + dy
        if 0 <= novo_x < self.grid and 0 <= novo_y < self.grid:
            self.agent_pos = [novo_x, novo_y]

    def atualizar(self):
        if self.agent_pos == list(self.gold) and not self.ouro_pego:
            self.ouro_pego = True
            self.estado = WIN

        if self.agent_pos == list(self.wumpus) or tuple(self.agent_pos) in self.pits:
            self.morto = True
            self.estado = GAME_OVER

    def loop(self):
        while True:
            self.screen.fill((100, 100, 100))

            if self.estado == TELA_MENU:
                desenhar_texto_centralizado(
                    "Escolha o Tamanho do Mapa", 100, self.screen, big_font
                )
                botao("4x4", 100, 200, 100, 50, self.screen, lambda: self.setar_grid(4))
                botao("6x6", 250, 200, 100, 50, self.screen, lambda: self.setar_grid(6))
                botao("8x8", 400, 200, 100, 50, self.screen, lambda: self.setar_grid(8))

            elif self.estado in [JOGANDO, GAME_OVER, WIN]:
                self.desenhar_grid()

                if not self.ouro_pego:
                    self.desenhar_objeto(self.gold, GOLD, "G")
                self.desenhar_objeto(self.wumpus, RED, "W")
                for pit in self.pits:
                    self.desenhar_objeto(pit, BREEZE, "P")
                self.desenhar_agente()

                percep = (
                    self.get_perceptions()
                    if self.estado == JOGANDO
                    else (
                        ["Você morreu!"]
                        if self.estado == GAME_OVER
                        else ["Você venceu!"]
                    )
                )
                self.desenhar_hud(percep)

                if self.estado == GAME_OVER:
                    desenhar_texto_centralizado(
                        "Você Morreu!",
                        self.height // 2 - 30,
                        self.screen,
                        big_font,
                        RED,
                    )
                    botao(
                        "Reiniciar",
                        self.width // 2 - 60,
                        self.height // 2 + 10,
                        120,
                        40,
                        self.screen,
                        self.resetar_jogo,
                    )
                elif self.estado == WIN:
                    desenhar_texto_centralizado(
                        "Você Pegou o Ouro!",
                        self.height // 2 - 30,
                        self.screen,
                        big_font,
                        GOLD,
                    )
                    botao(
                        "Jogar Novamente",
                        self.width // 2 - 80,
                        self.height // 2 + 10,
                        160,
                        40,
                        self.screen,
                        self.resetar_jogo,
                    )

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.estado == JOGANDO and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.mover_agente(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.mover_agente(1, 0)
                    elif event.key == pygame.K_LEFT:
                        self.mover_agente(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.mover_agente(0, 1)
                    self.atualizar()

    def setar_grid(self, valor):
        self.grid = valor
        self.cell_size = 100
        self.width = self.grid * self.cell_size
        self.height = self.grid * self.cell_size + 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.estado = JOGANDO
        self.reset()

    def resetar_jogo(self):
        self.estado = JOGANDO
        self.reset()


# --- Iniciar o jogo ---
if __name__ == "__main__":
    jogo = JogoWumpus()
    jogo.loop()
