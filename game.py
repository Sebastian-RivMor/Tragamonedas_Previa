import pygame
import sys
import random
import time
import os
import subprocess
from logic import obtener_simbolo, girar, simbolo_contar, ganador,simbolo_valor
# Inicializar Pygame
pygame.init()

pygame.mixer.init()
click_sound = pygame.mixer.Sound(os.path.join('img', 'music', 'sound_click.mp3'))
click_sound_start = pygame.mixer.Sound(os.path.join('img', 'music', 'sound_slot.wav'))
win_sound = pygame.mixer.Sound(os.path.join('img', 'music', 'winner_slot.wav'))
lose_sound = pygame.mixer.Sound(os.path.join('img', 'music', 'loser_slot.wav'))


# Definir tamaño de la pantalla
WIDTH = 960
HEIGHT = 540

# Definir la fuente
font = pygame.font.SysFont(None, 30)

# Definir símbolos del slot machine

SYMBOLS = [
'symbol_3bar', 'symbol_bar', 'symbol_bell', 'symbol_cherry',
'symbol_grape', 'symbol_seven', 'symbol_watermelon'
]

# Definir posiciones iniciales de los rieles
REEL_X_POSITIONS = [310, 474, 634]
REEL_SPEEDS = [35, 50, 40]

# Tamaño del área donde se muestran los símbolos
SLOT_AREA = pygame.Rect(244, 173, 455, 99)

# Función para cargar las imágenes de los símbolos y redimensionarlas
def load_symbol_images():
    symbol_images = {}
    for symbol in SYMBOLS:
        image = pygame.image.load(os.path.join('img', 'symbolos', f'{symbol}.png'))
        image = pygame.transform.scale(image, (75, 75))  # Redimensionar las imágenes de los símbolos
        symbol_images[symbol] = image
    return symbol_images

# Función para dibujar texto con efectos
def draw_text(text, font, color, surface, x, y):
    # Renderizar el texto principal (blanco y con efecto de desenfoque)
    blurred_text = font.render(text, True, (255, 255, 255))  # Texto en blanco
    blurred_text.set_alpha(200)  # Establecer transparencia (0 a 255)
    blurred_text = blurred_text.convert_alpha()  # Convertir a superficie con canal alfa

    # Calcular el rectángulo del texto principal
    text_rect = blurred_text.get_rect(center=(x + 4, y + 6))

    # Dibujar el texto con efecto de desenfoque
    surface.blit(blurred_text, text_rect)

    # Renderizar el texto con efecto de neon blanco
    neon_color = (255, 255, 255)
    neon_text_obj = font.render(text, True, neon_color)
    neon_text_rect = neon_text_obj.get_rect(center=(x + 5, y + 7))  # Ajuste para efecto hacia abajo y derecha
    surface.blit(neon_text_obj, neon_text_rect)

# Pantalla del juego
def game_screen(screen, symbol_images):
    clock = pygame.time.Clock()
    saldo = 0
    mont_apost = 0  # Inicializar mont_apost en cero
    mont_wing = 0
    spinning = False
    reels = [0, 0, 0]
    spin_start_time = 0

    # Cargar las tres imágenes de fondo
    background_1 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  
    background_1 = pygame.transform.scale(background_1, (127, 240))

    background_2 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  
    background_2 = pygame.transform.scale(background_2, (127, 240))

    background_3 = pygame.image.load(os.path.join('img', 'fond_princ.png'))   
    background_3 = pygame.transform.scale(background_3, (128, 240))

    background_1_pos = (246, 155)  
    background_2_pos = (410, 155)  
    background_3_pos = (570, 155)

    play_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'star.png'))
    play_button_image = pygame.transform.scale(play_button_image, (197, 57))
    play_button_rect = play_button_image.get_rect(topleft=(110, 458))

    min_bet_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'm_min.png'))
    min_bet_button_image = pygame.transform.scale(min_bet_button_image, (180, 60))
    min_bet_button_rect = min_bet_button_image.get_rect(topleft=(360, 458))

    max_bet_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'm_max.png'))
    max_bet_button_image = pygame.transform.scale(max_bet_button_image, (180, 60))
    max_bet_button_rect = max_bet_button_image.get_rect(topleft=(600, 455))

    recharge_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_recarga.png'))
    recharge_button_image = pygame.transform.scale(recharge_button_image, (150, 40))
    recharge_button_rect = recharge_button_image.get_rect(topleft=(WIDTH - 180, 50))

    # Imagen que se superpone sobre los símbolos
    overlay_image = pygame.image.load(os.path.join('img', 'fondo_sombra_sup.png'))  
    overlay_height = 249
    overlay_image = pygame.transform.scale(overlay_image, (SLOT_AREA.width, overlay_height))

    # Posiciones iniciales de los rieles, asegurándose de que estén espaciados uniformemente
    symbol_height = 98  # Altura de cada símbolo, ajustada para asegurar espacio
    num_symbols = len(SYMBOLS)
    reel_positions = [[SLOT_AREA.top + i * symbol_height for i in range(num_symbols)] for _ in range(3)]

    saldo_border_image = pygame.image.load(os.path.join('img', 'border', 'mont_cant.png'))
    saldo_border_image = pygame.transform.scale(saldo_border_image, (180, 52.9))  
    saldo_border_rect = saldo_border_image.get_rect(left=5, top=130)  

    saldo_border_image_2 = pygame.image.load(os.path.join('img', 'border', 'mont_apostado.png'))
    saldo_border_image_2 = pygame.transform.scale(saldo_border_image_2, (180, 52.9))
    saldo_border_rect_2 = saldo_border_image_2.get_rect(left=5, top=220)

    saldo_border_image_3 = pygame.image.load(os.path.join('img', 'border', 'mont_ganado.png'))
    saldo_border_image_3 = pygame.transform.scale(saldo_border_image_3, (180, 52.9))
    saldo_border_rect_3 = saldo_border_image_3.get_rect(left=5, top=305)

    # Cargar y reproducir la música de fondo
    try:
        audio_path = os.path.join('img','music', 'audio_fond.wav')
        print(f"Loading audio from: {audio_path}")
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error loading music: {e}")
        return

    while True:
        screen.fill((255, 255, 255))

        # Dibujar la imagen del fondo principal
        background = pygame.image.load(os.path.join('img', 'pose.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Dibujar la imagen de fondo del brillo
        brillo_image = pygame.image.load(os.path.join('img', 'fondo_brillo_prev.png'))
        overlay_height = 246
        brillo_image = pygame.transform.scale(brillo_image, (SLOT_AREA.width, overlay_height))
        screen.blit(brillo_image, (SLOT_AREA.x, SLOT_AREA.y - 20))  # Ajustar la posición Y aquí

        # Dibujar la imagen de fondo de los símbolos
        screen.blit(background_1, background_1_pos)
        screen.blit(background_2, background_2_pos)
        screen.blit(background_3, background_3_pos)

        if not spinning:
            for i, reel_position in enumerate(reel_positions):
                for j in range(len(reel_position)):
                    reel_positions[i][j] = SLOT_AREA.top + j * symbol_height

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
        screen.blit(brillo_image, (SLOT_AREA.x, SLOT_AREA.y - 23))  # Ajustar la posición Y aquí

        # Dibujar la imagen de fondo de la sombra
        screen.blit(overlay_image, (SLOT_AREA.x, SLOT_AREA.y - 23))  # Ajustar la posición Y aquí

        screen.blit(play_button_image, play_button_rect.topleft)

        # Dibujar la imagen de borde del saldo
        screen.blit(saldo_border_image, saldo_border_rect.topleft)
        text_x = saldo_border_rect.left + saldo_border_rect.width // 2
        text_y = saldo_border_rect.top + saldo_border_rect.height // 2 - 2
        draw_text(f"${saldo}", font, (0, 0, 255), screen, text_x, text_y + 5)

        # Dibujar la imagen de borde de mont_apost
        screen.blit(saldo_border_image_2, saldo_border_rect_2.topleft)
        text_x_2 = saldo_border_rect_2.left + saldo_border_rect_2.width // 2
        text_y_2 = saldo_border_rect_2.top + saldo_border_rect_2.height // 2 - 2

        if spinning:
            draw_text(f"${mont_apost}", font, (0, 0, 255), screen, text_x_2, text_y_2 + 5)
        else:
            if mont_apost == 0:
                draw_text(f"$0", font, (0, 0, 255), screen, text_x_2, text_y_2 + 5)
            else:
                draw_text(f"${mont_apost}", font, (0, 0, 255), screen, text_x_2, text_y_2 + 5)

        # Dibujar la imagen de borde de mont_wing
        screen.blit(saldo_border_image_3, saldo_border_rect_3.topleft)
        text_x_3 = saldo_border_rect_3.left + saldo_border_rect_3.width // 2
        text_y_3 = saldo_border_rect_3.top + saldo_border_rect_3.height // 2 - 2
        draw_text(f"${mont_wing}", font, (0, 0, 255), screen, text_x_3, text_y_3 + 5)

        screen.blit(min_bet_button_image, min_bet_button_rect.topleft)
        screen.blit(max_bet_button_image, max_bet_button_rect.topleft)
        screen.blit(recharge_button_image, recharge_button_rect.topleft)

        # Actualiza la pantalla después de dibujar todos los elementos
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button_rect.collidepoint(event.pos) and not spinning:
                        if mont_apost == 0:
                            print("Monto apostado es cero. No se puede girar.")
                        else:
                            spinning = True
                            spin_start_time = time.time()
                            click_sound.play()
                            resultado, cambiar_simbolos = girar(3)
                            for i in range(3):
                                reels[i] = list(simbolo_contar.keys()).index(resultado[i])
                                ganancia = ganador(resultado, mont_apost, simbolo_valor)
                            
                            if ganancia > 0:
                                print("------------------------------------------------")
                                print(f"Felicidades, has ganado ${ganancia}!")
                                saldo += ganancia
                                mont_wing += ganancia  # Actualizar monto ganado
                                if not pagar_jugador(ganancia):
                                    print("No hay suficiente dinero en la reserva para pagar al jugador.")
                            else:
                                print("------------------------------------------------")
                                print("Lo siento, no has ganado esta vez.")
                                agregar_a_reserva(mont_apost)  # Agregar el monto apostado a la reserva
                                
                            mont_apost = 0

                    if min_bet_button_rect.collidepoint(event.pos):
                        if saldo >= 200:
                            saldo -= 200
                            mont_apost = 200  # Establecer el monto de apuesta a 200
                            click_sound.play()
                    if max_bet_button_rect.collidepoint(event.pos):
                        if saldo >= 400:
                            saldo -= 400
                            mont_apost = 400  # Establecer el monto de apuesta a 400
                            click_sound.play()

                    if recharge_button_rect.collidepoint(event.pos):
                        click_sound.play()
                        saldo = open_recharge_window(saldo)
                            
        if spinning and time.time() - spin_start_time >= 3:
            spinning = False
            middle_index = 1  # Suponiendo que el símbolo central es el segundo en la lista de posiciones
            for i in range(3):
                symbol_index = (reels[i] + middle_index) % len(SYMBOLS)
                symbol = SYMBOLS[symbol_index]
                print(f"Reel {i+1} middle symbol: {symbol}")

            # Calcular ganancias o pérdidas utilizando la función ganador
            resultado_linea = [SYMBOLS[reels[i]] for i in range(3)]
            ganancia = ganador(resultado_linea, mont_apost, simbolo_valor)  # Suponiendo que 'valores' está definido
            
            if ganancia > 0:
                print(f"Has ganado ${ganancia}!")
                saldo += ganancia
                mont_wing += ganancia  # Actualizar monto ganado
                if not pagar_jugador(ganancia):
                    print("No hay suficiente dinero en la reserva para pagar al jugador.")
                win_sound.play()  # Reproducir sonido de victoria
            else:
                print("No has ganado esta vez.")
                agregar_a_reserva(mont_apost)  # Agregar el monto apostado a la reserva
                lose_sound.play()  # Reproducir sonido de pérdida
            print(f"Cantidad en reserva: {obtener_reserva()}")
            mont_apost = 0

        # Limita la velocidad de fotogramas a 60 FPS para controlar la velocidad del juego
        clock.tick(60)

reserva = 5000  # Cantidad de reserva inicial

# Función para realizar un pago a un jugador
def pagar_jugador(monto):
    global reserva
    if reserva >= monto:
        reserva -= monto
        return True
    else:
        return False  # No hay suficiente dinero en la reserva para pagar al jugador

# Función para agregar dinero a la reserva cuando el jugador pierde
def agregar_a_reserva(monto):
    global reserva
    reserva += monto

# Función para obtener la cantidad actual de la reserva (para propósitos de consola)
def obtener_reserva():
    return reserva

def open_recharge_window(current_saldo):
    try:
        # Ejecutar el script 'recharge.py' con el saldo actual como argumento
        result = subprocess.run([sys.executable, 'recharge.py', str(current_saldo)], capture_output=True, text=True, check=True)

        # Obtener la última línea de la salida que contiene el nuevo saldo y elimina espacios en blanco adicionales
        new_saldo_line = result.stdout.strip().splitlines()[-1]
        
        # Filtra y convierte los dígitos de la línea en un entero new_saldo
        new_saldo = int(''.join(filter(str.isdigit, new_saldo_line)))
        
        return new_saldo
    
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar recharge.py: {e}")
        
    except (ValueError, IndexError) as e:
        print(f"Error al procesar nuevo saldo: {e}")
    return current_saldo

def main():
    # Establecer el modo de pantalla utilizando las dimensiones WIDTH y HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Establecer el título de la ventana del juego
    pygame.display.set_caption("Slot Machine")
    
    # Cargar las imágenes de los símbolos del juego
    symbol_images = load_symbol_images()
    
    # Llamar a la función game_screen() para comenzar el juego
    game_screen(screen, symbol_images)

if __name__ == "__main__":
    main()