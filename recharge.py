import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Definir tamaño de la pantalla
WIDTH = 600
HEIGHT = 400

# Definir la fuente
font = pygame.font.SysFont(None, 48)

def recharge_screen(current_saldo):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recargar Saldo")

    # Cargar imagen de fondo
    background = pygame.image.load(os.path.join('img', 'fon_recharge.jpg'))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    input_box = pygame.Rect(150, 150, 300, 50)
    active = False
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    done = False
    new_saldo = current_saldo

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            new_saldo = current_saldo + int(text)
                            done = True
                        except ValueError:
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    if accept_button_rect.collidepoint(event.pos):
                        try:
                            new_saldo = current_saldo + int(text)
                        except ValueError:
                            new_saldo = current_saldo
                        done = True
                    elif cancel_button_rect.collidepoint(event.pos):
                        done = True
                        new_saldo = current_saldo

        screen.blit(background, (0, 0))  # Dibujar imagen de fondo

        pygame.draw.rect(screen, color, input_box, 2)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        accept_button_rect = pygame.draw.rect(screen, GREEN, (150, 250, 100, 50))
        draw_text("Aceptar", font, WHITE, screen, 200, 275)
        cancel_button_rect = pygame.draw.rect(screen, RED, (350, 250, 100, 50))
        draw_text("Cancelar", font, WHITE, screen, 400, 275)

        pygame.display.flip()

    return new_saldo

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    saldo = int(sys.argv[1])
    new_saldo = recharge_screen(saldo)
    print(new_saldo)

if __name__ == "__main__":
    main()
