from app.core.translator import Translator
from app.utils import load_di_parameters
from app.models.entities import User


def test_load_di_parameters():
    def test_method(any_param, translator: Translator, extra_value: str, user: User):
        pass

    parameters = load_di_parameters(test_method, extra_value="a string value")
    assert isinstance(parameters["translator"], Translator)
    assert isinstance(parameters["user"], User)
    assert isinstance(parameters["extra_value"], str)
    assert parameters["extra_value"] == "a string value"
