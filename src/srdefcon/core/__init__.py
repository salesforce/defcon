# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause

from .incident import Incidents
from .maintenance import Maintenances
from srdefcon.score import Scorable


class Core(Scorable):
    DEFCON_MIN = {
        5: None,
        4: 0,
        3: 128,
        2: 1024,
        1: 2048,
        0: 4096,
    }

    def score(self):
        return Incidents().score() + Maintenances().score()

    def defcon(self):
        score = self.score()
        if score == 0:
            return 5
        return max([k for k, v in self.DEFCON_MIN.items() if score <= v])

    def instances(self):
        """ Just do incidents for now """
        return Incidents().instances()

    def impact_type(self):
        return Incidents().impact_type()
