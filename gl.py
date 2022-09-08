"""
Basado en el codigo realizado en clase de Graficas por computadora con el 
profesor Carlos.
Hecho por Jose Monzon
"""

import struct
from math import cos, sin, tan, pi
from mathmeme import mul, div, add, norm,dot


def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)] )

def bary_coords(A, B, C, P) -> tuple: 
    
    ax, ay, _ = A
    bx, by, _ = B
    cx, cy, _ = C
    px, py = P
    
    area_PBC = (by - cy) * (px - cx) + (cx - bx) * (py - cy)
    area_PAC = (cy - ay) * (px - cx) + (ax - cx) * (py - cy)
    area_ABC = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    
    if area_ABC == 0: #Zero area triangle
        return -1, -1, -1

    u = area_PBC / area_ABC
    v = area_PAC / area_ABC
    w = 1 - u - v
    
    return u, v, w

class Raytracer(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.fov = 60
        self.nearPlane = 0.1
        self.camPosition = (0,0,0)

        self.scene = [ ]
        self.lights = [ ]


        self.clearColor = color(0,0,0)
        self.currColor = color(1,1,1)

        self.glViewport(0,0,self.width, self.height)
        
        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[ self.clearColor for y in range(self.height)]
                         for x in range(self.width)]




    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)


    def glPoint(self, x, y, clr = None): # Window Coordinates
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def sceneIntersect(self, orig, dir, sceneObj):
        depth = float('inf')
        intersect = None

        for obj in self.scene:
            hit = obj.ray_intersect(orig, dir)
            if hit != None:
                if sceneObj != hit.sceneObj:
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance

        return intersect

    def castRay(self, orig, dir):
        intersect = self.sceneIntersect(orig, dir, None)

        if not intersect:
            return None

        material = intersect.sceneObj.material

        finalColor, dirLightColor, ambLightColor = [0,0,0], [0,0,0], [0,0,0]
        objectColor = [*material.diffuse]

        for light in self.lights:
            if light.lightType == 0: # directional light
                diffuseColor = [0,0,0] 

                light_dir = mul(light.direction, -1)
                intensity = dot(intersect.normal, light_dir)
                intensity = float(max(0, intensity))

                diffuseColor = [intensity * light.color[0] * light.intensity,
                                intensity * light.color[1] * light.intensity,
                                intensity * light.color[2] * light.intensity]

                shadow_intersect = self.sceneIntersect(intersect.point, light_dir, intersect.sceneObj)
                
                shadow_intensity = 1 if shadow_intersect else 0

                dirLightColor = add(dirLightColor, mul(diffuseColor,(1 - shadow_intensity))) 

            elif light.lightType == 2: # ambient light
                
                ambLightColor = mul(light.color, light.intensity)

        finalColor = add(dirLightColor,ambLightColor)

        finalColor = [a*b for a,b in zip(finalColor, objectColor)]

        r,g,b = map(lambda x: min(1,x), finalColor)

        return (r,g,b)

    def glRender(self):
        for y in range(self.vpY, self.vpY + self.vpHeight + 1):
            for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC (-1 a 1)
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                # Proyeccion
                t = tan((self.fov * pi / 360)) * self.nearPlane
                r = t * self.vpWidth / self.vpHeight

                Px *= r
                Py *= t

                direction = (Px, Py, -self.nearPlane)
                direction = div(direction,norm(direction)) 

                rayColor = self.castRay(self.camPosition, direction)

                if rayColor is not None:
                    rayColor = color(rayColor[0],rayColor[1],rayColor[2])
                    self.glPoint(x, y, rayColor)





    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
                    