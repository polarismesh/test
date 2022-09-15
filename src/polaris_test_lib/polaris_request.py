from src.polaris_test_lib.common_lib import CommonLib


class CreateNamespaceRequest(CommonLib):

    def __init__(self, namespace_name, user_id=None, group_id=None, comment=None):
        self.namespace_name = namespace_name
        user_ids = self._check_list(user_id)
        group_ids = self._check_list(group_id)
        self.user_ids = user_ids
        self.group_ids = group_ids
        self.comment = comment

    def get_dict(self):
        return self._format_params(name=self.namespace_name, user_ids=self.user_ids, group_ids=self.group_ids,
                                   comment=self.comment)


class ModifyNamespaceRequest(CommonLib):

    def __init__(self, namespace_name, user_id=None, group_id=None, remove_user_id=None, remove_group_id=None,
                 comment=None):
        self.namespace_name = namespace_name
        user_ids = self._check_list(user_id)
        group_ids = self._check_list(group_id)
        remove_user_ids = self._check_list(remove_user_id)
        remove_group_ids = self._check_list(remove_group_id)
        self.user_ids = user_ids
        self.group_ids = group_ids
        self.remove_user_ids = remove_user_ids
        self.remove_group_ids = remove_group_ids
        self.comment = comment

    def get_dict(self):
        return self._format_params(name=self.namespace_name, user_ids=self.user_ids, group_ids=self.group_ids,
                                   remove_user_ids=self.remove_user_ids, remove_group_ids=self.remove_group_ids,
                                   comment=self.comment)


class DeleteNamespaceRequest(CommonLib):

    def __init__(self, namespace_name):
        self.namespace_name = namespace_name

    def get_dict(self):
        return self._format_params(name=self.namespace_name)


class CreateServiceRequest(CommonLib):

    def __init__(self, service_name, namespace_name, owners, user_id=None, group_id=None, business=None,
                 department=None, comment=None, metadata=None):
        self.service_name = service_name
        self.namespace_name = namespace_name
        self.owners = owners
        self.business = business
        self.department = department
        self.comment = comment
        self.metadata = metadata

        user_ids = self._check_list(user_id)
        group_ids = self._check_list(group_id)
        self.user_ids = user_ids
        self.group_ids = group_ids

    def get_dict(self):
        return self._format_params(name=self.service_name, namespace=self.namespace_name, owners=self.owners,
                                   user_ids=self.user_ids, group_ids=self.group_ids, comment=self.comment,
                                   metadata=self.metadata, business=self.business, department=self.department)


class ModifyServiceRequest(CommonLib):

    def __init__(self, service_name, namespace_name, owners, user_id=None, group_id=None, business=None,
                 department=None, comment=None, metadata=None, remove_user_id=None, remove_group_id=None):
        self.service_name = service_name
        self.namespace_name = namespace_name
        self.owners = owners
        self.business = business
        self.department = department
        self.comment = comment
        self.metadata = metadata

        user_ids = self._check_list(user_id)
        remove_user_ids = self._check_list(remove_user_id)
        group_ids = self._check_list(group_id)
        remove_group_ids = self._check_list(remove_group_id)
        self.user_ids = user_ids
        self.group_ids = group_ids
        self.remove_user_ids = remove_user_ids
        self.remove_group_ids = remove_group_ids

    def get_dict(self):
        return self._format_params(name=self.service_name, namespace=self.namespace_name, owners=self.owners,
                                   user_ids=self.user_ids, group_ids=self.group_ids, comment=self.comment,
                                   remove_user_ids=self.remove_user_ids, remove_group_ids=self.remove_group_ids,
                                   metadata=self.metadata, business=self.business, department=self.department)


class DeleteServiceRequest(CommonLib):

    def __init__(self, namespace_name, service_name):
        self.namespace_name = namespace_name
        self.service_name = service_name

    def get_dict(self):
        return self._format_params(namespace=self.namespace_name, name=self.service_name)


class CreateServiceInstanceRequest(CommonLib):

    def __init__(self, service_name, namespace_name, host, port, weight, healthy, enable_health_check, protocol=None,
                 version=None, metadata=None, health_check=None, isolate=None):
        self.service = service_name
        self.namespace = namespace_name
        self.host = host
        self.port = port
        self.weight = weight
        self.healthy = healthy
        self.enable_health_check = enable_health_check
        if self.enable_health_check:
            if health_check is None:
                raise Exception("You must assign health check way when enabled health check.")
        self.health_check = health_check
        self.protocol = protocol
        self.version = version
        self.isolate = isolate
        self.metadata = metadata

    def get_dict(self):
        return self._format_params(service=self.service, namespace=self.namespace, host=self.host, port=self.port,
                                   weight=self.weight, healthy=self.healthy,
                                   enable_health_check=self.enable_health_check, health_check=self.health_check,
                                   protocol=self.protocol, version=self.version, isolate=self.isolate,
                                   metadata=self.metadata)


class DeleteServiceInstanceRequest(CommonLib):

    def __init__(self, service_instance_id):
        self.service_instance_id = service_instance_id

    def get_dict(self):
        return self._format_params(id=self.service_instance_id)
