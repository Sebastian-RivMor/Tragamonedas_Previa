import pygame
import sys
from menu import main_menu
from game import game_screen, load_symbol_images

# Inicializar Pygame
pygame.init()

# Definir tamaño de la pantalla
WIDTH = 800
HEIGHT = 500

# Crear la ventana principal
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego")

# Cargar imágenes de los símbolos
symbol_images = load_symbol_images()

# Bucle principal
def main():
    while True:
        # Pantalla de inicio
        main_menu(screen)
        
        # Pantalla del juego
        game_screen(screen, symbol_images)

# Comenzar la aplicación
if __name__ == "__main__":
    main()
