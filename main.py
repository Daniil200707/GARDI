import pygame
import requests
import time

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# Цвета
red = (255, 0, 0)
green = (0, 255, 0)

# Карта дома и огорода
garden_map = [[0]*10 for _ in range(10)]  # 10x10 сетка, 0 - свободное место, 1 - место, где требуется работа

# Пример функции для получения погоды
def get_weather():
    API_KEY = "15c8a373e52a7fbc7659f9b458324c32"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=kiev&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data["main"]["temp"], weather_data["main"]["humidity"]

# Оповещение через сирену
pygame.mixer.init()
siren_sound = pygame.mixer.Sound("assets/medical-monitor-153306.mp3")  # Путь к файлу сирены

def trigger_siren():
    siren_sound.play()

# Функция для отрисовки карты
def draw_map():
    for y in range(10):
        for x in range(10):
            color = red if garden_map[y][x] == 1 else green
            pygame.draw.rect(screen, color, (x*60, y*60, 60, 60))

# Главный цикл
running = True
while running:
    screen.fill((255, 255, 255))  # Заполнение экрана белым цветом
    draw_map()  # Отрисовка карты

    # Получаем данные о погоде
    temp, humidity = get_weather()
    print(f"Температура: {temp}°C, Влажность: {humidity}%")

    # Пример проверки, если требуется вмешательство (погода слишком жаркая или сухая)
    if temp > 30 or humidity < 30 or temp < 10:
        garden_map[5][5] = 1  # Например, требуемое внимание в центре карты
        trigger_siren()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

