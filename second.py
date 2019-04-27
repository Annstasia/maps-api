import pygame
import requests
import sys
import os
# '37.618865,55.769600'
def new_request(x, y, delta_x, delta_y):
    try:

        map_request = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': '{},{}'.format(x, y),
            'spn': '{},{}'.format(delta_x, delta_y),
            'l': 'map'
        }
        response = requests.get(map_request, params=params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
    except Exception as e:
        print(e)
        sys.exit(1)


pygame.init()
x = 37.618865
y = 55.769600
delta_x = 0.0008
delta_y = 0.0008 * 450 / 600
new_request(x, y, delta_x, delta_y)
screen = pygame.display.set_mode((600, 450))
image = pygame.image.load('map.png')
screen.blit(pygame.image.load('map.png'), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 280 and delta_y > 0.0009:
                delta_x /= 2
                delta_y /= 2
                new_request(x, y, delta_x, delta_y)
                image = pygame.image.load('map.png')
            if event.key == 281 and -180 < x - 2 * delta_x < x + 2 * delta_x < 180 \
                    and -90 < y - 2*delta_y < y + 2 * delta_y < 90:
                delta_x *= 2
                delta_y *= 2
                new_request(x, y, delta_x, delta_y)
                image = pygame.image.load('map.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
os.remove('map.png')