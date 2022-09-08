from mathmeme import mul, norm, dot, sub, div

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

class DirectionalLight:
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = div(direction, norm(direction))
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT
        
    def getColor(self, intersect, raytracer):
        light_direction = [x*-1 for x in light_direction] 
        intensity =  dot(intersect.normal, light_direction) * self.intensity
        intensity = float(max(0, intensity))
                                                
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]
        
        reflect = 2 * dot(intersect.normal, light_direction)
        reflect = mul(reflect, intersect.normal)
        reflect = sub(reflect, light_direction)
        reflect = reflect / norm(reflect)
        
        view_direction = sub(raytracer.cam_position, intersect.point)
        view_direction = view_direction / norm(view_direction)
        
        spec_intensity = self.intensity * max(0, dot(view_direction, reflect)) ** intersect.scene_object.material.spec
        
        specColor = [spec_intensity * self.color[0],
                     spec_intensity * self.color[1],
                     spec_intensity * self.color[2]]
        
        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_direction, intersect.scene_object)
        
        if shadow_intersect:
            shadow_intensity = 1
            
        return (diffuseColor + specColor) * (1 - shadow_intensity)
    
class PointLight:
    def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT
        
    def getColor(self, intersect, raytracer):
        diffuseColor = (0,0,0)

        light_direction = sub(self.point, intersect.point)
        light_direction = light_direction / norm(light_direction)

        attenuation = 1.0
        intensity = dot(intersect.normal, light_direction) * attenuation
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        reflect = 2 * dot(intersect.normal, light_direction)
        reflect = mul(reflect, intersect.normal)
        reflect = sub(reflect, light_direction)
        reflect = reflect / norm(reflect)

        view_dir = sub(raytracer.camPosition, intersect.point)
        view_dir = view_dir / norm(view_dir)

        spec_intensity = attenuation * max(0, dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                     spec_intensity * self.color[1],
                     spec_intensity * self.color[2]]

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_direction, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return (diffuseColor + specColor) * (1 - shadow_intensity)
    
class AmbientLight():
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getColor(self):
        return mul(self.color,self.intensity)