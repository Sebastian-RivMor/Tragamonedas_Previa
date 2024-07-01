import pygame #Liblería para interfaces de videojuegos
import sys    #Líblería para establecer las imágenes, darle formato a las letras en otros características
import time  #Librería para controlar el tiempo de ejecución
import os   #Librería para trabajar con archivos internos del proyecto
import subprocess   # Librería para interactuar con el entorno del sistema operativo desde un programa de Python.
from logic import girar, simbolo_contar, ganador,simbolo_valor #LLamado de las funciones del archivo logic
# Inicializar Pygame
pygame.init()

pygame.mixer.init()#Inicializar el sonido
#Variables de los sonidos del juego

click_sound = pygame.mixer.Sound(os.path.join('img', 'music', 'sound_click.mp3'))#Sonido de cliqueo
win_sound = pygame.mixer.Sound(os.path.join('img', 'music', 'winner_slot.wav'))#Sonido ganador
lose_sound = pygame.mixer.Sound(os.path.join('img', 'music', 'loser_slot.wav'))#Sonido perdedor
sound_slot = pygame.mixer.Sound(os.path.join('img', 'music', 'sound_slot.wav'))#sonido de giro

# Definir tamaño de la pantalla
WIDTH = 960
HEIGHT = 540

# Definir la fuente
font = pygame.font.SysFont(None, 30)

# Definir símbolos del slot machine Interfaz

SYMBOLS = [
'symbol_3bar', 'symbol_bar', 'symbol_bell', 'symbol_cherry',
'symbol_grape', 'symbol_seven', 'symbol_watermelon'
]

# Definir posiciones iniciales de los rieles
#Posición horizontal
REEL_X_POSITIONS = [310, 474, 634]
#Velocidad por la cual gira los carretes
REEL_SPEEDS = [35, 50, 40]

# Tamaño del área donde se muestran los símbolos
SLOT_AREA = pygame.Rect(244, 173, 455, 99)#Horizontal, vertical, padding o relleno de arriba y abajo, espacio de entre carretes

#Icono y titulo
pygame.display.set_caption("UPN")
icono = pygame.image.load("img/UPN.png")
pygame.display.set_icon(icono)

# Función para cargar las imágenes de los símbolos y redimensionarlas
def load_symbol_images():
    #Direccionario de las imágenes con sus respectivos símbolos y dimensiones
    symbol_images = {}
    for symbol in SYMBOLS:
        image = pygame.image.load(os.path.join('img', 'symbolos', f'{symbol}.png'))#Busca la imagen y carga de la imagen mediante el nombre
        image = pygame.transform.scale(image, (75, 75))  # Redimensionar las imágenes de los símbolos
        symbol_images[symbol] = image# Se añade al símbolo su respectiva imagen cargada al diccionario symbol_imagenes
    return symbol_images

# Función para dar aspecto difuminado los casilleros donde van los créditos apartir del texto
def draw_text(text, font, color, surface, x, y):
    # Renderizar el texto principal (blanco y con efecto difuminado)
    #texto que está por encima
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

#Variables del juego
reserva = 500  # Cantidad de reserva inicial
perdida = 0
# Pantalla del juego
def game_screen(screen, symbol_images):
#VARIABLES
    clock = pygame.time.Clock()#
    saldo = 0 # monto total =  monto total + ganancia - apuesta
    mont_apost = 0  # monto apostar
    mont_wing = 0   #ganancia
    spinning = False #Ejecuta todo (inicializamos en false)
    reels = [0, 0, 0] #posición inicial de los símbolos de la interfaz desde la primera línea
    spin_start_time = 0 #Se inicializa en 0 hasta dar clic al botón jugar

#ESTABLECIENDO LOS COMPONENTES DEL TRAGAMONEDAS
    # Cargar las tres imágenes de fondo brillo
    brillo_imagen_1 = pygame.image.load(os.path.join('img', 'fondo_brillo_prev.png'))  #Busqueda y carga
    brillo_imagen_1 = pygame.transform.scale(brillo_imagen_1, (127, 240)) # Redimensionar

    brillo_imagen_2 = pygame.image.load(os.path.join('img', 'fondo_brillo_prev.png'))  
    brillo_imagen_2 = pygame.transform.scale(brillo_imagen_2, (127, 240))

    brillo_imagen_3 = pygame.image.load(os.path.join('img', 'fondo_brillo_prev.png'))   
    brillo_imagen_3 = pygame.transform.scale(brillo_imagen_3, (128, 240))
    #Posición de las imágenes de fondo brilla al tragamonedas (X,Y)
    brillo_imagen_1_pos = (246+10, 155)  # Designar la posión para la carga de imagen
    brillo_imagen_2_pos = (410+10, 155)  
    brillo_imagen_3_pos = (570+10, 155)  


    # Cargar las tres imágenes de fondo principal
    background_1 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  #Busqueda y carga
    background_1 = pygame.transform.scale(background_1, (127, 240))# Redimensionar

    background_2 = pygame.image.load(os.path.join('img', 'fond_princ.png'))  
    background_2 = pygame.transform.scale(background_2, (127, 240))

    background_3 = pygame.image.load(os.path.join('img', 'fond_princ.png'))   
    background_3 = pygame.transform.scale(background_3, (128, 240))

    #Posición de las imágenes de fondo principal al tragamonedas (X,Y)
    background_1_pos = (246+10, 155)  # Designar la posión para la carga de imagen
    background_2_pos = (410+10, 155)  
    background_3_pos = (570+10, 155)

    #Búsqueda y Carga de los botones del tragamonedas
    #Botón jugar
    play_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'star.png'))#búsqueda y carga
    play_button_image = pygame.transform.scale(play_button_image, (197, 57))#Redimensionar las imágenes
    play_button_rect = play_button_image.get_rect(topleft=(110, 458))#Posición del botón
    #Botón Mínima Apuesta
    min_bet_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'm_min.png'))
    min_bet_button_image = pygame.transform.scale(min_bet_button_image, (180, 60))
    min_bet_button_rect = min_bet_button_image.get_rect(topleft=(360, 458))
    #Botón Máxima Apuesta
    max_bet_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'm_max.png'))
    max_bet_button_image = pygame.transform.scale(max_bet_button_image, (180, 60))
    max_bet_button_rect = max_bet_button_image.get_rect(topleft=(600, 455))
    #Botón Mostrar tabla
    table_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_table.png'))  
    table_button_image = pygame.transform.scale(table_button_image, (50, 50)) 
    table_button_rect = table_button_image.get_rect(topleft=(WIDTH - 140, 120)) 
    #Bortón Créditos del equipo
    credit_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_credit.png')) 
    credit_button_image = pygame.transform.scale(credit_button_image, (50, 50)) 
    credit_button_rect = credit_button_image.get_rect(topleft=(WIDTH - 140, 330))   
    #Botón recargar
    recharge_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_recarga.png'))
    recharge_button_image = pygame.transform.scale(recharge_button_image, (50, 50)) 
    recharge_button_rect = recharge_button_image.get_rect(topleft=(WIDTH - 140, 260)) 
    #Botones de volumen
    #Imagenes de volumen
    sonido_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_sonido.png')) 
    sonido_button_image = pygame.transform.scale(sonido_button_image, (50, 50)) 
    sonido_button_rect = sonido_button_image.get_rect(topleft=(WIDTH - 140, 190)) 
    #Imagen Muteo del volumen
    mute_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_mute.png')) 
    mute_button_image = pygame.transform.scale(mute_button_image, (50, 50)) 
    mute_button_rect = mute_button_image.get_rect(topleft=(WIDTH - 140, 190)) 
    #Variable volumen
    volumen_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_sonido.png')) 
    volumen_button_image = pygame.transform.scale(sonido_button_image, (50, 50))  
    volumen_button_rect = sonido_button_image.get_rect(topleft=(WIDTH - 140, 190))  


    # Imagen que se superpone sobre los símbolos para darle efecto de sombra
    overlay_image = pygame.image.load(os.path.join('img', 'fondo_sombra_sup.png'))  
    overlay_height = 249
    overlay_image = pygame.transform.scale(overlay_image, (SLOT_AREA.width, overlay_height))

    # Posiciones de los carretes, asegurándose de que estén espaciados uniformemente
    symbol_height = 98  # Altura de cada símbolo, ajustada para asegurar espacio
    num_symbols = len(SYMBOLS) #Cantidad de símbolos
    #MATRIZ 3x7
    #Establece la posición de los símbolos a cada carrete (Establece 7 áreas para los símbolos de cada rueda)
    reel_positions = [[SLOT_AREA.top + i * symbol_height for i in range(num_symbols)] for _ in range(3)]
    # [  [1,2,3,4,5,6,7] , [1,2,3,4,5,6,7] , [1,2,3,4,5,6,7] ]
     #Establecer las imágenes de los casilleros donde van los créditos (cash, total bet y win)
     #CASH
    saldo_border_image = pygame.image.load(os.path.join('img', 'border', 'mont_cant.png')) #Busqueda y carga
    saldo_border_image = pygame.transform.scale(saldo_border_image, (180, 52.9))  #Redimensionar
    saldo_border_rect = saldo_border_image.get_rect(left=5, top=130)  #posición
    # TOTAL APOSTADO
    saldo_border_image_2 = pygame.image.load(os.path.join('img', 'border', 'mont_apostado.png'))
    saldo_border_image_2 = pygame.transform.scale(saldo_border_image_2, (180, 52.9))
    saldo_border_rect_2 = saldo_border_image_2.get_rect(left=5, top=220)
    #MONTO GANADO (WIN)
    saldo_border_image_3 = pygame.image.load(os.path.join('img', 'border', 'mont_ganado.png'))
    saldo_border_image_3 = pygame.transform.scale(saldo_border_image_3, (180, 52.9))
    saldo_border_rect_3 = saldo_border_image_3.get_rect(left=5, top=305)

    # Cargar y reproducir la música de fondo
    try:
        #Música de fondo
        audio_path = os.path.join('img','music', 'audio_fond.wav')#Búsqueda
        print(f"Loading audio from: {audio_path}")
        pygame.mixer.music.load(audio_path)#Carga del audio
        pygame.mixer.music.play(-1)#Estalece un ciclo repetitivo del audio (loop)
    except pygame.error as e:#Si no se ha encontrado el audio
        print(f"Error loading music: {e}")
        return
    
#BUCLE QUE CONTIENE ACCIONES QUE DEBEN REPETIRSE EN EL JUEGO
    while True:
    #EJECUTAR LOS COMPONENETES DEL TRAGAMONEDAS
        #Se ejecuta la pantalla en blanco al comienzo
        screen.fill((255, 255, 255))
    
        # Dibujar la imagen del fondo principal
        background = pygame.image.load(os.path.join('img', 'pose.png'))#carga y búsqueda
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))#Redimensionar
        screen.blit(background, (0, 0))

        # Dibujar la imagen de fondo de los símbolos (Carretes)
        screen.blit(background_1, background_1_pos)#Imagen, posición de la imágen
        screen.blit(background_2, background_2_pos)
        screen.blit(background_3, background_3_pos)

        #Si es Verdadero, Ejecuta todo el proceso lógico
        if not spinning:
            #Matriz 3x7
            #Bucle para establecer las posiciones iniciales de los símbolos de los carretes en la "INTERFAZ"
            for i, reel_position in enumerate(reel_positions):
                for j in range(len(reel_position)):#Itera entre elementos de la fila
                    reel_positions[i][j] = SLOT_AREA.top + j * symbol_height

        #Determinar una combinación Establecer la posición de cada símbolo en cada carrete de la interfaz
        for i, (x_position, speed) in enumerate(zip(REEL_X_POSITIONS, REEL_SPEEDS)):# Se itera 3 veces
            for j in range(len(reel_positions[i])):#Itera 7 veces
                symbol_index = (reels[i] + j) % num_symbols # vincula el reels con SYMBOLS
                #symbol_index = j
                #symbol_index = (j) % num_symbols
                symbol = SYMBOLS[symbol_index]#Obtiene el simbolo
                symbol_image = symbol_images[symbol]#Obtiene la imagen del simbolo

                # Calcular la posición del símbolo
                symbol_y = reel_positions[i][j]
                symbol_rect = symbol_image.get_rect(center=(x_position+10, symbol_y*0.8+55))

                # Renderizar el símbolo solo si está dentro del área visible del carrete
                if SLOT_AREA.top <= symbol_y <= SLOT_AREA.bottom + symbol_height:
                    screen.blit(symbol_image, symbol_rect)

                if spinning:#GIRO DE LSO ELEMENTOS
                    #sound_slot.play()#Ejecuto el sonido del giro
                    reel_positions[i][j] += speed
                    if reel_positions[i][j] > SLOT_AREA.bottom + symbol_height:
                        reel_positions[i][j] = SLOT_AREA.top - symbol_height

        # Dibujar la imagen de fondo del brillo
        #screen.blit(brillo_image, (SLOT_AREA.x, SLOT_AREA.y - 23))  # Ajustar la posición Y aquí
        screen.blit(brillo_imagen_1, brillo_imagen_1_pos)   # Dibujar los bordes de los rieles + tapar simbolos
        screen.blit(brillo_imagen_2, brillo_imagen_2_pos)
        screen.blit(brillo_imagen_3, brillo_imagen_3_pos)
        # Dibujar la imagen de fondo de la sombra
        screen.blit(overlay_image, (SLOT_AREA.x+10, SLOT_AREA.y - 23))  # Ajustar la posición Y aquí

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
         #Se muestra las cantidades apostadas
        if spinning:#Si es verdadero  se muestra el monto
            draw_text(f"${mont_apost}", font, (0, 0, 255), screen, text_x_2, text_y_2 + 5)
        else:#Si no si monto a postado es cero (Valores cuando comienza el juego)
            if mont_apost == 0:
                draw_text(f"$0", font, (0, 0, 255), screen, text_x_2, text_y_2 + 5)
            else:#Te muestra el monto apostado
                draw_text(f"${mont_apost}", font, (0, 0, 255), screen, text_x_2, text_y_2 + 5)

        # Dibujar la imagen de borde de mont_wing
        screen.blit(saldo_border_image_3, saldo_border_rect_3.topleft)
        text_x_3 = saldo_border_rect_3.left + saldo_border_rect_3.width // 2
        text_y_3 = saldo_border_rect_3.top + saldo_border_rect_3.height // 2 - 2
        draw_text(f"${mont_wing}", font, (0, 0, 255), screen, text_x_3, text_y_3 + 5)

        #Dibuja todos los botones (Jugar, monto mínimo, monto máximo, recargar, tabla, credito, volumen)
        screen.blit(min_bet_button_image, min_bet_button_rect.topleft)
        screen.blit(max_bet_button_image, max_bet_button_rect.topleft)
        screen.blit(recharge_button_image, recharge_button_rect.topleft)
        screen.blit(table_button_image, table_button_rect.topleft) 
        screen.blit(credit_button_image, credit_button_rect.topleft)
        screen.blit(volumen_button_image, volumen_button_rect.topleft) 
        # Actualiza la pantalla después de dibujar todos los elementos
        pygame.display.update()

        #Bucle que acciona el tragamonedas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Cierran y terminan el programa si se detecta un evento de salida
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:#Cuando hace clic a jugar comienza a girar el tragamonedas
                if event.button == 1:#cuando se hizo clic al botón jugar
                    if play_button_rect.collidepoint(event.pos) and not spinning:# Condicional si es que le he dado clic al botón jugar y spinning es verdadero
                                                                             #Comienza girar el tragamonedas
                        if mont_apost == 0:
                            print("Monto apostado es cero. No se puede girar.")
                        else: #Si monto apostado no es 0
                            
                            mont_wing = 0 # Inicializamos el monto ganador
                            spinning = True 
                            spin_start_time = time.time()
                            sound_slot.play()
                            click_sound.play() #Activar sonido
                            #Se determina las variables globales
                            global perdida, reserva
                            perdida += mont_apost
                            reserva += mont_apost
                            #Verificación por consola
                            print("")
                            print("============= ANALIZAR RESULTADO =============")
                            print("Monto Apostado: ",mont_apost)
                            #Ejecución del algoritmo aleatorio (Algoritmo de las Vegas)
                            resultado, cambiar_simbolos = girar(3)
                            #Ganancia respecto a la combinación aleatoria
                            ganancia = ganador(resultado, mont_apost, simbolo_valor)
                            #Establecer el monto total
                            monto_total = saldo + ganancia - mont_apost
                            print("Saldo 1:",saldo)
                            #Actualizando el salgo menos el monto apostar
                            saldo = saldo - mont_apost # saldo actual
                            print("Resultado 1: ",resultado)
                            print("Ganancia 1: ",ganancia)
                            print("Perdida: ",perdida)
                            print("Monto total: ",monto_total)
                            print("Reserva 1: ",reserva)
                            print("Saldo 2: ",saldo)
                            print("============= RESULTADO ENTREGADO ============")
                             #Condicional: No obtendrá montos de ganancia mayores a las pérdidas
                             # Y el saldo no debe ser menor a la reserva
                             #Trozo de Algoritmo Aleatorio ======================= Cereza Cereza Cereza
                            if (ganancia > perdida or monto_total > reserva): #El usuario no podrá ganar si cumple una de las 2 condiciones
                                ganancia = 0
                                result = cambiar_simbolos#De vuelve una combinación perdedora 
                            else:
                                result = resultado

                            print("Resultado 2: ",result)        
                            # Se actualiza la reserva
                            reserva = reserva - ganancia
                            #Se añade el resultado de la combinación a las imágenes de los símbolos de la interfaz
                            for i in range(3):#Cereza Cereza Cereza
                                reels[i] = list(simbolo_contar.keys()).index(result[i]) # Cereza Cereza Cereza 3
                                print("reels: ",reels[i])#
                            
                            print("Ganancia 2: ",ganancia)
                            #Actualizar reserva
                            print("Reserva 2: ",reserva)
                            mont_apost = 0 #monto apostado se actualiza a 0
                            
                            if ganancia > 0:
                                print("------------------------------------------------")
                                print(f"Felicidades, has ganado ${ganancia}!")
                            else:
                                print("------------------------------------------------")
                                print("Lo siento, no has ganado esta vez.")
                                
                    #Seleccionar el monto mínimo de apuesta
                    if min_bet_button_rect.collidepoint(event.pos):
                        if saldo >= 2:
                            mont_apost = 2  # Establecer el monto de apuesta a 200
                            click_sound.play()

                    #Seleccionar el monto máximo de apuesta
                    if max_bet_button_rect.collidepoint(event.pos):
                        if saldo >= 10:
                            mont_apost = 10  # Establecer el monto de apuesta a 400
                            click_sound.play()

                    #Seleccionar recargar
                    if recharge_button_rect.collidepoint(event.pos):
                        click_sound.play()
                        saldo = open_recharge_window(saldo)
                    #Seleccionar boton tabla
                    if table_button_rect.collidepoint(event.pos): 
                        click_sound.play() 
                        table = open_table_window() 
                    #Seleccionar el boton créditos
                    if credit_button_rect.collidepoint(event.pos): 
                        click_sound.play() 
                        credit = open_credit_window() 
                    #Algoritmo para desactivar y activar volumen
                    if volumen_button_rect.collidepoint(event.pos) and pygame.mixer.music.get_volume() > 0.0: 
                        click_sound.play() 
                        pygame.mixer.music.set_volume(0.0) 
                        volumen_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_mute.png')) 
                        volumen_button_image = pygame.transform.scale(mute_button_image, (50, 50)) 
                        volumen_button_rect = mute_button_image.get_rect(topleft=(WIDTH - 140, 190)) 
                    elif volumen_button_rect.collidepoint(event.pos) and pygame.mixer.music.get_volume() == 0.0: 
                        click_sound.play() 
                        pygame.mixer.music.set_volume(1.0) 
                        volumen_button_image = pygame.image.load(os.path.join('img', 'buttons_img', 'button_sonido.png')) 
                        volumen_button_image = pygame.transform.scale(sonido_button_image, (50, 50)) 
                        volumen_button_rect = sonido_button_image.get_rect(topleft=(WIDTH - 140, 190)) 
            #visualizar el icono o botón del volumen
            screen.blit(volumen_button_image, volumen_button_rect.topleft)              
        #Bucle para que el tragamonedas gire por lo menos 3 segundos                    
        if spinning and time.time() - spin_start_time >= 3:
            spinning = False
            middle_index = 0 
            print("════════════════════════════════════════════════")
            for i in range(3):
                symbol_index = (reels[i]+ middle_index) % len(SYMBOLS)
                symbol = SYMBOLS[symbol_index]
                print(f"Reel {i+1} middle symbol: {symbol}")
            
            #Si ganancia es mayor a 0 se actualiza monto ganando | sonido ganador
            if ganancia > 0:
                win_sound.play()  # Reproducir sonido de victoria
                mont_wing = ganancia  # Actualizar monto ganado
                
            else: # sonido perdedor
                lose_sound.play()  # Reproducir sonido de pérdida
            saldo = saldo + ganancia # Actualiza saldo con las ganancias
            print("Saldo 3: ",saldo)
            
        #Limita la velocidad de fotogramas a 60 FPS para controlar la velocidad del juego
        clock.tick(60)

#Función para ingresar la recarga
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
#Funcion para acceder a la tabla de pagos
def open_table_window():    #Tabla Pay  
    try:
        # Ejecutar el script 'table.py' con el saldo actual como argumento
        result = subprocess.run([sys.executable, 'table.py'], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar table.py: {e}")
#Funcion para acceder a créditos
def open_credit_window():   # Tabla Creditos  
    try:
        # Ejecutar el script 'credit.py' con el saldo actual como argumento
        result = subprocess.run([sys.executable, 'credit.py'], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar credit.py: {e}")

def main():
    # Establecer el modo de pantalla utilizando las dimensiones WIDTH y HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Establecer el título de la ventana del juego
    pygame.display.set_caption("Slot Machine")
    
    # Cargar las imágenes de los símbolos del juego
    symbol_images = load_symbol_images()
    
    # Llamar a la función game_screen() para comenzar el juego
    game_screen(screen, symbol_images)
#llamamos a la función main
if __name__ == "__main__":
    main()