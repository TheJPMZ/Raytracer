from mathmeme import mul, sub, add, div, dot, norm

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

class Intersect(object):
    def __init__(self, distance, point, normal, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = "white"):
        
        if isinstance(diffuse,str):
            diffuse = colors.get(diffuse)
        
        self.diffuse = diffuse


class Sphere(object):
    def __init__(self, center, radius, material):
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

        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         sceneObj = self)
