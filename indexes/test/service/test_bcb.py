from unittest.mock import patch

from service.bcb import (
    get_last_igpm,
    get_last_incc,
    get_last_ipca)


@patch('service.bcb.get_from_bcb')
def test_get_last_igpm(mock_get_ipca):
    last_igpm = {'data': '01/02/2022', 'valor': '1.83'}
    mock_get_ipca.return_value = [last_igpm]
    assert get_last_igpm() == last_igpm


@patch('service.bcb.get_from_bcb')
def test_get_last_incc(mock_get_ipca):
    last_incc = {'data': '01/01/2022', 'valor': '0.71'}
    mock_get_ipca.return_value = [last_incc]
    assert get_last_incc() == last_incc


@patch('service.bcb.get_from_bcb')
def test_get_last_ipca(mock_get_ipca):
    last_ipca = {'data': '01/01/2022', 'valor': '0.54'}
    mock_get_ipca.return_value = [last_ipca]
    assert get_last_ipca() == last_ipca
