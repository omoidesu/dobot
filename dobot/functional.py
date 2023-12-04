class CachedProperty:
    """
    这是个装饰器，作用是把被装饰的方法变成只读的，并且缓存第一次拿到的数据，后面再拿就直接从缓存里拿了
    """
    name = None

    @staticmethod
    def func(instance):
        raise TypeError(
            'Cannot use cached_property instance without calling '
            '__set_name__() on it.'
        )

    def __init__(self, func, name=None):
        self.real_func = func
        self.__doc__ = getattr(func, '__doc__')

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
            self.func = self.real_func
        elif name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


class CachedClass:
    """
    这是一个单例管理装饰器，作用是把被装饰的类变成单例模式
    通过_label参数来区分不同的实例，只有参数中存在_label参数时才会启用单例模式
    注意：这个装饰器只能用在类上，不能用在方法上，且被装饰的类__init__方法中不能有_label参数，否则会被装饰器捕获生成唯一实例
    """

    _instance_dict: dict
    _real_cls: callable

    def __init__(self, cls):
        if type(cls) != type:
            raise TypeError("CachedClass can only decorate class.")
        self._instance_dict = {}
        self._real_cls = cls
        self.__doc__ = getattr(cls, '__doc__')

    def __call__(self, *args, **kwargs):
        _label = kwargs.get("_label", None)
        if _label is None:
            return self._real_cls(*args, **kwargs)
        if _label not in self._instance_dict:
            _instance = self._real_cls(_label)
            self._instance_dict[_label] = _instance
            return _instance
        else:
            return self._instance_dict[_label]
