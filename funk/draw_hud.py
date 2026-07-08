def draw_hud(font, fps , screen):
    txt = font.render(f"FPS: {fps}  SCALE:", True, (255,255,255))
    screen.blit(txt, (10,10))