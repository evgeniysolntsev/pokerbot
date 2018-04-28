def singleton(cls):
    instance = cls()
    cls.__new__ = cls.__call__ = lambda cls: instance
    cls.__init__ = lambda self: None
    return instance
