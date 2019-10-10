# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
from srdefcon.score import Scorable
import requests
import dateutil.parser
import datetime
import pytz


class Maintenances(Scorable):
    BASE_URL = 'https://api.status.salesforce.com/v1/maintenances'

    def __init__(self):
        self.m = []
        r = requests.get(self.BASE_URL,
                         params=dict(limit=10000, offset=0, startTime=datetime.datetime.utcnow().isoformat()))
        r.raise_for_status()
        raw_data = r.json()
        print("Found %d maintenance rows" % len(raw_data))
        for row in raw_data:
            # print "Found maintenance %r"%row
            self.m.append(Maintenance(row))

    def score(self):
        return sum([i.score() for i in self.m])


class Maintenance(Scorable):
    M_TYPE_SCORES = dict(
        scheduledMaintenance=8,
        emergencyMaintenance=16,
        switch=16,
        release=32,
    )
    M_AVAIL_SCORES = dict(
        unavailable=2,
        readOnly=1,
        available=0,
        availabilityGenerallyAvailableInRead=1,
        availabilityLiveAgentNotAvailable=0.5,
        availabilityChatternowNotAvailable=0.5,
        availabilityIntermittentReadOnly=0.5,
        bulkOrgMigration=0,
        readOnlySiteSwitch=1,
        readOnlyContinuousSiteSwitch=1,
        eMaint=1,
        fullyAvailable=0,
    )
    M_AVAIL_SCORES['availability'] = 0

    def __init__(self, json_data):
        self.m_type = json_data['message']['maintenanceType']
        self.m_avail = json_data['message']['availability']
        self.start = dateutil.parser.parse(json_data['plannedStartTime'])
        self.end = dateutil.parser.parse(json_data['plannedEndTime'])

    def score_mtype(self):
        return self.M_TYPE_SCORES.get(self.m_type, 0)

    def score_avail(self):
        return self.M_AVAIL_SCORES.get(self.m_avail, 0)

    def is_active(self):
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        return self.start < now < self.end

    def score(self):
        if self.is_active():
            return self.score_avail() * self.score_mtype()
        return 0


if __name__ == "__main__":
    m = Maintenances()
    print("Score: {}".format(m.score()))
