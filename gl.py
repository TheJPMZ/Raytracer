import struct
from math import cos, sin, tan, pi

from figures import OPAQUE, REFLECTIVE, TRANSPARENT
from lights import reflectVector
from mathmeme import mul, div, add, norm,dot, matmul, sub

STEPS = 1
MAX_RECURSION_DEPTH = 3

def refractVector(normal, dirVector, ior):

    cosi = max(-1, min(1 , dot(dirVector, normal)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        normal = [x*-1 for x in normal] 

    eta = etai / etat
    k = 1 - eta * eta * (1 - (cosi * cosi))

    if k < 0: #Total Internal Reflection
        return None

    R = add(mul(dirVector,eta), mul(normal,(eta * cosi - k ** 0.5)))
    return div(R,norm(R))

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

def fresnel(normal, dirVector, ior):
    cosi = max(-1, min(1 , dot(dirVector, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1: #Total internal reflection
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))

    return (Rs * Rs + Rp * Rp) / 2

class Raytracer(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.fov = 60
        self.nearPlane = 0.1
        self.camPosition = (0,0,0)

        self.scene = [ ]
        self.lights = [ ]

        self.envMap = None

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

    def scene_intersect(self, orig, dir, sceneObj):
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

    def cast_ray(self, orig, dir, sceneObj = None, recursion = 0):
        intersect = self.scene_intersect(orig, dir, sceneObj)

        if not intersect or recursion >= MAX_RECURSION_DEPTH:
            if self.envMap:
                return self.envMap.getEnvColor(dir)
            else:
                return (self.clearColor[0] / 255,
                        self.clearColor[1] / 255,
                        self.clearColor[2] / 255)

        material = intersect.sceneObj.material

        finalColor:list = [0, 0, 0]
        objectColor:list = [*material.diffuse]
        refractColor:list = [0, 0, 0]
        if material.matType == OPAQUE:
            for light in self.lights:
                diffuseColor:list = light.getDiffuseColor(intersect, self)
                specColor:list = light.getSpecColor(intersect, self)
                shadowIntensity:int = light.getShadowIntensity(intersect, self)

                lightColor:list = mul(add(diffuseColor,specColor),(1 - shadowIntensity))

                finalColor = add(finalColor, lightColor)

        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intersect.normal, [x*-1 for x in dir])
            reflectColor = self.cast_ray(intersect.point, reflect, intersect.sceneObj, recursion + 1)

            specColor = [0,0,0]
            for light in self.lights:
                specColor = add(specColor, light.getSpecColor(intersect, self))

            finalColor = add(reflectColor, specColor)

        elif material.matType == TRANSPARENT:
            outside = dot(dir, intersect.normal) < 0
            bias =  mul(intersect.normal, 0.001)
            kr = fresnel(intersect.normal, dir, material.ior)
            specColor = [0,0,0]

            reflect = reflectVector(intersect.normal, [x*-1 for x in dir])
            reflectOrig = add(intersect.point, bias) if outside else sub(intersect.point, bias)
            reflectColor = self.cast_ray(reflectOrig, reflect, None, recursion + 1)

            for light in self.lights:
                specColor = add(specColor, light.getSpecColor(intersect, self))
            if kr < 1:
                refract = refractVector(intersect.normal, dir, material.ior )
                refractOrig = sub(intersect.point, bias) if outside else add(intersect.point, bias)
                refractColor = self.cast_ray(refractOrig, refract, None, recursion + 1)

            finalColor = add(mul(reflectColor,kr),add(mul(refractColor,(1 - kr)),specColor))

        finalColor = [a*b for a,b in zip(finalColor, objectColor)]

        r,g,b = map(lambda x: min(1,x), finalColor)

        return (r,g,b)
    
    def glRender(self):
        # Proyeccion
        t = tan((self.fov * pi / 360)) * self.nearPlane
        r = t * self.vpWidth / self.vpHeight

        for y in range(self.vpY, self.vpY + self.vpHeight + 1, STEPS):
            for x in range(self.vpX, self.vpX + self.vpWidth + 1, STEPS):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC (-1 a 1)
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                Px *= r
                Py *= t

                direction = (Px, Py, -self.nearPlane)
                direction = div(direction,norm(direction)) 

                rayColor = self.cast_ray(self.camPosition, direction)

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
