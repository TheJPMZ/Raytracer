from numpy import diff, mat
from gl import Raytracer
from figures import OPAQUE, REFLECTIVE, TRANSPARENT, Sphere, Intersect, Material, AABB, Triangle
from lights import AmbientLight, DirectionalLight, PointLight
from object_literally import Texture

width =  64
height =  64

def draw_cube(coords, size, material):
    x,y,z = coords
    tr = size/2
    
    rtx.scene.append( AABB((x-tr,y,z), (0,size,size), material) )
    rtx.scene.append( AABB((x+tr,y,z), (0,size,size), material) )
    rtx.scene.append( AABB((x,y-tr,z), (size,0,size), material) )
    rtx.scene.append( AABB((x,y+tr,z), (size,0,size), material) )
    rtx.scene.append( AABB((x,y,z-tr), (size,size,0), material) )
    rtx.scene.append( AABB((x,y,z+tr), (size,size,0), material) )

m1 = Material(diffuse = 'orange', spec = 64, matType = REFLECTIVE)
m2 = Material(diffuse = 'green', spec = 64, matType = TRANSPARENT)
m3 = Material(diffuse = 'magenta', spec = 64, matType = OPAQUE)

rtx = Raytracer(width, height)
rtx.envMap = Texture("mansion.bmp")

rtx.lights.append( AmbientLight(intensity = 0.6 ))
rtx.lights.append( PointLight(point=(0,0,-2)))

rtx.scene.append( Triangle((-1.5,1,-7), (1.5,1,-7), (0,3,-7), m1) )
rtx.scene.append( Triangle((1.5,1,-7), (2,2,-7), (0,3,-7), m1) )

rtx.scene.append( Triangle((-1.5,-1,-7), (1.5,-1,-7), (0,1,-7), m2) )
rtx.scene.append( Triangle((1.5,-1,-7), (2,0,-7), (0,1,-7), m2) )

rtx.scene.append( Triangle((-1.5,-3,-7), (1.5,-3,-7), (0,-1,-7), m3) )
rtx.scene.append( Triangle((1.5,-3,-7), (2,-2,-7), (0,-1,-7), m3) )

rtx.glRender()

rtx.glFinish("output.bmp")