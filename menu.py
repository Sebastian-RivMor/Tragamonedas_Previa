import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HOVER_LIME_GREEN = (34, 139, 34)

# Definir tamaño de la pantalla
WIDTH = 800
HEIGHT = 500

# Definir la fuente
font = pygame.font.SysFont(None, 48)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Pantalla de inicio
def main_menu(screen):
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        
        # Cargar imagen de fondo y redimensionarla
        background = pygame.image.load('C:\\Users\\usuario\\Desktop\\Proyect_Final\\Proyect_final\\img\\BIENVENIDO.png')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        # Posición del botón (ajustar aquí)
        button_x = WIDTH / 3.4
        button_y = HEIGHT * 2 / 2.5

        # Obtener la posición del ratón
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Determinar si el ratón está sobre el botón
        if button_x - 100 <= mouse_x <= button_x + 100 and button_y - 25 <= mouse_y <= button_y + 25:
            button_color = HOVER_LIME_GREEN
        else:
            button_color = BLUE

        # Dibujar botón de iniciar
        pygame.draw.rect(screen, button_color, (button_x - 100, button_y - 25, 200, 50))
        draw_text("Iniciar", font, WHITE, screen, button_x, button_y)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_x - 100 <= event.pos[0] <= button_x + 100 and button_y - 25 <= event.pos[1] <= button_y + 25:
                    return  # Salir del bucle y comenzar el juego

        clock.tick(60)

# Crear la pantalla principal
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_menu(screen)
