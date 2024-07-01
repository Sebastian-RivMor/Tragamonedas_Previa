import pygame #Liblería para interfaces de videojuegos
import sys #Líblería para establecer las imágenes, darle formato a las letras en otros características
import os #Librería para trabajar con archivos internos del proyecto

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
WIDTH = 960
HEIGHT = 540

# Definir la fuente
font = pygame.font.SysFont(None, 48)

#Icono y titulo
pygame.display.set_caption("UPN")
icono = pygame.image.load("img/UPN.png")
pygame.display.set_icon(icono)

# Interacción con el usuario
def credit_screen():
    # Se crea el formulario 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Creditos")

    # Cargar imagen de fondo
    background = pygame.image.load(os.path.join('img', 'fond_credit.png'))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Indica si la interfaz se ha terminado
    done = False

    while not done:
        # Itera sobre todos los eventos generados 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Cierran y terminan el programa si se detecta un evento de salida
                pygame.quit()
                sys.exit()
            
        screen.blit(background, (0, 0))  # Dibujar imagen de fondo

        pygame.display.flip()
        

#Llamamos la función credit_screen
if __name__ == "__main__":
    credit_screen()
