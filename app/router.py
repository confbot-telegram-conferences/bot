import logging
import traceback
from app.utils import load_di_parameters
from flask.app import Flask
from .injector import injector

logger = logging.getLogger("sentry_sdk")
app = injector.get(Flask)


def router(rule, **options):
    def decorator(f):
        def run():
            parameters = load_di_parameters(f)
            return f(**parameters)

        app.add_url_rule(rule, str(f), run, **options)
        return f

    return decorator


@app.errorhandler(Exception)
def all_exception_handler(error):
    logger.exception(error)
    traceback.print_exc()
    return "bad message"
