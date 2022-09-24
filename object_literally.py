from struct import unpack
from numpy import arctan2, arccos, pi
from mathmeme import div, norm

class Model():
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertex = []
        self.texcoords = []
        self.normals =  []
        self.faces = []
        
        for line in self.lines:
            try:
                prefix, value = line.split(' ', 1)
            except:
                continue
            
            while value[0] == " ":
                value = value[1:]
                
            if prefix == 'v': # Vertices
                try:
                    self.vertex.append( list(map(float,value.split(' '))))
                except ValueError:
                    print(value)
                    raise
            elif prefix == 'vt':
                self.texcoords.append( list(map(float, value.split(' '))))
            elif prefix == 'vn':
                self.normals.append( list(map(float, value.split(' '))))
            elif prefix == 'f':
                try:
                    self.faces.append([  list(map(int, vert.strip().split('/'))) for vert in value.strip().split(' ')] )
                except ValueError:
                    print(value)
                    raise
        
class Texture():
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = unpack('=l', image.read(4))[0]
            
            image.seek(18)
            self.width = unpack('=l', image.read(4))[0]
            self.height = unpack('=l', image.read(4))[0]
            
            image.seek(headerSize)
            
            self.pixels = []
            
            l = 0
            for y in range(self.height):
                pixelRow = []
                
                for x in range(self.width):
                    b = ord(image.read(1))/255
                    g = ord(image.read(1))/255
                    r = ord(image.read(1))/255
                    
                    pixelRow.append((r, g, b))
                    l += 1
                    if l % 100 == 0:
                        print("Rendering filename", l/(self.width*self.height)*100, end="%\r")
                self.pixels.append(pixelRow)
            print("Succesfully loaded Texture: ",filename)
                        
    def getColor(self, u, v):
        if 0 <= u <= 1 and 0 <= v <= 1:
            x = int(v * self.width)
            y = int(u * self.height)
            try:
                return self.pixels[y][x]
            except IndexError:
                pass         
        else:
            return (1,1,1)
        
    def getEnvColor(self, dir):
        dir = div(dir, norm(dir))
        x = int((arctan2(dir[2], dir[0]) / (2 * pi) + 0.5) * self.width)
        y = int(arccos(-dir[1]) / pi * self.height)

        return self.pixels[y][x]    