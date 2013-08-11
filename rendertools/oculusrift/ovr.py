from ctypes import CDLL, Structure, POINTER, c_uint, c_float, c_int, c_char
from os.path import dirname

lib = CDLL(dirname(__file__)+'/libovrwrapper.so')

class OVR_HMDInfo(Structure):
    _fields_ = [
        ('HResolution', c_uint),
        ('VResolution', c_uint),
        ('HScreenSize', c_float),
        ('VScreenSize', c_float),
        ('VScreenCenter', c_float),
        ('EyeToScreenDistance', c_float),
        ('LensSeparationDistance', c_float),
        ('InterpupillaryDistance', c_float),
        ('DistortionK', c_float*4),
        ('ChromaAbCorrection', c_float*4),
        ('DesktopX', c_int),
        ('DesktopY', c_int),
        ('DisplayDeviceName', c_char*32),
    ]

init = lib.OVR_Init
init.argtypes = []
init.restype = c_int

exit = lib.OVR_Exit
exit.argtypes = []
exit.restype = None

queryHMD = lib.OVR_QueryHMD
queryHMD.argtypes = [POINTER(OVR_HMDInfo)]
queryHMD.restype = c_int

peek = lib.OVR_Peek
peek.argtypes = [POINTER(c_float), POINTER(c_float), POINTER(c_float)]
peek.restype = c_int
