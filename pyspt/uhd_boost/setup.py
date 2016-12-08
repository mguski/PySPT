
from distutils.core import setup
from distutils.extension import Extension
import sys
#reposPath = "/home/mguski/repos/"
#reposPath = "../../../../"
#uhdPath = reposPath + "uhd/host/include/"


if sys.hexversion < 0x030300F0:
    print("Error: c++ wrapper is writen for boost_python-py35")
    sys.exit(0)


uhdPath = '/home/radar/uhd/host/'

setup(name="PackageName",
    ext_modules=[
        Extension("uhd", ["uhdmodule.cpp"],
        include_dirs = ["/home/radar/uhd/host/include", "/home/radar/uhd/host/include/uhd/types", "/home/radar/uhd/host/include/uhd/usrp"  ],
        libraries = ["boost_python-py35", "uhd"],
        library_dirs = [  "/home/radar/repos/uhd/host/build/lib","/home/radar/uhd/host/build/lib","/home/radar/uhd/host/lib", "/home/radar/uhd/host/build/lib/CMakeFiles/"  ])
 ])

