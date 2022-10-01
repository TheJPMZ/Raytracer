from mathmeme import mul, sub, add, div, dot, norm
from numpy import arctan2, pi, arccos

colors = {
    "white": (1, 1, 1),
    "black": (0, 0, 0),
    "red": (1, 0, 0),
    "orange": (1, 0.5, 0),
    "yellow": (1, 1, 0),
    "light-green": (0.5, 1, 0),
    "green": (0, 1, 0),
    "blue-green": (0, 1, 0.5),
    "sky-blue": (0, 1, 1),
    "blue": (0, 0.5, 1),
    "dark-blue": (0, 0, 1),
    "purple": (0.5, 0, 1),
    "magenta": (1, 0, 1),
    "rose": (1, 0, 0.5)
    }

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texCoords = texCoords
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = "white", ior = 1, spec = 1.0, matType = OPAQUE, texture = None):
        
        if isinstance(diffuse,str):
            diffuse = colors.get(diffuse)
        
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType


class Sphere(object):
    def __init__(self, center, radius, material = Material()):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin, direction):
        L = sub(self.center, origin)
        tca = dot(L, direction)
        d = (norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = add(origin, mul((direction), t0))
        normal = sub(P, self.center)
        normal = div(normal, norm(normal))
        
        u = 1 - ((arctan2(normal[2],normal[0])/ (2*pi))+0.5)
        v = arccos(-normal[1]) / pi
        
        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         texCoords = (u,v),
                         sceneObj = self)

class Plane:
    def __init__(self, position, normal, material = Material()):
        self.position = position
        self.normal = div(normal,norm(normal))
        self.material = material

    def ray_intersect(self, orig, dir):
        
        denom = dot(dir, self.normal)

        if abs(denom) > 0.0001:
            num = dot(sub(self.position, orig), self.normal)
            t = num / denom
            if t > 0:

                hit = add(orig, mul(dir,t))

                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObj = self)

        return None

import numpy as np
from collections import namedtuple
V3 = namedtuple('Point3', ['x', 'y', 'z'])

class AABB:
    # * Axis Aligned Bounding Box
    def __init__(self, position, size, material = Material()):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        hSx,hSy,hSz = map(lambda x:x / 2, size)

        #Sides
        self.planes.append(Plane( add(position, (hSx,0,0)), (1,0,0), material))
        self.planes.append(Plane( add(position, (-hSx,0,0)), (-1,0,0), material))

        # Up and down
        self.planes.append(Plane( add(position, (0,hSy,0)), (0,1,0), material))
        self.planes.append(Plane( add(position, (0,-hSy,0)), (0,-1,0), material))

        # Front and Back
        self.planes.append(Plane( add(position, (0,0,hSz)), (0,0,1), material))
        self.planes.append(Plane( add(position, (0,0,-hSz)), (0,0,-1), material))

        #Bounds
        epsilon = 0.001
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + self.size[i]/2)
            self.boundsMax[i] = self.position[i] + (epsilon + self.size[i]/2)


    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter:
                # Si estoy dentro de los bounds
                if planeInter.point[0] >= self.boundsMin[0] and planeInter.point[0] <= self.boundsMax[0]:
                    if planeInter.point[1] >= self.boundsMin[1] and planeInter.point[1] <= self.boundsMax[1]:
                        if planeInter.point[2] >= self.boundsMin[2] and planeInter.point[2] <= self.boundsMax[2]:
                            #Si soy el plano mas cercano
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                wx,wy,wz = map(lambda inter,min,max:(inter - min)/(max-min),planeInter.point,self.boundsMin,self.boundsMax)

                                if abs(plane.normal[0]) > 0:
                                    u, v = wy, wz
                                elif abs(plane.normal[1]) > 0:
                                    u, v = wx, wz
                                elif abs(plane.normal[2]) > 0:
                                    u, v = wx, wy


        if not intersect:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = (u,v),
                         sceneObj = self)



        