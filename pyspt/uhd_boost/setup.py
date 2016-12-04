
from distutils.core import setup
from distutils.extension import Extension

#reposPath = "/home/mguski/repos/"
#reposPath = "../../../../"
#uhdPath = reposPath + "uhd/host/include/"

uhdPath = '/home/radar/uhd/host/'

setup(name="PackageName",
    ext_modules=[
        Extension("hello", ["hellomodule.cpp"],
        include_dirs = ["/home/radar/uhd/host/include", "/home/radar/uhd/host/include/uhd/types", "/home/radar/uhd/host/include/uhd/usrp"  ],
        libraries = ["boost_python", "uhd"],
        library_dirs = [  "/home/radar/repos/uhd/host/build/lib","/home/radar/uhd/host/build/lib","/home/radar/uhd/host/lib", "/home/radar/uhd/host/build/lib/CMakeFiles/"  ])
 ])

