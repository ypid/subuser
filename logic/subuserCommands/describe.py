#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

import pathConfig
#external imports
import optparse,sys
#internal imports
import subuserlib.classes.user,subuserlib.commandLineArguments,subuserlib.resolve

def parseCliArgs(sysargs):
  usage = "usage: subuser %prog describe [subuser|image] SUBUSER(s)/IMAGE(s)"
  description = """Show basic information about a subuser or image: Whether it is installed, what it's permissions are ect.

EXAMPLE:

    $ subuser describe image iceweasel
    <lots of info>

    $ subuser describe subuser iceweasel
"""
  parser = optparse.OptionParser(usage=usage,description=description,formatter=subuserlib.commandLineArguments.HelpFormatterThatDoesntReformatDescription())
  return parser.parse_args(args=sysargs)

def describe(sysargs):
  """
  Describe subusers and images.
  
  >>> import describe #import self

  Describing a subuser prints its permissions.

  >>> describe.describe(["subuser","foo"])
  Subuser: foo
  ------------------
  Progam:
  foo:
   Description: 
   Maintainer: 
   Last update time(version): 0
   Executable: /usr/bin/foo

  Describing an image prints the default permissions for that image.

  >>> describe.describe(["image","foo"])
  foo:
   Description: 
   Maintainer: 
   Last update time(version): 0
   Executable: /usr/bin/foo

  Images can be refered to with their full paths as well.  Even remote images can be described.

  >>> describe.describe(["image","foo@default"])
  foo:
   Description: 
   Maintainer: 
   Last update time(version): 0
   Executable: /usr/bin/foo
  """
  user = subuserlib.classes.user.User()
  (options,args) = parseCliArgs(sysargs)
  if len(args) < 2:
    print("Args: '"+"' '".join(args)+"'")
    print("Wrong number of arguments.")
    #parseCliArgs(["","subuser","describe","--help"])
  elif args[0] == "image":
    for image in args[1:]:
      subuserlib.resolve.resolveImageSource(user,image).describe()
  elif args[0] == "subuser":
    for subuser in  args[1:]:
      try:
        user.getRegistry().getSubusers()[subuser].describe()
      except KeyError:
        sys.exit("Subuser "+subuser+" does not exist.")
  else:
    print("Args: '"+"' '".join(args)+"'")
    print("Option not supported.")

if __name__ == "__main__":
  describe(sys.argv[1:])
