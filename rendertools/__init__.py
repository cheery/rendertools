from vertexformat import VertexFormat
from glsl import Program
import gl

def hex2color(hexadecimal):
    data = hexadecimal.lstrip('#').decode('hex')
    r = ord(data[0]) / 255.0
    g = ord(data[1]) / 255.0
    b = ord(data[2]) / 255.0
    if len(data) > 3:
        a = ord(data[3]) / 255.0
    else:
        a = 1.0
    return [r,g,b,a]


try:
    import pygame

    class Image(object):
        def __init__(self, width, height, data):
            self.width  = width
            self.height = height
            self.format = gl.RGBA
            self.type   = gl.UNSIGNED_BYTE
            self.data   = data

        @classmethod
        def load(cls, path):
            surface = pygame.image.load(path)
            width, height = surface.get_size()
            data = pygame.image.tostring(surface, "RGBA", True)
            return cls(width, height, data)
except ImportError, e:
    pass

class VertexStream(object):
    def __init__(self, vertexformat):
        self.vertexbuffer = gl.createBuffer()
        self.vertexformat = vertexformat
        self.vertex = vertexformat.ctype()
        self.clear()

    def clear(self):
        self.count = 0
        self.data = ''

    def emit(self): 
        self.data += buffer(self.vertex)[:]
        self.count += 1

    def draw(self, gpu, mode=gl.TRIANGLES):
        gl.bindBuffer(gl.ARRAY_BUFFER, self.vertexbuffer)
        gl.bufferData(gl.ARRAY_BUFFER, len(self.data), self.data, gl.DYNAMIC_DRAW)
        self.vertexformat.enable(gpu)
        gl.drawArrays(mode, 0, self.count)
        self.vertexformat.disable(gpu)
        gl.bindBuffer(gl.ARRAY_BUFFER, 0)
        self.clear()
