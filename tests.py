import pytest
from unittest.mock import patch

from api_mock import MOCK_SAMPLE_REPONSE
from crawler import CrawlerClient
from utils import valid_cpf


def test_crawler_client_init():
    crawler = CrawlerClient(
        login_user='test_set_login_user', login_password='test_set_login_pass',
    )
    assert crawler.login_user == 'test_set_login_user'
    assert crawler.login_password == 'test_set_login_pass'


def test_crawler_client_init_no_credentials():
    # No credentials
    with pytest.raises(Exception):
        CrawlerClient()

    # No password
    with pytest.raises(Exception):
        CrawlerClient(login_user="User")

    # Empty credentials
    with pytest.raises(Exception):
        CrawlerClient(login_user="", login_password="")


@patch.object(CrawlerClient, 'request_login', return_value="")
@patch.object(CrawlerClient, 'request_benefits', return_value=MOCK_SAMPLE_REPONSE)
def test_crawler_full_response(mock_login_value, mock_benefits_value):
    crawler = CrawlerClient(login_user="user", login_password="pass")
    crawler.auth_token = 'mock-token'
    response = crawler.get_benefits(cpf='')

    assert type(response) is dict
    assert 'beneficios' in response
    assert len(response['beneficios']) > 0


@patch.object(CrawlerClient, 'request_login', return_value="")
@patch.object(CrawlerClient, 'request_benefits', return_value=MOCK_SAMPLE_REPONSE)
def test_crawler_simple_response(mock_login_value, mock_benefits_value):
    crawler = CrawlerClient(login_user="user", login_password="pass")
    crawler.auth_token = 'mock-token'
    response = crawler.get_benefits(cpf='', simple=True)

    assert type(response) is list
    assert len(response[0]) > 0


def test_invalid_cpf_with_str():
    invalid_cpf_str = '083.019.725-7A'
    is_valid = valid_cpf(invalid_cpf_str)
    assert is_valid is False
    

def test_valid_cpf_with_ponctuation():
    valid_cpf_with_ponctuation = '083.019.725-72'
    is_valid = valid_cpf(valid_cpf_with_ponctuation)
    assert is_valid is True


def test_valid_cpf_integer():
    valid_cpf_int = '08301972572'
    is_valid = valid_cpf(valid_cpf_int)
    assert is_valid is True
