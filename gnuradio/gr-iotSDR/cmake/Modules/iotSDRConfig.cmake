INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_IOTSDR iotSDR)

FIND_PATH(
    IOTSDR_INCLUDE_DIRS
    NAMES iotSDR/api.h
    HINTS $ENV{IOTSDR_DIR}/include
        ${PC_IOTSDR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    IOTSDR_LIBRARIES
    NAMES gnuradio-iotSDR
    HINTS $ENV{IOTSDR_DIR}/lib
        ${PC_IOTSDR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/iotSDRTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(IOTSDR DEFAULT_MSG IOTSDR_LIBRARIES IOTSDR_INCLUDE_DIRS)
MARK_AS_ADVANCED(IOTSDR_LIBRARIES IOTSDR_INCLUDE_DIRS)
