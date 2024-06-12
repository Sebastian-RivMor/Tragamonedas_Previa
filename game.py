import pygame
import sys
import random
import time
import os
import subprocess

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Definir tamaño de la pantalla
WIDTH = 800
HEIGHT = 500

# Definir la fuente
font = pygame.font.SysFont(None, 48)

# Definir símbolos del slot machine
SYMBOLS = [
    'symbol_banana', 'symbol_bar', 'symbol_campana', 'symbol_cereza',
    'symbol_limon', 'symbol_naranja', 'symbol_sandia', 'symbol_siete', 'symbol_uva'
]

# Definir posiciones iniciales de los rieles
REEL_X_POSITIONS = [275, 395, 510]
REEL_SPEEDS = [10, 15, 20]

# Tamaño del área donde se muestran los símbolos
SLOT_AREA = pygame.Rect(175, 150, 450, 200)

# Función para cargar las imágenes de los símbolos
def load_symbol_images():
    symbol_images = {}
    for symbol in SYMBOLS:
        symbol_images[symbol] = pygame.image.load(os.path.join('img', 'symbolos', f'{symbol}.png'))
    return symbol_images

# Pantalla del juego
def game_screen(screen, symbol_images):
    clock = pygame.time.Clock()
    saldo = 1000
    spinning = False
    reels = [0, 0, 0]
    spin_start_time = 0

    slot_background = pygame.image.load(os.path.join('img', 'slot_fond.jpg'))
    slot_background = pygame.transform.scale(slot_background, (SLOT_AREA.width, SLOT_AREA.height))

    play_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'jugar.png'))
    play_button_image = pygame.transform.scale(play_button_image, (140, 100))
    play_button_rect = play_button_image.get_rect(topleft=(80, 400))

    min_bet_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'min.png'))
    min_bet_button_image = pygame.transform.scale(min_bet_button_image, (180, 60))
    min_bet_button_rect = min_bet_button_image.get_rect(topleft=(260, 420))

    max_bet_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'max.png'))
    max_bet_button_image = pygame.transform.scale(max_bet_button_image, (180, 60))
    max_bet_button_rect = max_bet_button_image.get_rect(topleft=(500, 420))

    recharge_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'recarga.png'))
    recharge_button_image = pygame.transform.scale(recharge_button_image, (160, 50))
    recharge_button_rect = recharge_button_image.get_rect(topleft=(WIDTH - 180, 50))

    # Posiciones iniciales de los rieles, asegurándose de que estén espaciados uniformemente
    reel_positions = [[SLOT_AREA.top + i * (SLOT_AREA.height // len(SYMBOLS)) for i in range(len(SYMBOLS))] for _ in range(3)]

    while True:
        screen.fill(WHITE)

        background = pygame.image.load(os.path.join('img', 'pose.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        screen.blit(slot_background, (SLOT_AREA.x, SLOT_AREA.y))

        screen.blit(play_button_image, play_button_rect.topleft)
        screen.blit(min_bet_button_image, min_bet_button_rect.topleft)
        screen.blit(max_bet_button_image, max_bet_button_rect.topleft)
        draw_text("Monto apostado: $" + str(saldo), font, BLUE, screen, WIDTH / 2, 50)
        screen.blit(recharge_button_image, recharge_button_rect.topleft)

        for i, (x_position, speed) in enumerate(zip(REEL_X_POSITIONS, REEL_SPEEDS)):
            for j in range(len(SYMBOLS)):
                symbol_index = (reels[i] + j) % len(SYMBOLS)
                symbol = SYMBOLS[symbol_index]
                symbol_image = symbol_images[symbol]
                symbol_rect = symbol_image.get_rect(center=(x_position, reel_positions[i][j]))
                if SLOT_AREA.top <= reel_positions[i][j] <= SLOT_AREA.bottom:
                    screen.blit(symbol_image, symbol_rect)

                if spinning:
                    reel_positions[i][j] -= speed
                    if reel_positions[i][j] < SLOT_AREA.top - (SLOT_AREA.height // len(SYMBOLS)):
                        reel_positions[i][j] = SLOT_AREA.bottom + (SLOT_AREA.height // len(SYMBOLS))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button_rect.collidepoint(event.pos):
                        spinning = True
                        spin_start_time = time.time()
                    elif min_bet_button_rect.collidepoint(event.pos):
                        saldo -= 10
                    elif max_bet_button_rect.collidepoint(event.pos):
                        saldo -= 100
                    elif recharge_button_rect.collidepoint(event.pos):
                        saldo = open_recharge_window(saldo)

        if spinning and time.time() - spin_start_time >= 2:
            spinning = False

        clock.tick(60)

def open_recharge_window(current_saldo):
    recharge_process = subprocess.Popen([sys.executable, 'recharge.py', str(current_saldo)], stdout=subprocess.PIPE)
    recharge_process.wait()
    new_saldo = recharge_process.communicate()[0].strip()
    return int(new_saldo)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slot Machine")
    symbol_images = load_symbol_images()
    game_screen(screen, symbol_images)

if __name__ == "__main__":
    main()
