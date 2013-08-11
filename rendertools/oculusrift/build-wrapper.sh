echo remember to build the OculusSDK with -fPIC before trying to compile this.

OVR=$HOME/OculusSDK
BUILD="g++ -I$OVR/LibOVR/Include"
LIB=$OVR/LibOVR/Lib/Linux/Release/x86_64/libovr.a

$BUILD -c -fPIC libovrwrapper.cpp -o libovrwrapper.o
$BUILD -shared libovrwrapper.o $LIB -lXinerama -ludev -o libovrwrapper.so
