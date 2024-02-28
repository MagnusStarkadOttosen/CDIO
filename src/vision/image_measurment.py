
DPI = 96 #RESOLUTION
def calculate_image_size(image):
    height, width = image.shape[:2]
    print('Image width: ', width)
    print('Image Height:', height)
    return width, height

# def resolution(image):
#     dpi = image.info['dpi'] if 'dpi' in image.info else (72, 72)
#     print(f"The image resolution is: {dpi} DPI")


def convert_px_to_cm(image):
    width_px, height_px = calculate_image_size(image)
    width_in = width_px / DPI
    height_in = height_px / DPI
    width_cm = width_in * 2.54
    height_cm = height_in * 2.54
    print(f'Width in cm: {width_cm}, Height in cm: {height_cm}')
    return width_cm , height_cm

