import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Inicializar el mezclador de sonido
pygame.mixer.init()

# Verificar si el archivo de sonido existe
click_sound_path = os.path.join('img', 'music', 'sound_click.mp3')
if os.path.exists(click_sound_path):
    click_sound = pygame.mixer.Sound(click_sound_path)
else:
    print("El archivo de sonido no existe en la ruta especificada:", click_sound_path)
    click_sound = None

# Definir colores
WHITE = (255, 255, 255)

# Definir tamaño de la pantalla
WIDTH = 600
HEIGHT = 400

# Definir la fuente
font = pygame.font.SysFont(None, 48)

# Interacción con el usuario
def recharge_screen(current_saldo):
    # Se crea el formulario 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recargar Saldo")

    # Cargar imagen de fondo
    background = pygame.image.load(os.path.join('img', 'fond_recarga.png'))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Cargar imagen del botón "Aceptar"
    accept_button_image = pygame.image.load(os.path.join('img','buttons_img', 'button_acept.png'))
    accept_button_image = pygame.transform.scale(accept_button_image, (160, 70))

    # Cargar imagen del botón "Cancelar"
    cancel_button_image = pygame.image.load(os.path.join('img','buttons_img', 'button_cancel.png'))
    cancel_button_image = pygame.transform.scale(cancel_button_image, (170, 70))

    # Cargar imagen de fondo para el cuadro de entrada
    input_background = pygame.image.load(os.path.join('img','label' ,'zone_recarga.png'))
    input_background = pygame.transform.scale(input_background, (300, 140))  # Ajustar tamaño según sea necesario

    # Cuadro de entrada para ingresar el crédito/saldo
    txtSaldo = pygame.Rect(150, 150, 300, 50)
    input_background_y_offset = -80  
    active = False
    text = ''

    # Indica si la interfaz se ha terminado
    done = False

    # Inicializa con el saldo actual que se pasa como argumento a la función
    new_saldo = current_saldo

    while not done:
        # Itera sobre todos los eventos generados 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Cierran y terminan el programa si se detecta un evento de salida
                pygame.quit()
                sys.exit()
            
            # Maneja eventos cuando se hace clic 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica si la posición del clic está dentro del txtSaldo
                if txtSaldo.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()  # Reproduce el sonido de clic
                    # Alterna el estado dependiendo de si se hizo clic dentro del cuadro
                    active = not active
                # Detectar clic en el botón "Aceptar"
                elif accept_button_rect.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()  # Reproduce el sonido de clic
                    try: 
                        # El texto ingresado se le suma al saldo actual, actualizando el nuevo saldo
                        new_saldo = current_saldo + int(text)
                        done = True  # Cerrar la ventana al presionar "Aceptar"
                    # Captura errores de conversión 
                    except ValueError:
                        text = ''
                
                # Detectar clic del botón "Cancelar"
                elif cancel_button_rect.collidepoint(event.pos):
                    if click_sound:
                        click_sound.play()  # Reproduce el sonido de clic
                    done = True # Cerrar la ventana al presionar "Cancelar"

            # Manejo de eventos cuando se presiona una tecla
            elif event.type == pygame.KEYDOWN:
                # Verifica si el cuadro de entrada está activo
                if active:
                    # Verifica si se presionó ENTER
                    if event.key == pygame.K_RETURN:
                        try:
                            new_saldo = current_saldo + int(text)
                            # Termina el bucle al presionar ENTER
                            done = True
                        except ValueError:
                            text = ''
                    # Verifica si se presionó la tecla Backspace
                    elif event.key == pygame.K_BACKSPACE:
                        # Elimina el último carácter del texto ingresado
                        text = text[:-1]
                    # Captura todos los demás caracteres ingresados y los agrega al texto
                    else:
                        text += event.unicode

        screen.blit(background, (0, 0))  # Dibujar imagen de fondo

        # Dibujar imagen de fondo del cuadro de entrada
        screen.blit(input_background, (txtSaldo.x, txtSaldo.y + input_background_y_offset))

        txt_surface = font.render(text, True, WHITE)
        # Alinear horizontalmente el texto en el centro del cuadro de entrada
        input_x = txtSaldo.x + (txtSaldo.width - txt_surface.get_width()) // 2
        input_y = txtSaldo.y + (txtSaldo.height - txt_surface.get_height()) // 2
        screen.blit(txt_surface, (input_x, input_y))

        # Dibujar el botón "Aceptar" con la imagen
        accept_button_rect = screen.blit(accept_button_image, (100, 250))
        
        # Dibujar el botón "Cancelar" con la imagen
        cancel_button_rect = screen.blit(cancel_button_image, (350, 250))

        pygame.display.flip()

    return new_saldo

# Renderiza texto en una superficie pygame en la posición especificada
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    # Verifica si se proporcionó al menos un argumento en la línea de comandos
    if len(sys.argv) < 2:
        return
    # Lee el saldo actual desde los argumentos de la línea de comandos
    current_saldo = int(sys.argv[1])
    new_saldo = recharge_screen(current_saldo)
    # Imprime el nuevo saldo
    print(new_saldo)

if __name__ == "__main__":
    main()
