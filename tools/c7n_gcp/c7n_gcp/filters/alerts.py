# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
"""
GCP Filter to find Alerts for a Log Metric Filter
"""
from c7n.filters.core import ValueFilter
from c7n.utils import local_session, type_schema
from c7n_gcp.provider import resources as gcp_resources
import jmespath


class AlertsFilter(ValueFilter):
    """GCP Filter to find Alerts for a Log Metric Filter.

    .. code-block:: yaml

      - name: log-metric-filter-has-alert
        resource: gcp.log-project-metric
        filters:
        - type: alerts
    """

    schema = type_schema('alerts')
    required_keys = {}
    permissions = ("monitoring.alertPolicies.list",)

    def process(self, resources, event=None):
        self.findings_list = self.get_findings(resources)
        matched = [r for r in resources if self.process_resource(r)]
        return matched

    def get_findings(self, resources):
        query_params = {
            'pageSize': 1000
        }
        session = local_session(self.manager.session_factory)
        client = session.client("monitoring", "v3", "projects.alertPolicies")
        project = session.get_default_project()
        findings_paged_list = list(client.execute_paged_query('list',
            {'name': 'projects/' + project, **query_params}))
        findings_list = []
        for findings_page in findings_paged_list:
            if findings_page.get('alertPolicies'):
                findings_list.extend(findings_page['alertPolicies'])
        return findings_list

    def process_resource(self, resource):
        resource_name = resource.get('name')
        search_string = "[*].conditions[?contains(conditionThreshold.filter,\
        'metric.type=\"logging.googleapis.com/user/" + resource_name + "\"')]"
        result = jmespath.search(search_string, self.findings_list)

        if not any(result):
            return False
        else:
            return True

    @classmethod
    def register_resources(klass, registry, resource_class):
        resource_class.filter_registry.register('alerts', klass)


gcp_resources.subscribe(AlertsFilter.register_resources)
