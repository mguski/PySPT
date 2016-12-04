#include <iostream>
#include <Python.h>
#include <uhd.h>


#include <uhd/types/tune_request.hpp>
#include <uhd/utils/thread_priority.hpp>
#include <uhd/utils/safe_main.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/transport/udp_simple.hpp>
#include <uhd/exception.hpp>
#include <uhd/utils/msg.hpp>



using namespace std;

void say_hello(const char* name) {
    cout << "Hello " <<  name << "!\n";
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
        uhd::time_spec_t get_data_t0;


  	uhd::device_addr_t hint; //an empty hint discovers all devices
	uhd::device_addrs_t dev_addrs = uhd::device::find(hint);
        for (size_t i = 0; i < dev_addrs.size(); i++) {
            cout << dev_addrs[i].to_pp_string() << endl;
          }
//        cout << dev_addrs[0].to_string() ;
        PyObject *pArgs;
     //   PyTuple_SetItem(pArgs, 0,PyUnicode_FromString(dev_addrs[0].to_string()) );

        PyObject *tuple, *list;

        tuple = Py_BuildValue("(iis)", 1, 2, "three");
        list = Py_BuildValue("[iis]", 1, 2, "three");
     //   Py_XDECREF(list);
        return list;

}


/*
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

*/




#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(hello)
{
    def("say_hello", say_hello);
    def("find_device", find_device);
}
