import pygame #Liblería para interfaces de videojuegos
from menu import main_menu
from game import game_screen, load_symbol_images #Llamado de las funciones del archivo game

# Inicializar Pygame
pygame.init()

# Definir tamaño de la pantalla
WIDTH = 960
HEIGHT = 540

# Crear la ventana principal
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRAGAMONEDAS BAR 'LA PREVIA'")

# Cargar imágenes de los símbolos
symbol_images = load_symbol_images()

# Bucle principal
def main():      
    # Pantalla del juego
    game_screen(screen, symbol_images)

# Comenzar la aplicación
if __name__ == "__main__":
    main()
