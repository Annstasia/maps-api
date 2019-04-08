import pygame
import requests
import sys
import os


def new_request(spn='1', ll=('100', '65'), l='map'):
        try:
            map_request = "http://static-maps.yandex.ru/1.x/"
            params = {
                'll': ','.join(ll),
                'spn': ','.join([spn, spn]),
                'l': l
            }
            response = requests.get(map_request, params=params)

            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
        except:
            print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)


pygame.init()
new_request()
spn = 1
# Как реализовать перемещение по размру экрана?
ll = [100, 65]
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
            if event.key == 280 and spn > 0.001:

                spn /= 2
                new_request(spn=str(spn), ll=[str(ll[0]), str(ll[1])])
                image = pygame.image.load('map.png')
            if event.key == 281 and spn * 1.5 < 90:
                spn *= 2
                new_request(spn=str(spn), ll=[str(ll[0]), str(ll[1])])
                image = pygame.image.load('map.png')
            # r
            if event.key == 275:
                ll[0] += spn
                if ll[0] >= 180:
                    ll[0] = -360 + ll[0]
                new_request(spn=str(spn), ll=[str(ll[0]), str(ll[1])])
                image = pygame.image.load('map.png')
            if event.key == 276:
                ll[0] -= spn
                if ll[0] <= -180:
                    ll[0] = 360 + ll[0]
                new_request(spn=str(spn), ll=[str(ll[0]), str(ll[1])])
                image = pygame.image.load('map.png')
            if event.key == 273 and ll[1] + spn < 87:
                ll[1] += spn
                new_request(spn=str(spn), ll=[str(ll[0]), str(ll[1])])
                image = pygame.image.load('map.png')
            if event.key == 274 and ll[1] - spn > -87:
                ll[1] -= spn
                new_request(spn=str(spn), ll=[str(ll[0]), str(ll[1])])
                image = pygame.image.load('map.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
os.remove('map.png')