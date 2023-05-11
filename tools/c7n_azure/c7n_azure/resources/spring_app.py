# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n_azure.provider import resources
from c7n_azure.query import ChildResourceManager, ChildTypeInfo
from c7n_azure.utils import ResourceIdParser


@resources.register('spring-app')
class SpringApp(ChildResourceManager):
    """Azure Spring Apps Resource

    :example:

    Returns Spring Apps resources

    .. code-block:: yaml

         policies:
          - name: basic-spring-apps
            resource: azure.spring-app

    """

    class resource_type(ChildTypeInfo):
        doc_groups = ['Compute']

        service = 'azure.mgmt.appplatform'
        client = 'AppPlatformManagementClient'
        enum_spec = ('apps', 'list', None)
        parent_manager_name = 'spring-service-instance'

        default_report_fields = (
            'name',
            'location',
            'resourceGroup'
        )

        @classmethod
        def extra_args(cls, parent_resource):
            return {'resource_group_name': 
                    ResourceIdParser.get_resource_group(parent_resource['id']),
                    'service_name': parent_resource['name']}
