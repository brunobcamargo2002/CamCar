import pygame
import requests

# URLs
url = "http://192.168.0.10"
line_url = url + "/line"
rotation_url = url + "/rotation"
stop_url = url + "/stop"

# API functions
def go(forward):
    requests.post(line_url, json={"forward": forward})

def rotation(clockwise):
    requests.post(rotation_url, json={"clockwise": clockwise})

def stop():
    requests.post(stop_url, json={})

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Controle do Carrinho")

# Estado para evitar requests duplicados
current_action = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pressionou tecla
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if current_action != 'forward':
                    go(False)
                    current_action = 'forward'
            elif event.key == pygame.K_DOWN:
                if current_action != 'backward':
                    go(True)
                    current_action = 'backward'
            elif event.key == pygame.K_LEFT:
                if current_action != 'rotate_left':
                    rotation(False)
                    current_action = 'rotate_left'
            elif event.key == pygame.K_RIGHT:
                if current_action != 'rotate_right':
                    rotation(True)
                    current_action = 'rotate_right'

        # Soltou tecla
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                stop()
                current_action = None

pygame.quit()
