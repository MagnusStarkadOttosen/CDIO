DPI = 96  # RESOLUTION


def calculate_image_size(image):
    height, width = image.shape[:2]
    print('Image width: ', width)
    print('Image Height:', height)
    return width, height


# def resolution(image):
#     dpi = image.info['dpi'] if 'dpi' in image.info else (72, 72)
#     print(f"The image resolution is: {dpi} DPI")


def convert_px_to_cm(pixel_value):
    return pixel_value / 10


def convert_image_size_to_cm(image):
    width_px, height_px = calculate_image_size(image)
    width_cm, height_cm = convert_px_cm_temp(width_px, height_px)
    print(f'Width in cm: {width_cm}, Height in cm: {height_cm}')
    return width_cm, height_cm


def convert_px_cm_temp(width_px, height_px):
    width_in, height_in = convert_px_to_inches(width_px, height_px)
    return width_in * 2.54, height_in * 2.54


def convert_px_to_inches(width_px, height_px):
    width_in = width_px / DPI
    height_in = height_px / DPI
    return width_in, height_in

