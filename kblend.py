# This example assumes we have a mesh object selected

import bpy
import bmesh
from math import sin, cos, sqrt, pi, atan2

# Get the active mesh
me = bpy.context.object.data


# Get a BMesh representation
bm = bmesh.new()   # create an empty BMesh
bm.from_mesh(me)   # fill it in from a Mesh


#v1 = bm.verts.new((2.0, 2.0, 2.0))
#v2 = bm.verts.new((-2.0, 2.0, 2.0))
#v3 = bm.verts.new((-2.0, -2.0, 2.0))

#bm.faces.new((v1, v2, v3))


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

def drawRadial(r, theta):
    xypos = [r * cos(theta), r * sin(theta)]
    if preVert is None:
        preVert = bm.verts.new((xypos[0], xypos[1], 0))
    else:
        newVert = bm.verts.new((xypos[0], xypos[1], 0))
        bm.edges.new((preVert, newVert))
        preVert = newVert


preVert = None

for i in range(78):
    seconds = i * 60
    position = list(calculateCoords(seconds))
    position[0] /= 4e4
    print(position)
    drawRadial(*position)



# Finish up, write the bmesh back to the mesh
bm.to_mesh(me)
bm.free()  # free and prevent further access
