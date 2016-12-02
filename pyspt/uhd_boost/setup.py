
from distutils.core import setup
from distutils.extension import Extension

reposPath = "/home/mguski/repos/"
uhdPath = reposPath + "uhd/host/include/"

setup(name="PackageName",
    ext_modules=[
        Extension("hello", ["hellomodule.cpp"],
        include_dirs = [uhdPath,  uhdPath + 'uhd', uhdPath+'uhd/types', uhdPath+'uhd/usrp'],
        libraries = ["boost_python", reposPath + "uhd/host/lib", "/usr/lib/x86_64-linux-gnu/libpython2.7.a"])
    ])
