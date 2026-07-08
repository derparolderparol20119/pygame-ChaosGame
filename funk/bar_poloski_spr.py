import pygame


def draw_value_bar( screen, x, y, width, height, value, niz_porog, verh_porog ):
    if verh_porog == niz_porog:
        verh_porog += 1
    t = (value - niz_porog) / (verh_porog - niz_porog)
    t = max(0.0, min(1.0, t))

    if t < 0.5:
        k = t / 0.5
        r = 255
        g = int(255 * k)
        b = 0

    else:
        k = (t - 0.5) / 0.5
        r = int(255 * (1 - k))
        g = 255
        b = 0

    color = (r, g, b)

    pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height))

    pygame.draw.rect(screen,color,(x, y, int(width * t), height))

    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)


def draw_value_bar_vertical(screen, x, y, width, height, value, niz_porog, verh_porog , blue = None ):
    if verh_porog == niz_porog:
        verh_porog += 1

    t = (value - niz_porog) / (verh_porog - niz_porog)
    t = max(0.0, min(1.0, t))

    # Цвет (тот же градиент: красный → жёлтый → зелёный)
    if t < 0.5:
        k = t / 0.5
        r = 255
        g = int(255 * k)
        b = 0
    else:
        k = (t - 0.5) / 0.5
        r = int(255 * (1 - k))
        g = 255
        b = 0

    if blue != None:
        color = (40, 120, 255)
    else :
        color = (r, g, b)

    # Фон
    pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height))

    # Высота заполнения
    fill_height = int(height * t)

    # Рисуем снизу вверх
    pygame.draw.rect(
        screen,
        color,
        (x, y + height - fill_height, width, fill_height)
    )

    # Рамка
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)