/*---------------------------------------------------------------------\
|                          ____ _   __ __ ___                          |
|                         |__  / \ / / . \ . \                         |
|                           / / \ V /|  _/  _/                         |
|                          / /__ | | | | | |                           |
|                         /_____||_| |_| |_|                           |
|                                                                      |
\---------------------------------------------------------------------*/

#include <iostream>
#include <fstream>
#include <sstream>
#include "zypp/base/Logger.h"

#include "zypp/ProvideFilePolicy.h"

using std::endl;

///////////////////////////////////////////////////////////////////
namespace zypp
{ /////////////////////////////////////////////////////////////////
  ///////////////////////////////////////////////////////////////////
  //
  //	CLASS NAME : ProvideFilePolicy
  //
  ///////////////////////////////////////////////////////////////////

  bool ProvideFilePolicy::progress( int value ) const
  {
    if ( _progressCB )
      return _progressCB( value );
    return true;
  }

} // namespace zypp
///////////////////////////////////////////////////////////////////