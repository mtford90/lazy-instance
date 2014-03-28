from importlib import import_module


class LazyObjectProxyMeta(type):

    def __instancecheck__(self, instance):
        return object.__getattribute__(self, "_lp_obj").__instancecheck__(instance)

    def __subclasscheck__(self, subclass):
        return object.__getattribute__(self, "_lp_obj").__subclasscheck__(subclass)


# noinspection PyMissingConstructor
class LazyObjectProxy(object):

    __metaclass__ = LazyObjectProxyMeta
    __slots__ = ['_lp_class_name', '_lp_args', '_lp_kwargs', '_lp_obj', '_lazily_instantiate']

    def __init__(self, class_name, *args, **kwargs):
        object.__setattr__(self, "_lp_class_name", class_name)
        object.__setattr__(self, "_lp_args", args)
        object.__setattr__(self, "_lp_kwargs", kwargs)
        object.__setattr__(self, "_lp_obj", None)

    def _lazily_instantiate(self):
        if not object.__getattribute__(self, '_lp_obj'):
            path = object.__getattribute__(self, '_lp_class_name')
            p, m = path.rsplit('.', 1)
            mod = import_module(p)
            module_lp_obj = getattr(mod, m)
            args = object.__getattribute__(self, '_lp_args')
            kwargs = object.__getattribute__(self, '_lp_kwargs')
            object.__setattr__(self, "_lp_obj", module_lp_obj(*args, **kwargs))

    def __getattribute__(self, name):
        object.__getattribute__(self, '_lazily_instantiate')()
        return getattr(object.__getattribute__(self, "_lp_obj"), name)

    def __delattr__(self, name):
        object.__getattribute__(self, '_lazily_instantiate')()
        delattr(object.__getattribute__(self, "_lp_obj"), name)

    def __setattr__(self, name, value):
        object.__getattribute__(self, '_lazily_instantiate')()
        setattr(object.__getattribute__(self, "_lp_obj"), name, value)

    def __nonzero__(self):
        object.__getattribute__(self, '_lazily_instantiate')()
        return bool(object.__getattribute__(self, "_lp_obj"))

    def __str__(self):
        object.__getattribute__(self, '_lazily_instantiate')()
        return str(object.__getattribute__(self, "_lp_obj"))

    def __repr__(self):
        object.__getattribute__(self, '_lazily_instantiate')()
        return repr(object.__getattribute__(self, "_lp_obj"))