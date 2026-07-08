

def pos_percent(screen_w, screen_h, px, py , padding_x=0, padding_y=0 ):
    """
    px, py — проценты от 0.0 до 1.0
    """
    x = int(screen_w * px) + padding_x
    y = int(screen_h * py) + padding_y
    return x, y