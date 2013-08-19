from constants import *

#from globject import GLObject
from ctypes import (
    util, cdll,
    c_float, c_double, c_int, c_uint, c_void_p, c_long, c_ulong, c_void_p, c_char, c_char_p, c_byte, c_ubyte,
    CFUNCTYPE, POINTER, byref, sizeof,
)

lib = cdll.LoadLibrary(util.find_library('GL'))

getCurrentContext = lib.glXGetCurrentContext
getCurrentContext.restype = c_void_p
getProcAddress = lib.glXGetProcAddress
getProcAddress.restype = c_void_p

def procedure(name, restype, *argtypes):
    sig = CFUNCTYPE(restype, *argtypes)
    return sig(getProcAddress(name))

gl_float = c_float
gl_double = c_double
gl_enum  = c_uint
gl_bool  = c_uint
gl_byte  = c_byte
gl_ubyte  = c_ubyte
gl_int   = c_int
gl_uint  = c_uint
gl_long = c_long
gl_ulong = c_ulong

gl_object = gl_uint
gl_data = c_void_p
gl_char = c_char
gl_string = c_char_p

## follows the webgl quick reference card
# per-fragment operations
blendColor = procedure('glBlendColor', None, gl_float, gl_float, gl_float, gl_float)
blendEquation = procedure('glBlendEquation', None, gl_enum)
blendEquationSeparate = procedure('glBlendEquationSeparate', None, gl_enum, gl_enum)
blendFunc = procedure('glBlendFunc', None, gl_enum, gl_enum)
blendFuncSeparate = procedure('glBlendFuncSeparate', None, gl_enum, gl_enum, gl_enum, gl_enum)
depthFunc = procedure('glDepthFunc', None, gl_enum)
sampleCoverage = procedure('glSampleCoverage', None, gl_float, gl_bool)
stencilFunc = procedure('glStencilFunc', None, gl_enum, gl_int, gl_uint)
stencilFuncSeparate = procedure('glStencilFuncSeparate', None, gl_enum, gl_enum, gl_int, gl_uint)
stencilOp = procedure('glStencilOp', None, gl_enum, gl_enum, gl_enum)
stencilOpSeparate = procedure('glStencilOpSeparate', None, gl_enum, gl_enum, gl_enum, gl_enum)

# whole framebuffer operations
clear = procedure('glClear', None, gl_ulong)
clearColor = procedure('glClearColor', None, gl_float, gl_float, gl_float, gl_float)
clearDepth = procedure('glClearDepth', None, gl_float)
clearStencil = procedure('glClearStencil', None, gl_int)
colorMask = procedure('glColorMask', None, gl_bool, gl_bool, gl_bool, gl_bool)
depthMask = procedure('glDepthMask', None, gl_bool)
stencilMask = procedure('glStencilMask', None, gl_uint)
stencilMaskSepraate = procedure('glStencilMaskSeparate', None, gl_enum, gl_uint)

# buffer objects
bindBuffer = procedure('glBindBuffer', None, gl_enum, gl_object)
bufferData = procedure('glBufferData', None, gl_enum, gl_long, gl_data, gl_enum)
bufferSubData = procedure('glBufferSubData', None, gl_enum, gl_long, gl_long, gl_data, gl_enum)
isBuffer = procedure('glIsBuffer', gl_bool, gl_object)
#missing: getBufferParameter
raw_GenBuffers = procedure('glGenBuffers', None, gl_long, POINTER(gl_object))
def createBuffer():
    obj = gl_object()
    raw_GenBuffers(1, byref(obj))
    return obj
raw_DeleteBuffers = procedure('glDeleteBuffers', None, gl_long, POINTER(gl_object))
def deleteBuffer(obj):
    raw_DeleteBuffers(1, byref(obj))

# view and clip
depthRange = procedure('glDepthRange', None, gl_float, gl_float)
scissor = procedure('glScissor', None, gl_int, gl_int, gl_long, gl_long)
viewport = procedure('glViewport', None, gl_int, gl_int, gl_long, gl_long)

# rasterization
cullFace = procedure('glCullFace', None, gl_enum)
frontFace = procedure('glFrontFace', None, gl_enum)
lineWidth = procedure('glLineWidth', None, gl_float)
polygonOffset = procedure('glPolygonOffset', None, gl_float, gl_float)

# programs and shaders
attachShader = procedure('glAttachShader', None, gl_object, gl_object)
bindAttribLocation = procedure('glBindAttribLocation', None, gl_object, gl_uint, gl_string)
compileShader = procedure('glCompileShader', None, gl_object)
createProgram = procedure('glCreateProgram', gl_object)
createShader = procedure('glCreateShader', gl_object, gl_enum)
deleteProgram = procedure('glDeleteProgram', None, gl_object)
deleteShader = procedure('glDeleteShader', None, gl_object)
detachShader = procedure('glDetachShader', gl_object, gl_object)
raw_GetShaderiv = procedure('glGetShaderiv', None, gl_object, gl_enum, POINTER(gl_int))
def getShaderParameter(obj, pname):
    out = gl_int()
    raw_GetShaderiv(obj, pname, byref(out))
    return out.value
raw_GetProgramiv = procedure('glGetProgramiv', None, gl_object, gl_enum, POINTER(gl_int))
def getProgramParameter(obj, pname):
    out = gl_int()
    raw_GetProgramiv(obj, pname, byref(out))
    return out.value
raw_GetAttachedShaders = procedure('glGetAttachedShaders', None, gl_object, gl_long, POINTER(gl_long), POINTER(gl_object))
def getAttachedShaders(obj):
    length = getProgramParameter(obj, ATTACHED_SHADERS)
    out = (gl_uint*length)()
    raw_GetAttachedShaders(obj, length, None, out)
    return out[:]
isProgram = procedure('glIsProgram', gl_bool, gl_object)
isShader = procedure('glIsShader', gl_bool, gl_object)
linkProgram = procedure('glLinkProgram', None, gl_object)
useProgram = procedure('glUseProgram', None, gl_object)
validateProgram = procedure('glValidateProgram', None, gl_object)
raw_ShaderSource = procedure('glShaderSource', None, gl_object, gl_long, POINTER(gl_string), POINTER(gl_int))
def shaderSource(obj, source):
    raw_ShaderSource(obj, 1, byref(gl_string(source)), byref(gl_int(len(source))))
raw_GetShaderInfoLog = procedure('glGetShaderInfoLog', None, gl_object, gl_long, POINTER(gl_long), gl_string)
def getShaderInfoLog(obj):
    length = getShaderParameter(obj, INFO_LOG_LENGTH)
    out = (gl_char*length)()
    raw_GetShaderInfoLog(obj, length, None, out)
    return out.value
raw_GetProgramInfoLog = procedure('glGetProgramInfoLog', None, gl_object, gl_long, POINTER(gl_long), gl_string)
def getProgramInfoLog(obj):
    length = getProgramParameter(obj, INFO_LOG_LENGTH)
    out = (gl_char*length)()
    raw_GetProgramInfoLog(obj, length, None, out)
    return out.value

# uniforms and attributes
disableVertexAttribArray = procedure('glDisableVertexAttribArray', None, gl_uint)
enableVertexAttribArray = procedure('glEnableVertexAttribArray', None, gl_uint)
#missing: getActiveAttrib
#missing: getActiveUniform
#missing: getUniform
getAttribLocation = procedure('glGetAttribLocation', gl_int, gl_object, gl_string)
getUniformLocation = procedure('glGetUniformLocation', gl_int, gl_object, gl_string)
#missing: getVertexAttrib
#missing: getVertexAttribOffset

uniform1f = procedure('glUniform1f', None, gl_int, gl_float)
uniform2f = procedure('glUniform2f', None, gl_int, gl_float, gl_float)
uniform3f = procedure('glUniform3f', None, gl_int, gl_float, gl_float, gl_float)
uniform4f = procedure('glUniform4f', None, gl_int, gl_float, gl_float, gl_float, gl_float)
uniform1i = procedure('glUniform1i', None, gl_int, gl_int)
uniform2i = procedure('glUniform2i', None, gl_int, gl_int, gl_int)
uniform3i = procedure('glUniform3i', None, gl_int, gl_int, gl_int, gl_int)
uniform4i = procedure('glUniform4i', None, gl_int, gl_int, gl_int, gl_int, gl_int)

# these are raw, unlike in webgl. They could get anything at all.
uniform1fv = procedure('glUniform1fv', None, gl_int, gl_long, POINTER(gl_float))
uniform2fv = procedure('glUniform2fv', None, gl_int, gl_long, POINTER(gl_float))
uniform3fv = procedure('glUniform3fv', None, gl_int, gl_long, POINTER(gl_float))
uniform4fv = procedure('glUniform4fv', None, gl_int, gl_long, POINTER(gl_float))
uniform1iv = procedure('glUniform1iv', None, gl_int, gl_long, POINTER(gl_int))
uniform2iv = procedure('glUniform2iv', None, gl_int, gl_long, POINTER(gl_int))
uniform3iv = procedure('glUniform3iv', None, gl_int, gl_long, POINTER(gl_int))
uniform4iv = procedure('glUniform4iv', None, gl_int, gl_long, POINTER(gl_int))
uniformMatrix2fv = procedure('glUniformMatrix2fv', None, gl_int, gl_long, gl_bool, POINTER(gl_float))
uniformMatrix3fv = procedure('glUniformMatrix3fv', None, gl_int, gl_long, gl_bool, POINTER(gl_float))
uniformMatrix4fv = procedure('glUniformMatrix4fv', None, gl_int, gl_long, gl_bool, POINTER(gl_float))
vertexAttrib1f = procedure('glVertexAttrib1f', None, gl_int, gl_float)
vertexAttrib2f = procedure('glVertexAttrib2f', None, gl_int, gl_float)
vertexAttrib3f = procedure('glVertexAttrib3f', None, gl_int, gl_float)
vertexAttrib4f = procedure('glVertexAttrib4f', None, gl_int, gl_float)
vertexAttrib1fv = procedure('glVertexAttrib1fv', None, gl_int, POINTER(gl_float))
vertexAttrib2fv = procedure('glVertexAttrib2fv', None, gl_int, POINTER(gl_float))
vertexAttrib3fv = procedure('glVertexAttrib3fv', None, gl_int, POINTER(gl_float))
vertexAttrib4fv = procedure('glVertexAttrib4fv', None, gl_int, POINTER(gl_float))
vertexAttribPointer = procedure('glVertexAttribPointer', None, gl_uint, gl_int, gl_enum, gl_bool, gl_long, gl_long)

# texture objects
activeTexture = procedure('glActiveTexture', None, gl_enum)
bindTexture = procedure('glBindTexture', None, gl_enum, gl_object)
copyTexImage2D = procedure('glCopyTexImage2D', None, gl_enum, gl_int, gl_enum, gl_int, gl_int, gl_long, gl_long, gl_int)
copyTexSubImage2D = procedure('glCopyTexSubImage2D', None, gl_enum, gl_int, gl_int, gl_int, gl_int, gl_int, gl_long, gl_long)
raw_GenTextures = procedure('glGenTextures', None, gl_long, POINTER(gl_object))
def createTexture():
    obj = gl_object()
    raw_GenTextures(1, byref(obj))
    return obj
raw_DeleteTextures = procedure('glDeleteTextures', None, gl_long, POINTER(gl_object))
def deleteTexture(obj):
    raw_DeleteTextures(1, byref(obj))
generateMipmap = procedure('glGenerateMipmap', None, gl_enum)
isTexture = procedure('glIsTexture', gl_bool, gl_object)
#missing: getTexParameter (problem: hardly needed)
texImage2D = procedure('glTexImage2D', None, gl_enum, gl_int, gl_int, gl_long, gl_long, gl_int, gl_enum, gl_enum, gl_data)
texSubImage2D = procedure('glTexSubImage2D', None, gl_enum, gl_int, gl_int, gl_int, gl_long, gl_long, gl_enum, gl_enum, gl_data)
raw_TexParameterf = procedure('glTexParameterf', None, gl_enum, gl_enum, gl_float)
raw_TexParameteri = procedure('glTexParameteri', None, gl_enum, gl_enum, gl_int)
def texParameter(target, pname, param):
    if isinstance(param, float):
        raw_TexParameterf(target, pname, param)
    else:
        raw_TexParameteri(target, pname, param)

# write to the draw buffer
drawArrays = procedure('glDrawArrays', None, gl_enum, gl_int, gl_long)
drawElements = procedure('glDrawElements', None, gl_enum, gl_long, gl_enum, gl_long)

# special functions
disable = procedure('glDisable', None, gl_enum)
enable = procedure('glEnable', None, gl_enum)
isEnabled = procedure('glIsEnabled', gl_bool, gl_enum)
finish = procedure('glFinish', None)
flush = procedure('glFlush', None)
getError = procedure('glGetError', gl_enum)
hint = procedure('glHint', None, gl_enum, gl_enum)

#missing: getParameter (problem: could return almost anything at all)
#missing: pixelStorei (problem: very different from opengl version)

# renderbuffer objects
bindRenderbuffer = procedure('glBindRenderbuffer', None, gl_enum, gl_object)
raw_GenRenderbuffers = procedure('glGenRenderbuffers', None, gl_long, POINTER(gl_object))
def createRenderbuffer():
    obj = gl_object()
    raw_GenRenderbuffers(1, byref(obj))
    return obj
raw_DeleteRenderbuffers = procedure('glDeleteRenderbuffers', None, gl_long, POINTER(gl_object))
def deleteRenderbuffer(obj):
    raw_DeleteRenderbuffers(1, byref(obj))
isRenderbuffer = procedure('glIsRenderbuffer', gl_bool, gl_object)
raw_GetRenderbufferParameteriv = procedure('glGetRenderbufferParameteriv', None, gl_enum, gl_enum, gl_enum, POINTER(gl_int))
def getRenderbufferParameter(target, attachment, pname):
    out = gl_int()
    raw_GetRenderbufferParameteriv(target, attachment, pname, byref(out))
    return out.value
renderbufferStorage = procedure('glRenderbufferStorage', None, gl_enum, gl_enum, gl_long,  gl_long)


#missing: readPixels (problem: slightly useless)

# framebuffer objects
bindFramebuffer = procedure('glBindFramebuffer', None, gl_enum, gl_object)
checkFramebufferStatus = procedure('glCheckFramebufferStatus', gl_enum, gl_enum)
raw_GenFramebuffers = procedure('glGenFramebuffers', None, gl_long, POINTER(gl_object))
def createFramebuffer():
    obj = gl_object()
    raw_GenFramebuffers(1, byref(obj))
    return obj
raw_DeleteFramebuffers = procedure('glDeleteFramebuffers', None, gl_long, POINTER(gl_object))
def deleteFramebuffer(obj):
    raw_DeleteFramebuffers(1, byref(obj))
isFramebuffer = procedure('glIsFramebuffer', gl_bool, gl_object)
framebufferRenderbuffer = procedure('glFramebufferRenderbuffer', None, gl_enum, gl_enum, gl_enum, gl_object)
framebufferTexture2D = procedure('glFramebufferTexture2D', None, gl_enum, gl_enum, gl_enum, gl_object, gl_int)
raw_GetFramebufferAttachmentParameteriv = procedure('glGetFramebufferAttachmentParameteriv', None, gl_enum, gl_enum, gl_enum, POINTER(gl_int))
def getFramebufferAttachmentParameter(target, attachment, pname):
    out = gl_int()
    raw_GetFramebufferAttachmentParameteriv(target, attachment, pname, byref(out))
    return out.value

# utility functions
def floats(data):
    return (gl_float*len(data))(*data)

def uniformVec3(location, vec3):
    uniform3f(location, *vec3)

def uniformVec4(location, vec4):
    uniform4f(location, *vec4)

def uniformMat3(location, mat3):
    uniformMatrix3fv(location, 1, FALSE, floats(mat3))

def uniformMat4(location, mat4):
    uniformMatrix4fv(location, 1, FALSE, floats(mat4))
