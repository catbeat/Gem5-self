#include <iostream>

#include "debug/Hello.hh"
#include "configs/self/helloObject/hello_object.hh"

HelloObject::HelloObject(HelloObjectParams* p)
    :SimObject(p), event([this]{ processEvent(); }, name() + ".event"), \
    myName(params->name), latency(100), timesLeft(10)
{
    DPRINTF(HelloExample, "Created the hello object\n");
    panic_if(!goodbye, "HelloObject must have a non-null GoodbyeObject");
}

HelloObject::startup()
{
    schedule(event, latency);
}

void HelloObject::processEvent()
{
    timesLeft--;
    DPRINTF(Hello, "Hello world! Processing the event! %d left\n", timesLeft);

    if (timesLeft <= 0) {
        DPRINTF(Hello, "Done firing!\n");
        goodbye->sayGoodbye(myName);
    } else {
        schedule(event, curTick() + latency);
    }
}


HelloObject *HelloObjectParams::create()
{
    return new HelloObject(this);
}
