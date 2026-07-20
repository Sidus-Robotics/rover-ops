#ifndef GPS_TELEM_INIT
#define GPS_TELEM_INIT

#include "events.hpp"
#include "ros_decl.hpp"

SharedPublisher(NavSatFix, gps);
UniquePtr(NavSatFix, navSatFix);
UniquePtr(NavSatStatus, navSatStatus);

SharedTimer(gps);

#endif