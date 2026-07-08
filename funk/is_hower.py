import pygame

def is_hover(obj, wx, wy):

    # Старая система
    if hasattr(obj, "xit_boks"):
        print(1)
        return obj.xit_boks.collidepoint(wx, wy)

    # Новая система
    elif hasattr(obj, "is_hover_world"):
        print(2)
        return obj.check_click(wx, wy)

    # fallback
    print(3)
    return False