import bpy
from bpy.props import *
from math import sin, cos, sqrt, pi, atan2


def uObj(ob):
    if not ob.doorbit:
        return
    bigG = 6.67408e-11
    mEarth = 5.972e24
    rmax = ob.rmax
    rmin = ob.rmin
    time = ob.time
    ecc = (rmax - rmin) / (rmax + rmin)

    p = 2 / (1 / rmin + 1 / rmax)

    a = p / (1 - ecc ** 2)
    b = p / sqrt(1 - ecc ** 2)

    period = 2 * pi * sqrt(a ** 3 / (bigG * mEarth))

    meananomaly = (time % period) * (2 * pi) / period

    eanom = meananomaly
    for it in range(9):
        eanom = meananomaly + ecc * sin(eanom)

    theta = 2 * atan2(sqrt(1 + ecc) * sin(eanom / 2), sqrt(1 - ecc) * cos(eanom / 2))

    radius = p / (1 + ecc * cos(theta))

    radius /= 4e5  # Make it smaller

    xco, yco = radius * cos(theta), radius * sin(theta)

    ob.location = (xco, yco, 0)


def updateProperties(self, context):
    ob = context.object
    if not ob:
        return

    # Update the position of the object
    uObj(ob)


bpy.types.Object.doorbit = BoolProperty(
    name="Do Orbit",
    default=False,
    update=updateProperties)

bpy.types.Object.rmin = FloatProperty(
    name="Min Radius",
    default=2.783e6,
    update=updateProperties)

bpy.types.Object.rmax = FloatProperty(
    name="Max Radius",
    default=6.783e6,
    update=updateProperties)

bpy.types.Object.time = FloatProperty(
    name="Simulation Time",
    default=0,
    update=updateProperties)


class OrbitPanel(bpy.types.Panel):
    bl_label = "Orbit Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        ob = context.object
        if not ob:
            return
        layout = self.layout
        layout.prop(ob, 'doorbit')
        layout.prop(ob, 'rmin')
        layout.prop(ob, 'rmax')
        layout.prop(ob, 'time')


# Registration
bpy.utils.register_class(OrbitPanel)


def my_handler(scene):
    for obj in scene.objects:
        uObj(obj)


bpy.app.handlers.frame_change_post.append(my_handler)