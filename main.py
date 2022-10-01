from numpy import diff, mat
from gl import Raytracer
from figures import REFLECTIVE, TRANSPARENT, Sphere, Intersect, Material, AABB
from lights import AmbientLight, DirectionalLight, PointLight
from object_literally import Texture

width =  256
height =  256

def draw_cube(coords, size, material):
    x,y,z = coords
    tr = size/2
    
    rtx.scene.append( AABB((x-tr,y,z), (0,size,size), material) )
    rtx.scene.append( AABB((x+tr,y,z), (0,size,size), material) )
    rtx.scene.append( AABB((x,y-tr,z), (size,0,size), material) )
    rtx.scene.append( AABB((x,y+tr,z), (size,0,size), material) )
    rtx.scene.append( AABB((x,y,z-tr), (size,size,0), material) )
    rtx.scene.append( AABB((x,y,z+tr), (size,size,0), material) )

wall = Material(diffuse = "blue", spec = 32, matType=REFLECTIVE)
roof = Material(diffuse = (0.6, 0.6, 0.6))
back = Material(diffuse = (0.3, 0.3, 0.3))

cube1 = Material(diffuse = "red")
cube2 = Material(diffuse = "red", spec = 32, ior = 2, matType=TRANSPARENT)
cube3 = Material(diffuse = "orange")
cube4 = Material(diffuse = "orange", spec = 32, ior = 2, matType=TRANSPARENT)

rtx = Raytracer(width, height)

#rtx.envMap = Texture("mansion.bmp")

rtx.lights.append( AmbientLight(intensity = 0.5 ))
rtx.lights.append( PointLight(point=(0,0,-2)))

z = 10
size = 6
tr = size/2

rtx.scene.append( AABB((tr,0,-z), (0.1,size,z), wall) )
rtx.scene.append( AABB((-tr,0,-z), (0.1,size,z), wall) )
rtx.scene.append( AABB((0,tr,-z), (size,0.1,z), roof) )
rtx.scene.append( AABB((0,-tr,-z), (size,0.1,z), roof) )

rtx.scene.append( AABB((0,0,-z), (size,size,0.1), back) )



draw_cube((-1,-1,-5), 0.5, cube1)
draw_cube((1,1,-5), 0.6, cube2)
draw_cube((1,-1,-5), 0.7, cube3)
draw_cube((-1,1,-5), 0.8, cube4)

rtx.glRender()

rtx.glFinish("output.bmp")