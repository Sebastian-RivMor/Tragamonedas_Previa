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
    'symbol_apple', 'symbol_bar', 'symbol_bell', 'symbol_cherry',
    'symbol_limon', 'symbol_grape', 'symbol_orange', 'symbol_seven', 'symbol_watermelon'
]

# Definir posiciones iniciales de los rieles
REEL_X_POSITIONS = [245, 405, 560]
REEL_SPEEDS = [35, 50, 40]

# Tamaño del área donde se muestran los símbolos
SLOT_AREA = pygame.Rect(175, 173, 455, 100)

# Función para cargar las imágenes de los símbolos y redimensionarlas
def load_symbol_images():
    symbol_images = {}
    for symbol in SYMBOLS:
        image = pygame.image.load(os.path.join('img', 'symbolos', f'{symbol}.png'))
        image = pygame.transform.scale(image, (65, 65))  # Redimensionar las imágenes de los símbolos
        symbol_images[symbol] = image
    return symbol_images

# Pantalla del juego
def game_screen(screen, symbol_images):
    clock = pygame.time.Clock()
    saldo = 1000
    spinning = False
    reels = [0, 0, 0]
    spin_start_time = 0

    # Cargar las tres imágenes de fondo
    background_1 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  # Ruta a la primera imagen de fondo
    background_1 = pygame.transform.scale(background_1, (127, 237))

    background_2 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  # Ruta a la segunda imagen de fondo
    background_2 = pygame.transform.scale(background_2, (127, 237))

    background_3 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  # Ruta a la tercera imagen de fondo
    background_3 = pygame.transform.scale(background_3, (128, 237))

    background_1_pos = (177, 155)  
    background_2_pos = (340, 155)  
    background_3_pos = (500, 155)

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

    # Imagen que se superpone sobre los símbolos
    overlay_image = pygame.image.load(os.path.join('img', 'fondo_sombra_sup.png'))  
    overlay_height = 242
    overlay_image = pygame.transform.scale(overlay_image, (SLOT_AREA.width, overlay_height))

    # Posiciones iniciales de los rieles, asegurándose de que estén espaciados uniformemente
    symbol_height = 100  # Altura de cada símbolo, ajustada para asegurar espacio
    num_symbols = len(SYMBOLS)
    reel_positions = [random.randint(0, num_symbols - 1) for _ in range(3)]


    while True:
        screen.fill(WHITE)

        # Dibujar la imagen del fondo principal
        background = pygame.image.load(os.path.join('img', 'pose.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Dibujar la imagen de fondo del brillo
        brillo_image = pygame.image.load(os.path.join('img', 'fondo_brillo_prev.png'))
        overlay_height = 242
        brillo_image = pygame.transform.scale(brillo_image, (SLOT_AREA.width, overlay_height))
        screen.blit(brillo_image, (SLOT_AREA.x, SLOT_AREA.y - 20))  # Ajustar la posición Y aquí

        # Dibujar la imagen de fondo de los símbolos
        screen.blit(background_1, background_1_pos)
        screen.blit(background_2, background_2_pos)
        screen.blit(background_3, background_3_pos)

        if not spinning:
            # Restablecer las posiciones de los símbolos en los rieles
            reel_positions = [[SLOT_AREA.top + i * symbol_height for i in range(num_symbols)] for _ in range(3)]

            # Calcular la posición de la primera fila de símbolos en el centro del área visible
            center_row = SLOT_AREA.top + (SLOT_AREA.height - symbol_height) // 2
            # Ajustar las posiciones de los símbolos en los rieles para mostrar al menos una fila completa en el centro
            for i, reel_position in enumerate(reel_positions):
                # Calcular la posición del centro del carrete
                center_reel_y = center_row - symbol_height * (len(reel_position) // 2)
                # Ajustar la posición de los símbolos para que la fila del centro sea visible
                for j in range(len(reel_position)):
                    reel_positions[i][j] = center_reel_y + j * symbol_height


        for i, (x_position, speed) in enumerate(zip(REEL_X_POSITIONS, REEL_SPEEDS)):
            for j in range(len(reel_positions[i])):
                symbol_index = (reels[i] + j) % num_symbols
                symbol = SYMBOLS[symbol_index]
                symbol_image = symbol_images[symbol]

                # Calcular la posición del símbolo
                symbol_y = reel_positions[i][j]
                symbol_rect = symbol_image.get_rect(center=(x_position, symbol_y))

                # Renderizar el símbolo solo si está dentro del área visible del carrete
                if SLOT_AREA.top <= symbol_y <= SLOT_AREA.bottom + symbol_height:
                    screen.blit(symbol_image, symbol_rect)

                if spinning:
                    reel_positions[i][j] += speed
                    if reel_positions[i][j] > SLOT_AREA.bottom + symbol_height:
                        reel_positions[i][j] = SLOT_AREA.top - symbol_height
        
        # Dibujar la imagen de fondo del brillo
        screen.blit(brillo_image, (SLOT_AREA.x, SLOT_AREA.y - 20))  # Ajustar la posición Y aquí

        # Dibujar la imagen de fondo de la sombra
        screen.blit(overlay_image, (SLOT_AREA.x, SLOT_AREA.y - 20))  # Ajustar la posición Y aquí

        screen.blit(play_button_image, play_button_rect.topleft)
        screen.blit(min_bet_button_image, min_bet_button_rect.topleft)
        screen.blit(max_bet_button_image, max_bet_button_rect.topleft)
        draw_text("Monto apostado: $" + str(saldo), font, BLUE, screen, WIDTH / 2, 50)
        screen.blit(recharge_button_image, recharge_button_rect.topleft)

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
                        # Girar los rodillos al iniciar el giro
                        reels = [random.randint(0, num_symbols - 1) for _ in range(3)]
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
