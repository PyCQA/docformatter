#!/bin/bash
#
# Install dependencies on Travis CI.

if [ "$TRAVIS_PYTHON_VERSION" == "2.6" ]
then
    pip --quiet install argparse unittest2
fi
