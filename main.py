from numpy import diff, mat
from gl import Raytracer
from figures import OPAQUE, REFLECTIVE, TRANSPARENT, Sphere, Intersect, Material, AABB, Triangle
from lights import AmbientLight, DirectionalLight, PointLight
from object_literally import Texture

width =  128
height =  128

m1 = Material(diffuse = 'orange', spec = 64, matType = REFLECTIVE)
m2 = Material(diffuse = 'green', spec = 64, matType = TRANSPARENT)
m3 = Material(diffuse = 'magenta', spec = 64, matType = OPAQUE)
m4 = Material(diffuse = 'yellow', spec = 64, matType = OPAQUE, texture=Texture("sponge.bmp"))
m51 = Material(diffuse = 'white', spec = 0.5, matType = TRANSPARENT)
m52 = Material(diffuse = 'white', spec = 64, matType = REFLECTIVE)
m5 = Material(diffuse = 'white', spec = 64, matType = OPAQUE)

tie = Material(diffuse = 'red', spec = 64, matType = OPAQUE)
shirt = Material(diffuse = (0.85,0.85,0.85), spec = 64, matType = OPAQUE)
shirt2 = Material(diffuse = (1,1,1), spec = 64, matType = OPAQUE)
pants = Material(diffuse = (0.6,0.3,0), spec = 64, matType = OPAQUE)
pupil = Material(diffuse = 'black', spec = 64, matType = REFLECTIVE)
eye = Material(diffuse = 'sky-blue', spec = 64, matType = TRANSPARENT)

rtx = Raytracer(width, height)
rtx.envMap = Texture("mansion.bmp")

rtx.lights.append( DirectionalLight((0,-10,-1), 0.1))
rtx.lights.append( AmbientLight(intensity = 0.3 ))
rtx.lights.append( PointLight(point=(4,2,-6)))

#rtx.scene.append( Triangle((-1.5,1,-7), (1.5,1,-7), (0,3,-7), m1) )
#rtx.scene.append( Triangle((1.5,1,-7), (2,2,-7), (0,3,-7), m1) )
#
#rtx.scene.append( Triangle((-1.5,-1,-7), (1.5,-1,-7), (0,1,-7), m2) )
#rtx.scene.append( Triangle((1.5,-1,-7), (2,0,-7), (0,1,-7), m2) )
#
#rtx.scene.append( Triangle((1.5,-3,-7), (0,-1,-7), (-1.5,-3,-7), m5) )
#rtx.scene.append( Triangle((2,-2,-7), (0,-1,-7), (1.5,-3,-7), m5) )

rtx.scene.append( AABB((-0.5,-1,-9), (5,5,0), m4) )

rtx.scene.append( Triangle((-2.9,1.5,-9), (-4,-3,-10), (-4,2.5,-10), m4) )
rtx.scene.append( Triangle((-2.9,-3.5,-9), (-2.9,1.5,-9), (-4,-3,-10), m4) )

rtx.scene.append( Triangle((-2.9,1.5,-9), (-4,2.5,-10), (1,2.5,-10), m4) )
rtx.scene.append( Triangle((2,1.5,-9), (-2.9,1.5,-9), (1,2.5,-10), m4) )

rtx.scene.append( Sphere((-1,-0.3,-8), 0.9, m52) )
rtx.scene.append( Sphere((-0.8,-0.3,-7), 0.3, eye) )
rtx.scene.append( Sphere((-0.7,-0.3,-6), 0.15, pupil) )


rtx.scene.append( Sphere((0.3,-0.3,-8), 0.9, m51) )
rtx.scene.append( Sphere((0.2,-0.3,-7), 0.3, eye) )
rtx.scene.append( Sphere((0.2,-0.3,-6), 0.15, pupil) )

rtx.scene.append( AABB((-0.7,-2.3,-8.5), (1.5,1,0), m3) )

rtx.scene.append( AABB((-0.7,-2,-8), (0.4,0.4,0), m5) )
rtx.scene.append( AABB((0.1,-2,-8), (0.4,0.4,0), m5) )


rtx.scene.append( AABB((-0.5,-5,-10), (5.4,1,0), pants) )

rtx.scene.append( Triangle((-3,-5.5,-10), (-3,-4.5,-10), (-4,-4.5,-10), pants) )
rtx.scene.append( Triangle((-4,-4,-10), (-3,-4.5,-10), (-4,-4.5,-10), pants) )


rtx.scene.append( AABB((-0.5,-4,-10), (5.4,1,0), shirt) )

rtx.scene.append( Triangle((-3,-4.5,-10), (-3,-4,-10), (-4,-4,-10), shirt) )
rtx.scene.append( Triangle((-4,-3,-10), (-3,-4,-10), (-4,-4,-10), shirt) )


rtx.scene.append( Triangle((-0.5,-4,-9.9), (-2.5,-4,-9.9), (-1.5,-4.5,-9.9), shirt2) )
rtx.scene.append( Triangle((1.5,-4,-9.9), (-0.5,-4,-9.9), (0.5,-4.5,-9.9), shirt2) )

rtx.scene.append( Triangle((-0.5,-5.5,-9.9), (-0.5,-4,-9.9), (0,-5,-9.9), tie) )
rtx.scene.append( Triangle((-0.5,-5.5,-9.9), (-0.5,-4,-9.9), (-1.1,-5,-9.9), tie) )


rtx.glRender()

rtx.glFinish("output.bmp")