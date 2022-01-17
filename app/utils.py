import inspect
from blinker import signal


def is_handler(item):
    from app.core.handler import Handler

    return inspect.isclass(item) and issubclass(item, Handler) and not item is Handler


def load_handlers(handlers):
    items = [getattr(handlers, item) for item in dir(handlers)]
    return [item for item in items if is_handler(item)]


def injector_signal(event_name, listener):
    def wrapper(*args, **kwargs):
        parameters = load_di_parameters(listener, **kwargs)
        return listener(*args, **{**parameters, **kwargs})

    signal(event_name).connect(wrapper, weak=False)


def inject_fuction():
    def decorator(f):
        def run(*args, **kwargs):
            parameters = load_di_parameters(f, update=args[0], context=args[1])
            return f(**{**parameters, **kwargs})

        return run

    return decorator


def load_di_parameters(method, **kwargs):
    from app.injector import injector

    args_spec = inspect.getfullargspec(method)
    values = dict()
    for k, v in args_spec.annotations.items():
        values[k] = kwargs[k] if k in kwargs else injector.get(v)
    return values
