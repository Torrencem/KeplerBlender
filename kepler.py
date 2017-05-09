from math import sin, cos, sqrt, pi, tan, atan, atan2
from PIL import Image, ImageDraw

# rmin = 6.783e6
rmin = 2.783e6
rmax = 9.253e6
bigG = 6.67408e-11
mEarth = 5.972e24
ecc = (rmax - rmin) / (rmax + rmin)

p = 2 / (1 / rmin + 1 / rmax)

a = p / (1 - ecc ** 2)
b = p / sqrt(1 - ecc ** 2)

period = 2 * pi * sqrt(a ** 3 / (bigG * mEarth))

print(period)

def calculateCoords(time):
    meananomaly = (time % period) * (2 * pi) / period

    # Find eccentric anomaly
    eanom = meananomaly

    # Use Newton's Method to approximate
    # the eccentric anomaly
    for it in range(9):
        eanom = meananomaly + ecc * sin(eanom)

    # Now solve for the true anomaly theta
    theta = 2 * atan2(sqrt(1 + ecc) * sin(eanom / 2), sqrt(1 - ecc) * cos(eanom / 2))

    radius = p / (1 + ecc * cos(theta))

    return (radius, theta)

img = Image.new('RGB', (512, 512))

draw = ImageDraw.Draw(img)

def drawRadial(r, theta):
    xypos = [r * cos(theta), r * sin(theta)]
    # Shift it to be in the center
    xypos[0] += 256
    xypos[1] += 256
    coords = [(xypos[0] - 2, xypos[1] - 2), (xypos[0] + 2, xypos[1] + 2)]
    draw.ellipse(coords)

drawRadial(0, 0)

for i in range(78):
    seconds = i * 60
    position = list(calculateCoords(seconds))
    position[0] /= 4e4
    print(position)
    drawRadial(*position)

img.show()