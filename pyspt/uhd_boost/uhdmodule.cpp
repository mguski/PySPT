#include <iostream>
#include <Python.h>
#include <uhd.h>
#include <boost/format.hpp>
#include <complex>


#include <uhd/types/tune_request.hpp>
#include <uhd/utils/thread_priority.hpp>
#include <uhd/utils/safe_main.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/transport/udp_simple.hpp>
#include <uhd/exception.hpp>
#include <uhd/utils/msg.hpp>

// PyString_FromString works only for python2
// py 3?: result = PyUnicode_FromFormat("Hello, %S!", name)
 

using namespace std;

void say_hello(const char* name) {
    cout << "Hello " <<  name << "!\n";
}

void init_usrp(PyObject *self, PyObject * args){

//void init_usrp( PyObject *args){
  // parse arguments
  char *usrpArgs;
  if (!PyArg_ParseTuple(args, "i", &usrpArgs)) {
    cout << "Parsing error \n";  
//    return NULL;
  }
    cout << " gut\n";
//    uhd::usrp::multi_usrp::sptr usrp = uhd::usrp::multi_usrp::make(args);
}




void find_device_old() {
        cout << "laeuft\n";
       uhd::time_spec_t get_data_t0;


  	uhd::device_addr_t hint; //an empty hint discovers all devices
	uhd::device_addrs_t dev_addrs = uhd::device::find(hint);

        cout << dev_addrs[0].to_string() ;
}

PyObject* find_device() {
        cout << "Searching for devices ...\n";

  	uhd::device_addr_t hint; //an empty hint discovers all devices
	uhd::device_addrs_t dev_addrs = uhd::device::find(hint);
//        for (size_t i = 0; i < dev_addrs.size(); i++) {
//            cout << dev_addrs[i].to_pp_string() << endl;
//          }
        
        PyObject *PyDeviceList;
        PyDeviceList = PyList_New(dev_addrs.size());

        for (size_t i = 0; i < dev_addrs.size(); i++) {
         //   PyList_SetItem(PyDeviceList, i,   PyString_FromString(dev_addrs[i].to_string().c_str()));
            PyList_SetItem(PyDeviceList, i,   PyUnicode_FromString(dev_addrs[i].to_string().c_str()));
          }

        return PyDeviceList;
}


// example from https://wiki.python.org/moin/boost.python/ExportingClasses

namespace { // Avoid cluttering the global namespace.

  // A friendly class.
  class uhd_ext
  {
    public:
      uhd_ext(const std::string& country) { this->country = country; }
      void create_usrp(std::string usrp_args){
     //     std::cout << boost::format("Creating the usrp device with: %s...") % usrp_args << std::endl;
          std::cout << "Creating the usrp device with: "  <<  usrp_args << std::endl;
          this->usrp = uhd::usrp::multi_usrp::make(usrp_args);
          std::cout << boost::format("Using Device: %s") % this->usrp->get_pp_string() << std::endl;

       }
      std::string greet() const { return "Hello from " + country; }
    private:
      std::string country;
      uhd::usrp::multi_usrp::sptr usrp;  
  };

  // A function taking a hello object as an argument.
  std::string invite(const uhd_ext& w) {
    return w.greet() + "! Please come soon!";
  }
}


/*

void create_rx_streamer(){

// create streamer
uhd::stream_args_t stream_args("fc32", "sc16");
// 2. Set the channel list, we want 3 streamers coming from channels
//    0, 1 and 2, in that order:
stream_args.channels = boost::assign::list_of(0)(1)(2);
// 3. Set optional args:
stream_args.args["spp"] = "200"; // 200 samples per packet
// Now use these args to create an rx streamer:
// (We assume that usrp is a valid uhd::usrp::multi_usrp)
uhd::rx_streamer::sptr rx_stream = usrp->get_rx_stream(stream_args);

}
*/
/*
namespace { // Avoid cluttering the global namespace.

  // A couple of simple C++ functions that we want to expose to Python.
  std::string greet() { return "hello, world"; }
  int square(int number) { return number * number; }
}
*/
static PyObject *
hello_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;
//    cout << args[0] << "\n"
    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);
}

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/class.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(uhd)
{
// Create the Python type object for our extension class and define __init__ function.
    class_<uhd_ext>("uhd_ext", init<std::string>())
        .def("greet", &uhd_ext::greet)  // Add a regular member function.
        .def("create_usrp", &uhd_ext::create_usrp)
        .def("invite", invite)  // Add invite() as a regular function to the module.
    ;  
    def("say_hello", say_hello);
    def("hello_system", hello_system);
    def("init_usrp", init_usrp);
    def("find_device", find_device);
    // Add regular functions to the module.
//    def("greet", greet);
 //   def("square", square);
}

