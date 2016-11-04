"""
   Copyright 2015-2016 Red Hat, Inc. and/or its affiliates
   and other contributors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import requests

from requests.auth import HTTPBasicAuth


class HawkularAlertsClient:
    """
    Creates new client for Hawkular-Alerts
    """

    def __init__(self, endpoint, tenant, token=None, username=None,
                 password=None, ssl_verify=False):
        self.tenant = tenant
        self.endpoint = endpoint
        self.ssl_verify = ssl_verify
        self.token = token
        self.username = username
        self.password = password

    def _endpoint(self, *args):
        return '/'.join((self.endpoint,) + args)

    def _request_options(self):
        headers = {
            'Hawkular-Tenant': self.tenant,
            'Content-Type':   'application/json',
        }

        if self.token:
            headers.update({
                'Authorization': 'Bearer {0}'.format(self.token)
            })

        if self.username:
            auth = HTTPDigestAuth(self.username, self.password)
        else:
            auth = None

        return {'headers': headers, 'auth': auth, 'verify': self.ssl_verify}

    def create_group(self, group):
        response = requests.post(
            self._endpoint('triggers', 'groups'),
            json=group,
            **self._request_options())
        response.raise_for_status()

    def create_group_conditions(self, group_id, trigger_mode, conditions):
        response = requests.put(
            self._endpoint('triggers', 'groups', group_id, 'conditions',
                           trigger_mode.lower()),
            json=conditions,
            **self._request_options())
        response.raise_for_status()

    def create_group_member(self, member):
        response = requests.post(
            self._endpoint('triggers', 'groups', 'members'),
            json=member,
            **self._request_options())
        response.raise_for_status()
