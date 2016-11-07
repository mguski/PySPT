# script to add PySPT path to Python search path

import os
import sys
import site
PySPT_path = os.path.dirname(os.path.abspath(__file__))
print("Install PySPT:")
print("  PySPT path: {}".format(PySPT_path))

searchPaths = sys.path

print('\n  Curren search paths: (start)')
for idxPath,iPath in enumerate(searchPaths):
    print("    {}: {}".format(idxPath, iPath))

idxPySPT_path = [idx for idx, path in enumerate(searchPaths) if path == PySPT_path]

print("\n   Found PySPT at {} (0 is local path) \n\n".format(idxPySPT_path))


if len(idxPySPT_path) < 2:
    print("  Adding PySPT path as USER_SITE to sys.path ({}):".format(PySPT_path))
    userSitePath = site.USER_SITE
    if not os.path.exists(userSitePath):
       print('    creating USER_SITE path: {}'.format(userSitePath)) 
       os.makedirs(userSitePath)
   
    with open(userSitePath + '/PySPT.pth', 'w+') as f:
       print('    creating:  {}/PySPT.pth'.format(userSitePath)) 
       f.write(PySPT_path)
    print("\n  PySPT install complete.")
   


#   searchPaths = sys.path

#   print('  Search paths: (end)')
#   for idxPath,iPath in enumerate(searchPaths):
#       print("    {}: {}".format(idxPath, iPath))
else:
   print("  PySPT path already in search path.")
