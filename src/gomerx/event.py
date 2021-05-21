import collections

__all__ = ['Handler', 'Dispatcher']


class Handler(collections.namedtuple("Handler", ("obj name f"))):
    __slots__ = ()


class Dispatcher(object):
    def __init__(self):
        self._dispatcher_handlers = collections.defaultdict(list)

    def add_handler(self, obj, name, f):
        handler = Handler(obj, name, f)
        self._dispatcher_handlers[name] = handler
        return handler

    def remove_handler(self, name):
        del self._dispatcher_handlers[name]

    def dispatch(self, msg, **kw):
        for name in self._dispatcher_handlers:
            handler = self._dispatcher_handlers[name]
            handler.f(handler.obj, msg)
