# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
from srdefcon.score import Scorable
import requests
import dateutil.parser
import datetime
import pytz


class Incidents(Scorable):
    BASE_URL = 'https://api.status.salesforce.com/v1/incidents'

    def __init__(self):
        self.m = []
        r = requests.get(self.BASE_URL,
                         params=dict(limit=10000, offset=0, startTime=datetime.datetime.utcnow().isoformat()))
        r.raise_for_status()
        raw_data = r.json()
        print("Found %d incidents" % len(raw_data))
        for row in raw_data:
            print("Found incident %r" % row)
            self.m.append(Incident(row))

    def score(self):
        return sum([i.score() for i in self.m])

    def instances(self):
        r = set()
        for m in self.m:
            for i in m.instances:
                r.add(i)
        return r


class Incident(Scorable):
    def __init__(self, json_data):
        self.m_type = json_data['IncidentImpacts']
        self.instances = json_data['instanceKeys']
        # print "Instances {}".format(self.instances)
        self.instance_count = len(self.instances)

        self.impacts = []
        for row in json_data['IncidentImpacts']:
            self.impacts.append(Impacts(row))

    def score(self):
        if self.instance_count == 0:
            return 0
        elif self.instance_count == 1:
            mult = 1
        elif self.instance_count >= 2:
            mult = 2
        else:
            raise ValueError("Unexpected instance count {}".format(self.instance_count))

        return sum([i.score() * mult for i in self.impacts])


class Impacts(Scorable):
    I_IMPACT_TYPE = dict(
        serviceDisruption=2048,
        intermittentPageLoadErrors=1024,
        intermittentLoginErrors=1024,
        performanceDegradation=1024,
        pageLoadDelays=1024,
        slowDataProcessing=1024,
        performanceDegradationAsynchronousProcessingSubset=1024,
        performanceDegradationAsynchronousProcessing=1024,
        disruptionReadOnlySsOverRun=512,
        disruptionReadOnlyInstanceRefreshOverrun=512,
    )

    def __init__(self, json_data):
        self.i_type = json_data['type']
        self.start = dateutil.parser.parse(json_data['startTime'])
        if json_data['endTime'] is None:
            self.end = None
        else:
            self.end = dateutil.parser.parse(json_data['endTime'])

    def is_active(self):
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if self.end is None:
            return self.start < now
        else:
            return self.start < now < self.end

    def score(self):
        if self.is_active():
            return self.I_IMPACT_TYPE.get(self.i_type, 0)
        return 0
