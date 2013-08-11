#include "libovrwrapper.h"
#include <OVR.h>

using namespace OVR;

// Ptr<> AddRef'ed, AutoCleaned
bool               bInited = false;
Ptr<DeviceManager> pManager;
Ptr<HMDDevice>     pHMD;
Ptr<SensorDevice>  pSensor;
SensorFusion       pSensorFusion;


LIBOVRWRAPPER_API int OVR_Init()
{
   bInited = false;
   System::Init(Log::ConfigureDefaultLog(LogMask_Regular));

   if (System::IsInitialized())
   {
      int stage = -1;
      while (++stage > -1 && !bInited)
      {
         switch (stage)
         {
            case 0:
               pManager = *DeviceManager::Create();
               if (pManager == NULL)
                  return bInited;
               break;
            case 1:
               pHMD     = *pManager->EnumerateDevices<HMDDevice>().CreateDevice();
               if (pHMD == NULL)
                  return bInited;
               break;
            case 2:
               pSensor = *pHMD->GetSensor();
               if (pSensor == NULL)
                  return bInited;
               break;
            default:
               bInited = true;
               break;
         };
      }
   }

   pSensorFusion.AttachToSensor(pSensor);

   return (bInited?1:0);
}


LIBOVRWRAPPER_API void OVR_Exit()
{
   if (bInited)
   {
      System::Destroy();
   }
}


LIBOVRWRAPPER_API int OVR_QueryHMD(OVR_HMDInfo* refHmdInfo)
{
   if (!bInited)
   {
      return 0;
   }

   HMDInfo src;
   if (pHMD->GetDeviceInfo(&src))
   {
      refHmdInfo->HResolution             = src.HResolution;
        refHmdInfo->VResolution             = src.VResolution;
        refHmdInfo->HScreenSize             = src.HScreenSize;
        refHmdInfo->VScreenSize             = src.VScreenSize;
        refHmdInfo->VScreenCenter           = src.VScreenCenter;
        refHmdInfo->EyeToScreenDistance     = src.EyeToScreenDistance;
        refHmdInfo->LensSeparationDistance  = src.LensSeparationDistance;
        refHmdInfo->InterpupillaryDistance  = src.InterpupillaryDistance;
        refHmdInfo->DistortionK[0]          = src.DistortionK[0];
        refHmdInfo->DistortionK[1]          = src.DistortionK[1];
        refHmdInfo->DistortionK[2]          = src.DistortionK[2];
        refHmdInfo->DistortionK[3]          = src.DistortionK[3];
        refHmdInfo->ChromaAbCorrection[0]   = src.ChromaAbCorrection[0];
        refHmdInfo->ChromaAbCorrection[1]   = src.ChromaAbCorrection[1];
        refHmdInfo->ChromaAbCorrection[2]   = src.ChromaAbCorrection[2];
        refHmdInfo->ChromaAbCorrection[3]   = src.ChromaAbCorrection[3];
        refHmdInfo->DesktopX                = src.DesktopX;
        refHmdInfo->DesktopY                = src.DesktopY;
        memcpy(refHmdInfo->DisplayDeviceName, src.DisplayDeviceName, sizeof(refHmdInfo->DisplayDeviceName));        
   }

   return 1;
}


LIBOVRWRAPPER_API int OVR_Peek(float* yaw, float* pitch, float* roll)
{
   if (!bInited)
   {
      return 0;
   }

   Quatf hmdOrient = pSensorFusion.GetOrientation();
   hmdOrient.GetEulerAngles<Axis_Y, Axis_X, Axis_Z>(yaw, pitch, roll);

   return 1;
}
