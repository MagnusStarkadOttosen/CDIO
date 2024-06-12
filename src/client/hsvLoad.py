# Do this in main loop
# orange_hsv_values = read_hsv_values('hsv_presets_orange.txt')

def read_hsv_values(filename):
    hsv_values = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            hsv_values[key] = int(value)
    return hsv_values