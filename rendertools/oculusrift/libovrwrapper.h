#define LIBOVRWRAPPER_API extern "C"

//#ifdef LIBOVRWRAPPER_EXPORTS
//   #if defined __cplusplus
//      #define LIBOVRWRAPPER_API extern "C" __declspec(dllexport)
//   #else
//      #define LIBOVRWRAPPER_API __declspec(dllexport)
//   #endif
//#else
//   #if defined __cplusplus
//      #define LIBOVRWRAPPER_API extern "C" __declspec(dllimport)
//   #else
//      #define LIBOVRWRAPPER_API __declspec(dllimport)
//   #endif
//#endif

struct OVR_HMDInfo
{   
   unsigned      HResolution;
   unsigned      VResolution; 
    float         HScreenSize;
   float         VScreenSize;
    float         VScreenCenter;
    float         EyeToScreenDistance;
    float         LensSeparationDistance;
    float         InterpupillaryDistance;
    float         DistortionK[4];
    float         ChromaAbCorrection[4];
    int           DesktopX;
    int           DesktopY;
    char          DisplayDeviceName[32];
};


LIBOVRWRAPPER_API int   OVR_Init();
LIBOVRWRAPPER_API void  OVR_Exit();
LIBOVRWRAPPER_API int   OVR_QueryHMD(struct OVR_HMDInfo* refHmdInfo);
LIBOVRWRAPPER_API int   OVR_Peek(float* yaw, float* pitch, float* roll);
