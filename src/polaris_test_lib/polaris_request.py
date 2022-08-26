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


class DeleteServiceRequest(CommonLib):

    def __init__(self, namespace_name, service_name):
        self.namespace_name = namespace_name
        self.service_name = service_name

    def get_dict(self):
        return self._format_params(namespace=self.namespace_name, name=self.service_name)


class DeleteServiceInstanceRequest(CommonLib):

    def __init__(self, service_instance_id):
        self.service_instance_id = service_instance_id

    def get_dict(self):
        return self._format_params(id=self.service_instance_id)
