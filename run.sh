#!/bin/bash
# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause

set -e
set -x

cd /home/pi/defcon
export PYTHONPATH="$PYTHONPATH:/home/pi/defcon/src"

/usr/bin/python /home/pi/defcon/src/srdefcon/main.py

exit 0
