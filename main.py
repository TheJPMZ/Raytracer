from gl import Raytracer
from figures import Sphere, Intersect, Material
from lights import AmbientLight, DirectionalLight, PointLight

width =  256
height =  256

snow = Material(diffuse = (1,1,1))
carrot = Material(diffuse = (1,0.5,0.5))
coal = Material(diffuse = (0,0,0))

rtx = Raytracer(width, height)

rtx.lights.append( AmbientLight(intensity = 0.2))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1)))
rtx.lights.append( PointLight(point = (0,0,0)))

rtx.scene.append( Sphere((0,2,-10), 1, snow))
rtx.scene.append( Sphere((0,0,-10), 1.5, snow))
rtx.scene.append( Sphere((0,-2.5,-10), 2, snow))

rtx.scene.append( Sphere((0,-1.25,-8), 0.35, coal))
rtx.scene.append( Sphere((0,-2.5,-8), 0.35, coal))
rtx.scene.append( Sphere((0,0,-8), 0.35, coal))

rtx.scene.append( Sphere((0,2,-9), 0.2, carrot))
rtx.scene.append( Sphere((0.3,2.3,-8.5), 0.1, coal))
rtx.scene.append( Sphere((-0.3,2.3,-8.5), 0.1, coal))

rtx.scene.append( Sphere((-0.2,1.3,-8), 0.1, coal))
rtx.scene.append( Sphere((0.2,1.3,-8), 0.1, coal))
rtx.scene.append( Sphere((0.6,1.4,-8), 0.1, coal))
rtx.scene.append( Sphere((-0.6,1.4,-8), 0.1, coal))

rtx.glRender()

rtx.glFinish("output.bmp")