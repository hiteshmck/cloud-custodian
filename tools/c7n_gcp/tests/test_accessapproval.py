# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from gcp_common import BaseTest
from googleapiclient.errors import HttpError


class AccessApprovalTest(BaseTest):

    def test_access_approval_disabled(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('access-approval-disabled', project_id)
        p = self.load_policy(
            {'name': 'gcp-access-approval',
             'resource': 'gcp.access-approval'},
            session_factory=factory)

        with self.assertRaises(HttpError) as ex:
            p.run()

        self.assertEqual(ex.exception.reason, 'Requested entity was not found.')

    def test_access_approval_precondition(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('access-approval-precondition', project_id)
        p = self.load_policy(
            {'name': 'gcp-access-approval',
             'resource': 'gcp.access-approval'},
            session_factory=factory)

        with self.assertRaises(HttpError) as ex:
            p.run()

        self.assertEqual(ex.exception.reason, 'Precondition check failed.')

    def test_access_approval_enabled(self):
        project_id = 'cloud-custodian'
        factory = self.replay_flight_data('access-approval-enabled', project_id)
        p = self.load_policy(
            {'name': 'gcp-access-approval',
             'resource': 'gcp.access-approval'},
            session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
