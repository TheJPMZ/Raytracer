from gl import Raytracer
from figures import REFLECTIVE, TRANSPARENT, Sphere, Intersect, Material
from lights import AmbientLight, DirectionalLight, PointLight
from object_literally import Texture

width =  1024
height =  1024

o1 = Material(diffuse = "red", spec = 64, ior=1)
o2 = Material(diffuse = "blue", spec = 64, ior = 2)
o3 = Material(diffuse = "yellow", spec = 64, ior = 3)

r1 = Material(diffuse = "red", spec = 1, matType= REFLECTIVE,)
r2 = Material(diffuse = "blue", spec = 32, matType = REFLECTIVE)
r3 = Material(diffuse = "yellow", spec = 64, matType = REFLECTIVE)

t1 = Material(diffuse = "red", spec = 64, matType = TRANSPARENT)
t2 = Material(diffuse = "blue", spec = 64, matType = TRANSPARENT)
t3 = Material(diffuse = "yellow", spec = 64, matType = TRANSPARENT)

rtx = Raytracer(width, height)

rtx.envMap = Texture("mansion.bmp")

rtx.lights.append( AmbientLight(intensity = 0.2 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.5 ))

rtx.scene.append( Sphere((-3,3,-10), 1, o1)  )
rtx.scene.append( Sphere((0,3,-10), 1, o2)  )
rtx.scene.append( Sphere((3,3,-10), 1, o3)  )

rtx.scene.append( Sphere((-3,0,-10), 1, t1)  )
rtx.scene.append( Sphere((0,0,-10), 1, t2)  )
rtx.scene.append( Sphere((3,0,-10), 1, t3)  )

rtx.scene.append( Sphere((-3,-3,-10), 1, r1)  )
rtx.scene.append( Sphere((0,-3,-10), 1, r2)  )
rtx.scene.append( Sphere((3,-3,-10), 1, r3)  )

rtx.glRender()

rtx.glFinish("output.bmp")