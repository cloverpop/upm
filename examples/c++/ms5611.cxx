/*
 * Author: Henry Bruce <henry.bruce@intel.com>
 * Copyright (c) 2016 Intel Corporation.
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include <iostream>
#include <signal.h>
#include <stdio.h>

#include "ms5611.hpp"
#include "upm_utilities.h"

static int is_running = 0;

void
sig_handler(int signo)
{
    printf("got signal\n");
    if (signo == SIGINT) {
        is_running = 1;
    }
}

//! [Interesting]
int
main(int argc, char** argv)
{
    upm::MS5611 sensor(0);
    signal(SIGINT, sig_handler);

    while (!is_running) {
        int value = sensor.getTemperatureCelsius();
        std::cout << "Temperature = " << value << "C" << std::endl;
        value = sensor.getPressurePa();
        std::cout << "Pressure = " << value << "Pa" << std::endl;
        upm_delay(1);
    }

    std::cout << "exiting application" << std::endl;

    return 0;
}
//! [Interesting]
