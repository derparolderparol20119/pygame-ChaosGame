def def_slice_spritesheet(image, frame_width, frame_height):
    frames = []
    sheet_width, sheet_height = image.get_size()
    
    columns = sheet_width // frame_width
    rows = sheet_height // frame_height
    
    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            
            frame = image.subsurface((x, y, frame_width, frame_height))
            frames.append(frame)
    
    return frames