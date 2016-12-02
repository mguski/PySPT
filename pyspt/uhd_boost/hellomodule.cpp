#include <iostream>
#include <Python.h>
#include <uhd/types/device_addr.hpp>
#include <uhd/device.hpp>

using namespace std;

void say_hello(const char* name) {
    cout << "Hello " <<  name << "!\n";
}

void find_device() {
        cout << "laeuft\n";
  	uhd::device_addr_t hint; //an empty hint discovers all devices
//	uhd::device_addrs_t dev_addrs = uhd::device::find(hint);
//        cout << dev_addrs[0].to_string() ;
}

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(hello)
{
    def("say_hello", say_hello);
    def("find_device", find_device);
}
