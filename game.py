import pygame
import sys
import random
import time
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
SYMBOLS = ['symbol_banana', 'symbol_bar', 'symbol_campana', 'symbol_cereza', 'symbol_limon', 'symbol_naranja', 'symbol_sandia', 'symbol_siete', 'symbol_uva']

# Definir posiciones iniciales de los rieles
REEL_X_POSITIONS = [275, 395, 510]

# Velocidades de giro de los rieles
REEL_SPEEDS = [10, 15, 20]  # Velocidades para cada rodillo

# Tamaño del área donde se muestran los símbolos
SLOT_AREA = pygame.Rect(175, 150, 450, 200)

# Función para cargar las imágenes de los símbolos
def load_symbol_images():
    symbol_images = {}
    for symbol in SYMBOLS:
        symbol_images[symbol] = pygame.image.load(f'C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\\symbolos\\{symbol}.png')
    return symbol_images

# Pantalla del juego
def game_screen(screen, symbol_images):
    clock = pygame.time.Clock()
    saldo = 1000
    spinning = False  # Variable para controlar si los rieles están girando
    reels = [0, 0, 0]  # Índices de los símbolos actuales para cada rodillo
    spin_start_time = 0  # Tiempo de inicio del giro

    # área del slot machine
    slot_background = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\slot_fond.jpg')
    slot_background = pygame.transform.scale(slot_background, (SLOT_AREA.width, SLOT_AREA.height))

    # botones
    play_button_image = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\buttons_img\\jugar.png')
    play_button_image = pygame.transform.scale(play_button_image, (140, 100))
    play_button_x = 80  
    play_button_y = 400  
    play_button_rect = play_button_image.get_rect(topleft=(play_button_x, play_button_y))

    min_bet_button_image = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\buttons_img\\min.png')
    min_bet_button_image = pygame.transform.scale(min_bet_button_image, (180, 60))
    min_bet_button_x = 260  
    min_bet_button_y = 420  
    min_bet_button_rect = min_bet_button_image.get_rect(topleft=(min_bet_button_x, min_bet_button_y))

    max_bet_button_image = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\buttons_img\\max.png')
    max_bet_button_image = pygame.transform.scale(max_bet_button_image, (180, 60))
    max_bet_button_x = 500  
    max_bet_button_y = 420  
    max_bet_button_rect = max_bet_button_image.get_rect(topleft=(max_bet_button_x, max_bet_button_y))

    recharge_button_image = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\buttons_img\\recarga.png')
    recharge_button_image = pygame.transform.scale(recharge_button_image, (160, 50))
    recharge_button_x = WIDTH - 180  
    recharge_button_y = 50  
    recharge_button_rect = recharge_button_image.get_rect(topleft=(recharge_button_x, recharge_button_y))

    while True:
        screen.fill(WHITE)

        # Mostrar fondo
        background = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\background_2.png')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Dibujar el área del slot machine con la imagen de fondo
        screen.blit(slot_background, (SLOT_AREA.x, SLOT_AREA.y))

        # Dibujar botones
        screen.blit(play_button_image, play_button_rect.topleft)
        screen.blit(min_bet_button_image, min_bet_button_rect.topleft)
        screen.blit(max_bet_button_image, max_bet_button_rect.topleft)

        # Dibujar saldo y botón de recarga
        draw_text("Saldo: $" + str(saldo), font, BLUE, screen, WIDTH / 2, 100)
        screen.blit(recharge_button_image, recharge_button_rect.topleft)

        # Dibujar el slot machine
        for i, (x_position, speed) in enumerate(zip(REEL_X_POSITIONS, REEL_SPEEDS)):
            symbol_index = reels[i] % len(SYMBOLS)
            symbol = SYMBOLS[symbol_index]
            symbol_image = symbol_images[symbol]
            symbol_rect = symbol_image.get_rect(center=(x_position, SLOT_AREA.centery))
            screen.blit(symbol_image, symbol_rect)

            if spinning:
                reels[i] += speed
                if reels[i] >= len(SYMBOLS) * 100: 
                    reels[i] = 0

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

        if spinning and time.time() - spin_start_time >= 0.5:  
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

# Iniciar el juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slot Machine")
    symbol_images = load_symbol_images()
    game_screen(screen, symbol_images)

if __name__ == "__main__":
    main()
