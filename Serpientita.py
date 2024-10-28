import pygame as pg
from random import randrange
from pygame.locals import *

# Configuración de la ventana
window = 500  
titlesize = 25  

# Función para obtener una posición aleatoria dentro de los límites de la ventana
getrandomposition = lambda: [
    randrange(0, window // titlesize) * titlesize, 
    randrange(0, window // titlesize) * titlesize
]

def restart_game():
    """Reinicia el juego, restableciendo las variables del estado del juego."""
    global serpente, length, segmentos, sepentedir, comia, comia_count, game_over
    serpente = pg.Rect([0, 0, titlesize, titlesize])  
    serpente.topleft = getrandomposition()  

    length = 1
    segmentos = [serpente.copy()]  # Almacena la posición inicial de la serpiente

    sepentedir = (0, 0)  # Dirección inicial de la serpiente

    comia.topleft = getrandomposition()  # Reubica la comida

    comia_count = 0  # Reinicia el contador de comida
    return False  

# Inicialización de la serpiente y otros parámetros
serpente = pg.Rect([0, 0, titlesize, titlesize])  
serpente.topleft = getrandomposition()  

length = 1
segmentos = [serpente.copy()]

sepentedir = (0, 0)  # Dirección inicial de la serpiente

# Configuración de tiempo
time, timestep = 0, 150

# Carga y escalado de la imagen de la comida
comida_img = pg.image.load(r'C:\Users\Ebbony G\OneDrive\Documentos\Palmore\Programacion 2\Parcial 2\Snake\comia.png')
comida_img = pg.transform.scale(comida_img, (titlesize, titlesize))  

# Inicialización de la comida
comia = pg.Rect([0, 0, titlesize, titlesize])  
comia.topleft = getrandomposition()

comia_count = 0  # Contador de comida

paused = False  # Estado de pausa

# Configuración de la pantalla y el reloj
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()

# Configuración de las direcciones permitidas
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Inicialización de la fuente
pg.font.init()
font = pg.font.Font(None, 36)

game_over = False  # Estado del juego

while True:
    # Dibuja el fondo de la cuadrícula
    for y in range(0, window, titlesize):
        for x in range(0, window, titlesize):
            color = '#f9d0d6' if (x // titlesize + y // titlesize) % 2 == 0 else '#faf0f8'
            pg.draw.rect(screen, color, (x, y, titlesize, titlesize))

    # Manejo de eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()  # Salir del juego al cerrar la ventana
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                paused = not paused  # Cambiar estado de pausa
            
            if event.key == pg.K_RETURN and game_over:  
                game_over = restart_game()  # Reiniciar el juego si está en estado de "game over"

            # Manejo de la dirección de la serpiente
            if not paused and not game_over:  
                if event.key == pg.K_w and dirs[pg.K_w]:
                    sepentedir = (0, -titlesize)  # Mover hacia arriba
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_s and dirs[pg.K_s]:
                    sepentedir = (0, titlesize)  # Mover hacia abajo
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    sepentedir = (-titlesize, 0)  # Mover hacia la izquierda
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    sepentedir = (titlesize, 0)  # Mover hacia la derecha
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    # Verificar colisiones y límites
    serpentecomiamisma = pg.Rect.collidelist(serpente, segmentos[:-1]) != -1
    if serpente.left < 0 or serpente.right > window or serpente.top < 0 or serpente.bottom > window or serpentecomiamisma:
        game_over = True  # Cambiar a estado de "game over"

    # Asegurar que la comida no aparezca sobre la serpiente
    while pg.Rect.collidelist(comia, segmentos[:-1]) != -1:
        comia.topleft = getrandomposition()  

    # Comprobar si la serpiente come la comida
    if serpente.topleft == comia.topleft:
        comia.topleft = getrandomposition()  # Reubicar la comida
        length += 1  # Aumentar la longitud de la serpiente
        comia_count += 1  # Aumentar el contador de comida

    # Dibujar la comida
    screen.blit(comida_img, comia.topleft)  

    # Dibujar la serpiente
    for segmento in segmentos:
        pg.draw.rect(screen, '#577655', segmento)

    # Mostrar la puntuación
    puntuaciontxt = font.render(f'Puntos: {comia_count}', True, (0, 0, 0))  
    screen.blit(puntuaciontxt, (10, 10))

    # Lógica de movimiento y actualización de la serpiente
    if not paused and not game_over:  
        timenow = pg.time.get_ticks()
        if timenow - time > timestep:
            time = timenow
            serpente.move_ip(sepentedir)  # Mover la serpiente
            segmentos.append(serpente.copy())  # Agregar nueva posición
            segmentos = segmentos[-length:]  # Mantener el tamaño de la serpiente

    else:
        # Mostrar mensajes de pausa o "game over"
        if paused:
            pause_text = font.render('Pausa', True, (0, 0, 0))  
            text_rect = pause_text.get_rect(bottomright=(window - 10, window - 10))  
            screen.blit(pause_text, text_rect)
        elif game_over:  
            game_over_text1 = font.render('HAS PERDIDO', True, (0, 0, 0))  
            sad_face_text = font.render(':(', True, (0, 0, 0))  
            instruction_text = font.render('Presiona Enter para reiniciar', True, (0, 0, 0))  

            # Centrar los textos en la pantalla
            text_rect1 = game_over_text1.get_rect(center=(window // 2, window // 2 - 30))
            sad_face_rect = sad_face_text.get_rect(center=(window // 2, window // 2))
            instruction_rect = instruction_text.get_rect(center=(window // 2, window // 2 + 30))

            # Dibujar los textos en la pantalla
            screen.blit(game_over_text1, text_rect1)
            screen.blit(sad_face_text, sad_face_rect)
            screen.blit(instruction_text, instruction_rect)

    pg.display.flip()  # Actualizar la pantalla
    clock.tick(30)  # Limitar a 30 FPS
