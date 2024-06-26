def read_hsv_values(filename):
    """
    Reads HSV values from a file and returns them as a dictionary.
    Do this:
    orange_hsv_values = read_hsv_values('hsv_presets_orange.txt')

    Parameters
    ----------
    filename : str
        The name of the file containing the HSV values.

    Returns
    -------
    dict
        A dictionary containing the HSV values with keys as 'LowerH', 'LowerS', 'LowerV', 'UpperH', 'UpperS', 'UpperV'.
    """
    hsv_values = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            hsv_values[key] = int(value)
    return hsv_values