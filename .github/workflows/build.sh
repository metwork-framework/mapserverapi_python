#!/bin/bash

set -x

yum -y install metwork-mfext-layer-mapserver
cd /src
/opt/metwork-mfext/bin/mfext_wrapper -- python setup.py install
/opt/metwork-mfext/bin/mfext_wrapper -- pip install -r dev-requirements.txt
/opt/metwork-mfext/bin/mfext_wrapper -- pytest
