# this one is important
set(MINT True)
set(UNIX 1)
set(CMAKE_SYSTEM_NAME mint)
set(CMAKE_SYSTEM_PROCESSOR m68k)

#this one not so much
set(CMAKE_SYSTEM_VERSION 1.19)

# specify the cross compiler
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

# where is the target environment 
set(CMAKE_SYSTEM_PREFIX_PATH /usr)
set(CMAKE_INCLUDE_PATH ${CMAKE_SYSTEM_PREFIX_PATH}/include)
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

include(Platform/UnixPaths)
