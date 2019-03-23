# this one is important
set(MINT True)
set(UNIX 1)
set(CMAKE_SYSTEM_NAME mint)
set(CMAKE_SYSTEM_PROCESSOR m68k)

#this one not so much
set(CMAKE_SYSTEM_VERSION 1.19)
if (NOT DEFINED TARGET)
  set(TARGET "m68k-atari-${CMAKE_SYSTEM_NAME}")
endif()

# specify the cross compiler
set(CMAKE_C_COMPILER /home/sebilla/mintstd/binary7-package/usr/bin/m68k-atari-mint-gcc)
set(CMAKE_CXX_COMPILER /home/sebilla/mintstd/binary7-package/usr/bin/m68k-atari-mint-g++)

# where is the target environment 
set(CMAKE_SYSROOT /usr/${TARGET}/sys-root)
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
set(CMAKE_SYSTEM_PREFIX_PATH ${CMAKE_SYSROOT}/usr)
set(CMAKE_INCLUDE_PATH ${CMAKE_SYSTEM_PREFIX_PATH}/include)

# search for programs in the build host directories
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# for libraries and headers in the target directories
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_C_IMPLICIT_LINK_DIRECTORIES "${CMAKE_SYSTEM_PREFIX_PATH}/lib")
set(CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES "${CMAKE_SYSTEM_PREFIX_PATH}/lib")

# MiNT does not support shared libs
set_property(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS FALSE)
set(CMAKE_C_LINK_SHARED_LIBRARY )
set(CMAKE_C_LINK_MODULE_LIBRARY )
set(CMAKE_CXX_LINK_SHARED_LIBRARY )
set(CMAKE_CXX_LINK_MODULE_LIBRARY )
set(CMAKE_DL_LIBS "")

# No -fPIC on MiNT
set(CMAKE_C_COMPILE_OPTIONS_PIC "")
set(CMAKE_C_COMPILE_OPTIONS_PIE "")
set(CMAKE_CXX_COMPILE_OPTIONS_PIC "")
set(CMAKE_CXX_COMPILE_OPTIONS_PIE "")

set( KWSYS_LFS_WORKS 0)
set( KWSYS_LFS_WORKS__TRYRUN_OUTPUT "")

# do not pull in the paths for the host
set(__UNIX_PATHS_INCLUDED 1)
