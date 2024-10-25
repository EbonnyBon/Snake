import pygame as pg
from random import randrange
from pygame.locals import *

# Configuración de la ventana del juego
window = 500  # Tamaño de la ventana
titlesize = 25  # Tamaño de cada tile (ancho/alto de la serpiente)

# Se ajusta el rango para que las posiciones sean múltiplos del tamaño del tile
getrandomposition = lambda: [randrange(0, window, titlesize), randrange(0, window, titlesize)]

# Creación del rectángulo que representa la serpiente
serpente = pg.Rect([0, 0, titlesize - 2, titlesize - 2])  
serpente.center = getrandomposition()  # Colocar en una posición aleatoria

# Longitud inicial de la serpiente
length = 1
# Lista para almacenar los tiles de la serpiente
segmentos = [serpente.copy()]

# Dirección de movimiento inicial
sepentedir = (0, 0)

# Tiempo y pasos de tiempo
time, timestep = 0, 220
# Crear la comida en una posición aleatoria
comia = serpente.copy()
comia.center = getrandomposition()

# Configuración de la ventana de visualización de Pygame
screen = pg.display.set_mode([window] * 2)
# Reloj para controlar la velocidad de actualización de los cuadros
clock = pg.time.Clock()

# Bucle principal del juego
while True:
    # Revisión de los eventos, como el cierre de la ventana
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()  
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                sepentedir = (0, -titlesize)
            if event.key == pg.K_s:
                sepentedir = (0, titlesize)
            if event.key == pg.K_a:
                sepentedir = (-titlesize, 0)
            if event.key == pg.K_d:
                sepentedir = (titlesize, 0)

    # Rellenar la pantalla con color negro en cada iteración
    screen.fill('black')
    serpentecomiamisma = pg.Rect.collidelist(serpente, segmentos[:-1]) !=-1
    if serpente.left < 0 or serpente.right > window or serpente.top < 0 or serpente.bottom > window or serpentecomiamisma:
        serpente.center, comia.center = getrandomposition(),getrandomposition()
        length, sepentedir = 1, (0,0)
        segmentos = [serpente.copy()]

    if serpente.center == comia.center:
        comia.center = getrandomposition()
        length += 1

    # Dibujar la comida
    pg.draw.rect(screen, 'red', comia)

    # Dibuja la serpiente (segmentos)
    [pg.draw.rect(screen, 'green', segmento) for segmento in segmentos]

    # Mover la serpiente
    timenow = pg.time.get_ticks()
    if timenow - time > timestep:
        time = timenow
        serpente.move_ip(sepentedir)
        segmentos.append(serpente.copy())
        segmentos = segmentos[-length:]

    # Actualizar la pantalla 
    pg.display.flip()
    
    # Controlar la velocidad del bucle de juego para que corra a 60 fps
    clock.tick(60)
