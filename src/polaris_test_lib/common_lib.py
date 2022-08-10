class CommonLib:
    @classmethod
    def _format_params(cls, **kwargs):
        req = {}
        for key, value in kwargs.items():
            if value is not None:
                req.update({key: value})
        return req

    @classmethod
    def _check_list(cls, param):

        convert_param = []
        if param is None:
            param = []
        elif type(param) != list:
            if callable(getattr(param, "get_dict", None)):
                convert_param = [param.get_dict()]
            else:
                param = [param]
        elif type(param) == list:
            for p in param:
                if callable(getattr(p, "get_dict", None)):
                    convert_param.append(p.get_dict())
        return convert_param if convert_param != [] else param
