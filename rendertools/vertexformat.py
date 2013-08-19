import gl, glsl
from ctypes import Structure

gltypes = {
    gl.FLOAT: gl.gl_float,
    gl.DOUBLE: gl.gl_double,
    gl.UNSIGNED_BYTE: gl.gl_ubyte,
    gl.BYTE: gl.gl_byte,
    gl.UNSIGNED_INT: gl.gl_uint,
    gl.INT: gl.gl_int,
}

def structure(gldef):
    fields = []
    for name, count, gltype, normalized in gldef:
        fields.append((name, gltypes[gltype] * count))
    return type('vertexformat', (Structure,), {"_fields_":fields})

def set_vertex_pointer(program, name, size, kind, normalized, stride, offset):
    if isinstance(program, glsl.Program):
        a = program.attribLoc(name)
    else:
        a = gl.getAttribLocation(program, name)
    if a >= 0:
        gl.enableVertexAttribArray(a)
        gl.vertexAttribPointer(a, size, kind, normalized, stride, offset)
    
def unset_vertex_pointer(program, name):
    if isinstance(program, glsl.Program):
        a = program.attribLoc(name)
    else:
        a = gl.getAttribLocation(program, name)
    if a >= 0:
        gl.disableVertexAttribArray(a)

class VertexFormat(object):
    def __init__(self, gldef):
        self.gldef = gldef
        self.ctype = structure(gldef)
        self.stride = gl.sizeof(self.ctype)
    
    def enable(self, program):
        for name, count, gltype, normalized in self.gldef:
            offset = getattr(self.ctype, name).offset
            set_vertex_pointer(program, name, count, gltype, normalized, self.stride, offset)

    def disable(self, program):
        for name, count, gltype, normalized in self.gldef:
            unset_vertex_pointer(program, name)
