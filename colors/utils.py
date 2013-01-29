
import random

def random_color():
    '''Return a random 6 digit hex color'''

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = ''.join('%02x' % c for c in (r, g, b))

    return color
