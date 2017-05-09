import bpy
from bpy.props import *
import bmesh
from math import sin, cos, sqrt, pi, atan2
from mathutils import Vector, Quaternion

def calculateCords(ob, progress=None):
    bigG = 6.67408e-11
    mEarth = 5.972e24
    rmax = ob.rmax * 10**6
    rmin = ob.rmin * 10**6
    time = ob.time
    
    ecc = (rmax - rmin) / (rmax + rmin)
    
    p = 2 / (1 / rmin + 1 / rmax)
    
    if progress is None:
        # We need to find theta ourselves
        a = p / (1 - ecc ** 2)
        #b = p / sqrt(1 - ecc ** 2)
        
        period = 2 * pi * sqrt(a ** 3 / (bigG * mEarth))
        
        meananomaly = (time % period) * (2 * pi) / period
        
        # Use Newton's Method (9 steps) to calculate the eccentric anomaly
        eanom = meananomaly
        for it in range(9):
            eanom = meananomaly + ecc * sin(eanom)
        
        theta = 2 * atan2(sqrt(1 + ecc) * sin(eanom / 2), sqrt(1 - ecc) * cos(eanom / 2))
    
    else:
        theta = 2 * pi * progress
    
    radius = p / (1 + ecc * cos(theta))
    
    radius /= 4e5 # Make it smaller
    
    # Take the argument of periapsis into account
    # theta += ob.argofp
    
    xco, yco = radius * cos(theta), radius * sin(theta)
    
    # Rotate around y-axis for inclination:
    x, y, z = xco, yco, 0
    
    rotate1 = Quaternion((0.0, 1.0, 0.0), ob.inc)
    
    x, y, z = rotate1 * Vector((x, y, z))
    
    # angle to rotate for the argument of periapsis
    axis = rotate1 * Vector((0, 0, 1))
    # Rotate around for arg of periapsis
    rotate = Quaternion((axis.x, axis.y, axis.z), ob.argofp)
    x, y, z = rotate * Vector((x, y, z))
    
    # Rotate around z-axis for longitude of ascending node
    x, y, z = Quaternion((0.0, 0.0, 1.0), ob.longascend) * Vector((x, y, z))
    
    return (x, y, z)

def uObj(ob):
    if not ob.doorbit:
        return
    ob.location = calculateCords(ob)

def updateProperties(self, context):
    # check if orbitdisplay object exists
    me = bpy.data.objects["OD"].data
    # create a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(me)
    
    
    # TODO: Create OD object if it doesn't exist
    
    
    ob = context.object
    if not ob:
        return
    
    # Update the position of the object
    uObj(ob)
    
    # Remove the old verticies of the orbit display
    for v in bm.verts:
        bm.verts.remove(v)
    
    # Draw the orbit display
    preVert = None
    firstVert = None
    for i in range(100):
        pg = i / 100
        position = calculateCords(ob, progress=pg)
        if preVert is None:
            preVert = bm.verts.new(position)
            firstVert = preVert
        else:
            newVert = bm.verts.new(position)
            bm.edges.new((preVert, newVert))
            preVert = newVert
    bm.edges.new((preVert, firstVert))
    bm.to_mesh(me)
    bm.free()

bpy.types.Object.doorbit = BoolProperty(
    name="Do Orbit",
    default = False,
    update = updateProperties)

bpy.types.Object.rmin = FloatProperty(
    name="Perigee",
    default = 2.783,
    update = updateProperties)

bpy.types.Object.rmax = FloatProperty(
    name="Apogee",
    default = 6.783,
    update = updateProperties)

bpy.types.Object.argofp = FloatProperty(
    name="Arg of Periapsis",
    default = 0,
    update = updateProperties)

bpy.types.Object.inc = FloatProperty(
    name = "Inclination",
    default = 0,
    update = updateProperties)

bpy.types.Object.longascend = FloatProperty(
    name = "Longitude of Ascending Node",
    default = 0,
    update = updateProperties)

bpy.types.Object.time = FloatProperty(
    name="Simulation Time",
    default = 0,
    update = updateProperties)

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
        layout.prop(ob, 'inc')
        layout.prop(ob, 'argofp')
        layout.prop(ob, 'longascend')
        layout.prop(ob, 'time')

# Registration
bpy.utils.register_class(OrbitPanel)

def my_handler(scene):
    for obj in scene.objects:
        uObj(obj)

bpy.app.handlers.frame_change_post.append(my_handler)
