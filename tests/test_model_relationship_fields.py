import pytest

from flake8_django.checkers.model_relationship_fields import RELATIONSHIP_FIELDS

from .utils import run_check, error_code_in_result


RELATIONSHIP_FIELDS_TO = ['apps_name.CheckModel', 'CheckModel']
RELATIONSHIP_FIELDS_USER_TO = ['models.User', 'User']

@pytest.mark.parametrize('to', RELATIONSHIP_FIELDS_TO)
@pytest.mark.parametrize('field_type', RELATIONSHIP_FIELDS)
def test_string_binding_is_used(field_type, to):
    code = "field = models.{}(to={})".format(field_type, to)
    result = run_check(code)
    assert error_code_in_result('DJ21', result)


@pytest.mark.parametrize('to', RELATIONSHIP_FIELDS_TO)
@pytest.mark.parametrize('field_type', RELATIONSHIP_FIELDS)
def test_string_binding_is_used_not_raise_an_error(field_type, to):
    code = "field = models.{}(to='{}')".format(field_type, to)
    result = run_check(code)
    assert not error_code_in_result('DJ21', result)


@pytest.mark.parametrize('field_type', RELATIONSHIP_FIELDS)
def test_function_binding_is_used_not_raise_an_error(field_type):
    code = "field = models.{}(to=get_model())".format(field_type)
    result = run_check(code)
    assert not error_code_in_result('DJ21', result)


@pytest.mark.parametrize('to', RELATIONSHIP_FIELDS_USER_TO)
@pytest.mark.parametrize('field_type', RELATIONSHIP_FIELDS)
def test_get_user_model_is_not_used_is_string(field_type, to):
    code = "field = models.{}(to='{}')".format(field_type, to)
    result = run_check(code)
    assert error_code_in_result('DJ22', result)


@pytest.mark.parametrize('to', RELATIONSHIP_FIELDS_USER_TO)
@pytest.mark.parametrize('field_type', RELATIONSHIP_FIELDS)
def test_get_user_model_is_not_used_is_module(field_type, to):
    code = "field = models.{}(to={})".format(field_type, to)
    result = run_check(code)
    assert error_code_in_result('DJ22', result)


@pytest.mark.parametrize('field_type', RELATIONSHIP_FIELDS)
def test_get_user_is_used(field_type):
    code = "field = models.{}(to=get_user_model())".format(field_type)
    result = run_check(code)
    assert not error_code_in_result('DJ22', result)