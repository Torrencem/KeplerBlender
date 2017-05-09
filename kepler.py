from math import sin, cos, sqrt, pi, tan, atan, atan2

rmin = 6.783e6
rmax = 9.253e6
bigG = 6.67408e-11
mEarth = 5.972e24
ecc = (rmax - rmin) / (rmax + rmin)

p = 2 / (1 / rmin + 1 / rmax)

a = p / (1 - ecc ** 2)
b = p / sqrt(1 - ecc ** 2)

period = 2 * pi * sqrt(a ** 3 / (bigG * mEarth))

print(period)

def calculateTheta(time):
    meananomaly = (time % period) * (2 * pi) / period

    # Find eccentric anomaly
    eanom = meananomaly

    # Use Newton's Method to approximate
    # the eccentric anomaly
    for it in range(9):
        eanom = meananomaly + ecc * sin(eanom)

    # Now solve for the true anomaly theta
    theta = 2 * atan2(sqrt(1 - ecc) * cos(eanom / 2), sqrt(1 + ecc) * sin(eanom / 2))
    return theta

for t in range(200):
    print(calculateTheta(t * 40))