#ifndef __LEARNING_GEM5_HELLO_OBJECT_HH__
#define __LEARNING_GEM5_HELLO_OBJECT_HH__

#include <string>

#include "configs/self/helloObject/goodbye_object.hh"
#include "params/HelloObject.hh"
#include "sim/sim_object.hh"

class HelloObject: public SimObject
{
    public:
        HelloObject(HelloObjectParams *p);

        void startup();

    private:
        void processEvent();
        EventWrapper<HelloObject, &HelloObject::processEvent> event;

        Tick latency;

        int timesLeft;

        const std::string myName;

        GoodbyeObject* goodbye;
};

#endif
