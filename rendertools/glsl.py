import re, gl, sys
record = re.compile(r"^(\w+):")

def parse(source):
    name    = None
    shared  = []
    lines   = shared
    for line in source.splitlines():
        match = record.match(line)
        if match:
            if name != None:
                yield name, '\n'.join(shared + lines)
            name = match.groups()[0]
            lines = []
        else:
            lines.append(line)
    if name != None:
        yield name, '\n'.join(shared + lines)

shadertypes = {
    'VERTEX': gl.VERTEX_SHADER,
    'FRAGMENT': gl.FRAGMENT_SHADER,
    'GEOMETRY': gl.GEOMETRY_SHADER,
    'TESS_EVALUATION': gl.TESS_EVALUATION_SHADER,
    'TESS_CONTROL': gl.TESS_CONTROL_SHADER,
    'COMPUTE': gl.COMPUTE_SHADER,
}

class Program(object):
    def __init__(self, obj):
        self._as_parameter_ = obj
        self.uniform_cache = {}
        self.attrib_cache = {}

    def attribLoc(self, name):
        if not name in self.attrib_cache:
            self.attrib_cache[name] = gl.getAttribLocation(self, name)
        return self.attrib_cache[name]

    def loc(self, name):
        if not name in self.uniform_cache:
            self.uniform_cache[name] = gl.getUniformLocation(self, name)
        return self.uniform_cache[name]

    @classmethod
    def load(cls, path, log=sys.stderr):
        with open(path) as fd:
            source = fd.read()
        return cls.fromSource(source, log, path)

    @classmethod
    def fromSource(cls, source, log=sys.stderr, path=None):
        gpu = gl.createProgram()
        success = gl.TRUE
        for name, lines in parse(source):
            shader = gl.createShader(shadertypes[name])
            gl.attachShader(gpu, shader)
            gl.shaderSource(shader, lines)
            gl.compileShader(shader)
            success &= gl.getShaderParameter(shader, gl.COMPILE_STATUS)
            logmessage = gl.getShaderInfoLog(shader)
            if len(logmessage) > 0:
                log.write('compile %s section %s:\n%s' % (path, name, logmessage))
        gl.linkProgram(gpu)
        success &= gl.getProgramParameter(gpu, gl.LINK_STATUS)
        logmessage = gl.getProgramInfoLog(gpu)
        if len(logmessage) > 0:
            log.write('link %s:\n%s' % (path, logmessage))
        if success == gl.TRUE:
            return Program(gpu)
        else:
            raise Exception("could not load program %s" % path)
