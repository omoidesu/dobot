import copy
import os.path
from functools import wraps
from typing import Union

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
    通过_label参数来区分不同的实例，只有实例化参数中存在_label参数时才会启用单例模式
    注意：这个装饰器只能用在类上，不能用在方法上，且被装饰的类__init__方法中不能有_label参数，否则会被装饰器捕获生成唯一实例

    example:

    @CachedClass
    class Test:
        def __init__(self, test_arg):
            self.test_arg = test_arg

    # 启用单例模式
    test_instance_1 = Test("test_arg", _path_label="label_1")
    test_instance_2 = Test("test_arg", _path_label="label_12345")
    test_instance_3 = Test("test_arg", _path_label="label_1")
    # 不启用单例模式
    test_not_instance = Test("test_arg")

    print(test_instance_1) # <__main__.Test object at 0x0000019008D1A948>
    print(test_instance_2) # <__main__.Test object at 0x0000019008D1D088>
    print(test_instance_3) # <__main__.Test object at 0x0000019008D1A948>
    print(test_not_instance) # <__main__.Test object at 0x0000019008D1D548>

    # 1=3且!=2，说明1和3是同一个实例，2是另一个实例
    """

    _instance_dict: dict
    _real_cls: callable

    def __init__(self, cls):
        if not isinstance(cls, type):
            raise TypeError("CachedClass can only decorate class.")
        self._instance_dict = {}
        self._real_cls = cls
        self.__doc__ = getattr(cls, '__doc__')

    def __instancecheck__(self, other):
        return isinstance(other, self._real_cls)

    def __call__(self, *args, **kwargs):
        _label = kwargs.pop("_label", None)
        if _label is None:
            _label = kwargs.pop("_path_label", None)
            if _label is not None:
                _label = os.path.abspath(_label).replace("\\", '/')
        _args_label_flag = kwargs.pop("_args_label_flag", False)
        if _args_label_flag:
            label_kwargs = copy.deepcopy(kwargs)
            label_kwargs["args"]: tuple = args
            label_kwargs = dict(sorted(label_kwargs.items(), key=lambda x: x[0]))
            _label = str(label_kwargs)
        if _label is None:
            return self._real_cls(*args, **kwargs)
        if _label not in self._instance_dict:
            _instance = self._real_cls(_label)
            self._instance_dict[_label] = _instance
            return _instance
        else:
            return self._instance_dict[_label]


class SingleClass:
    """
    单例装饰器，被装饰的类会变成单例的
    """
    _instance: Union[type, None]
    _real_cls: callable

    def __init__(self, cls):
        if not isinstance(cls, type):
            raise TypeError("CachedClass can only decorate class.")
        self._instance = None
        self._real_cls = cls
        self.__doc__ = getattr(cls, '__doc__')

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._real_cls(*args, **kwargs)
        return self._instance

    def __instancecheck__(self, other):
        return isinstance(other, self._real_cls)


def absolute_path(func):
    @wraps(func)
    def wrapper(self, path):
        if isinstance(path, str):
            _abs_path = os.path.abspath(path)
            _abs_path = _abs_path.replace('\\', '/')
        else:
            _abs_path = path
        return func(self, _abs_path)

    return wrapper


def async_absolute_path(func):
    @wraps(func)
    async def wrapper(self, path):
        if isinstance(path, str):
            _abs_path = os.path.abspath(path)
            _abs_path = _abs_path.replace('\\', '/')
        else:
            _abs_path = path
        return await func(self, _abs_path)

    return wrapper
