import pygame as pg
from random import randrange

# Configuración de la ventana del juego

window = 500  # Tamaño de la ventana
titlesize = 25  # Tamaño de cada tile (ancho/alto de la serpente)

# Se calcula el rango de manera que los objetos queden dentro de los límites de la ventana
rango = (titlesize // 2, window - titlesize // 2) 
# Función lambda para obtener una posición aleatoria dentro del rango
getrandomposition = lambda: [randrange(*rango), randrange(*rango)]

# Creación del rectángulo que representa la serpiente
# pg.Rect([x, y, width, height]) define el rectángulo con posición y tamaño
# Rectángulo de la serpiente (2 píxeles menos para dar borde)
serpiente = pg.Rect([0, 0, titlesize - 2, titlesize - 2])  

# Colocamos la serpiente en una posición aleatoria
serpientecentro = getrandomposition()

# Longitud inicial de la serpiente (un tile pq empieza chikita)
length = 1

# Lista para almacenar los tiles de la serpiente
segmentos = [serpiente.copy()]

# Configuración de la ventana de visualización de Pygame
screen = pg.display.set_mode([window] * 2)

# Reloj para controlar la velocidad de actualización de los cuadros
clock = pg.time.Clock()

background = pg.image.load(r"C:\Users\Ebbony G\OneDrive\Documentos\Palmore\Programacion 2\Parcial 2\Snake\rosa.jpg").convert()
snaki = pg.image.load(r"C:\Users\Ebbony G\OneDrive\Documentos\Palmore\Programacion 2\Parcial 2\Snake\snaki.png").convert_alpha()
# Bucle principal del juego
while True:
    # Revisión de los eventos, como el cierre de la ventana
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()  
    
    mopos = pg.mouse.get_pos()
    x = mopos[0]
    y = mopos [1]

    # Rellenar la pantalla con color negro en cada iteración
    screen.blit(background, [0, 0])
    screen.blit(snaki,[0,0])
    #snake
    [pg.draw.rect(screen, 'green', segmentos) for segmentos in segmentos]
    # Actualizar la pantalla 
    pg.display.flip()
    
    # Controlar la velocidad del bucle de juego para que corra a 60 fps
    clock.tick(60)
