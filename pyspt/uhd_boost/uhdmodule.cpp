#include <iostream>
#include <Python.h>
#include <uhd.h>
#include <boost/format.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/class.hpp>
#include <boost/python/list.hpp>
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
 

// Converts a C++ vector to a python list
template <class T>
boost::python::list toPythonList(std::vector<T> vector) {
    typename std::vector<T>::iterator iter;
    boost::python::list list;
    for (iter = vector.begin(); iter != vector.end(); ++iter) {
        list.append(*iter);
    }
    return list;
}

template <class T>
std::vector<T> listToVector(boost::python::list input ) {
    std::vector<T> vec(boost::python::len(input)); 
    for (int iElement =0; iElement <= boost::python::len(input); ++iElement) {
        vec[iElement] = input[iElement];
    }
    return vec;
}




using namespace std;

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
  class usrpPython
  {
    public:
//      usrpPython(const std::string& country) { this->country = country; }
      usrpPython(std::string usrp_args){

          std::cout << "Creating the usrp device with: "  <<  usrp_args << std::endl;
          this->usrp = uhd::usrp::multi_usrp::make(usrp_args);
          std::cout << boost::format("Using Device: %s") % this->usrp->get_pp_string() << std::endl;
       }
    int get_nChannels_rx(){    return this->usrp->get_rx_num_channels();  }
    int get_nChannels_tx(){    return this->usrp->get_tx_num_channels();  }


    void set_rate(double rate) {
        this->usrp->set_rx_rate(rate);
        this->usrp->set_tx_rate(rate);
    }
    double get_rate_rx() { return this->usrp->get_rx_rate();}

    boost::python::list send_receive( int nSamples) { 
        //allocate a buffer to use
        std::vector<std::complex<float> > buffer(nSamples);

        //create RX and TX streamers
        uhd::stream_args_t stream_args("fc32"); //complex floats
        uhd::rx_streamer::sptr rx_stream = this->usrp->get_rx_stream(stream_args);
        uhd::tx_streamer::sptr tx_stream = this->usrp->get_tx_stream(stream_args);

        /***************************************************************
         * Issue a stream command some time in the near future
         **************************************************************/
        uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_NUM_SAMPS_AND_DONE);
        stream_cmd.num_samps = buffer.size();
        stream_cmd.stream_now = false;
        stream_cmd.time_spec = this->usrp->get_time_now() + uhd::time_spec_t(0.01);
        rx_stream->issue_stream_cmd(stream_cmd);

        uhd::rx_metadata_t rx_md;
        size_t num_rx_samps = rx_stream->recv( &buffer.front(), buffer.size(), rx_md   );
      
        boost::python::list PyRec;
        PyRec = toPythonList(buffer);
        

        return PyRec;
    }

//    void send( boost::python::list input){
    void send( PyObject* input){

//      std::vector<std::complex<float> > buffer = listToVector(input);
        std::vector<std::complex<float> > buffer(PyObject_Length(input)); 
        for (int iElement =0; iElement <= PyObject_Length(input); ++iElement) {
            buffer[iElement] = std::complex<double>(PyComplex_RealAsDouble(input[iElement]),  PyComplex_ImagAsDouble(input[iElement])); 
        }
        

        //create TX streamer
        uhd::stream_args_t stream_args("fc32"); //complex floats
        uhd::tx_streamer::sptr tx_stream = this->usrp->get_tx_stream(stream_args);

        uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_NUM_SAMPS_AND_DONE);
        stream_cmd.num_samps = buffer.size();
        stream_cmd.stream_now = false;
        stream_cmd.time_spec = this->usrp->get_time_now() + uhd::time_spec_t(0.01);
      
        uhd::tx_metadata_t tx_md;
        tx_md.start_of_burst = true;
        tx_md.end_of_burst = true;
        tx_md.has_time_spec = true;
        tx_md.time_spec = this->usrp->get_time_now() + uhd::time_spec_t(0.01);
        size_t num_tx_samps = tx_stream->send(
            &buffer.front(), buffer.size(), tx_md
        );

        
    }



    boost::python::list receive( int nSamples) { 
        //allocate a buffer to use
        std::vector<std::complex<float> > buffer(nSamples);

        //create RX  streamer
        uhd::stream_args_t stream_args("fc32"); //complex floats
        uhd::rx_streamer::sptr rx_stream = this->usrp->get_rx_stream(stream_args);

        uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_NUM_SAMPS_AND_DONE);
        stream_cmd.num_samps = buffer.size();
        stream_cmd.stream_now = false;
        stream_cmd.time_spec = this->usrp->get_time_now() + uhd::time_spec_t(0.01);
        rx_stream->issue_stream_cmd(stream_cmd);

        uhd::rx_metadata_t rx_md;
        size_t num_rx_samps = rx_stream->recv( &buffer.front(), buffer.size(), rx_md   );
      
        boost::python::list PyRec;
        PyRec = toPythonList(buffer);
        
        return PyRec;
    }





//      std::string greet() const { return "Hello from " + country; }
    private:
//      std::string country;
      uhd::usrp::multi_usrp::sptr usrp;  
  };

  // A function taking a hello object as an argument.
  std::string invite(const usrpPython& w) {
    return  "! Please come soon!";
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

using namespace boost::python;

BOOST_PYTHON_MODULE(uhd)
{
// Create the Python type object for our extension class and define __init__ function.
    class_<usrpPython>("usrp", init<std::string>())
        .def("get_nChannels_rx", &usrpPython::get_nChannels_rx) 
        .def("get_nChannels_tx", &usrpPython::get_nChannels_tx) 
        .def("set_rate", &usrpPython::set_rate)
        .def("get_rate_rx", &usrpPython::get_rate_rx)
        .def("send_receive", &usrpPython::send_receive)
        .def("send", &usrpPython::send)
        .def("receive", &usrpPython::receive)
//        .def("create_usrp", &usrpPython::create_usrp)
//        .def("invite", invite)  // Add invite() as a regular function to the module.
    ;  
//    def("say_hello", say_hello);
//    def("hello_system", hello_system);
//    def("init_usrp", init_usrp);
    def("find_device", find_device);
    // Add regular functions to the module.
//    def("greet", greet);
 //   def("square", square);
}

// OLD STUFF

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


