from mathmeme import mul, norm, dot, sub, div

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

def reflectVector(normal, direction):
    reflect = 2 * dot(normal, direction)
    reflect = mul(normal, reflect)
    reflect = sub(reflect, direction)
    reflect = div(reflect, norm(reflect))
    return reflect 

class DirectionalLight:
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = div(direction, norm(direction))
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = [x*-1 for x in self.direction] 
        intensity =  dot(intersect.normal, light_dir) * self.intensity
        intensity = float(max(0, intensity))         
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = [x*-1 for x in self.direction]
        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = sub(raytracer.camPosition, intersect.point)
        view_dir = div(view_dir,norm(view_dir))

        spec_intensity = self.intensity * max(0, dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                     spec_intensity * self.color[1],
                     spec_intensity * self.color[2]]

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = [x*-1 for x in self.direction]

        shadow_intensity = 0
        shadow_intersect = raytracer.sceneIntersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class PointLight(object):
    def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = sub(self.point, intersect.point)
        light_dir = light_dir / norm(light_dir)

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0
        intensity = dot(intersect.normal, light_dir) * attenuation
        intensity = float(max(0, intensity))              
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = sub(self.point, intersect.point)
        light_dir = light_dir / norm(light_dir)

        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = sub(raytracer.camPosition, intersect.point)
        view_dir = view_dir / norm(view_dir)

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0

        spec_intensity = attenuation * max(0, dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                     spec_intensity * self.color[1],
                     spec_intensity * self.color[2]]

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = sub(self.point, intersect.point)
        light_dir = light_dir / norm(light_dir)

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        return mul(self.color,self.intensity)

    def getSpecColor(self, intersect, raytracer):
        return [0,0,0]

    def getShadowIntensity(self, intersect, raytracer):
        return 0
