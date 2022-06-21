import pytest

from runtime.src.core.aws_secure_parameters import AWSParameterStore


class FakeSSMClient:
    def __init__(self, parameter_return):
        self._parameter_return = {'Parameter': parameter_return}

    def __call__(self, *args, **kwargs):
        return self

    def get_parameter(self, *args, **kwargs):
        return self._parameter_return


@pytest.fixture
def fake_ssm_client():
    def _fake_ssm_client(parameter_store, parameter_return):
        parameter_store._AWSParameterStore__ssm = FakeSSMClient(parameter_return)
    return _fake_ssm_client


def test_secure_parameter(fake_ssm_client):
    ssm = AWSParameterStore()
    fake_ssm_client(ssm, {'Value': 'asd'})
    assert ssm.get_secure_parameter('name') == 'asd'


def test_no_secure_parameter_no_exist(fake_ssm_client):
    ssm = AWSParameterStore()
    fake_ssm_client(ssm, {})
    assert ssm.get_secure_parameter('name') == ''


def test_not_secure_parameter(fake_ssm_client):
    ssm = AWSParameterStore()
    fake_ssm_client(ssm, {'Value': 'asd'})
    assert ssm.get_not_secure_parameter('name') == 'asd'


def test_not_secure_parameter_no_exist(fake_ssm_client):
    ssm = AWSParameterStore()
    fake_ssm_client(ssm, {})
    assert ssm.get_not_secure_parameter('name') == ''
