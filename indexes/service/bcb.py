from datetime import (
    datetime,
    timedelta)
from json import loads
from pprint import pprint
from urllib.request import urlopen

CODE_IGPM = 189
CODE_INCC = 192
CODE_IPCA = 433

DATE_FORMAT = '%d/%m/%Y'

URL_BASE = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.'


def main():
    getters = {'IGPM': get_last_igpm, 'INCC': get_last_incc, 'IPCA': get_last_ipca}
    data = {index: getter() for index, getter in getters.items()}
    pprint(data)


def get_from_bcb(code, start=None, end=None):
    url = f'{URL_BASE}{code}/dados?formato=json&dataInicial={start}&dataFinal={end}'
    with urlopen(url) as stream:
        ipca_list = stream.read().decode('utf-8')
        ipca_list = loads(ipca_list)
        return ipca_list


def get_last_igpm():
    start, end = _get_three_months_interval()
    return get_from_bcb(CODE_IGPM, start, end)[-1]


def get_last_incc():
    start, end = _get_three_months_interval()
    return get_from_bcb(CODE_INCC, start, end)[-1]


def get_last_ipca():
    start, end = _get_three_months_interval()
    return get_from_bcb(CODE_IPCA, start, end)[-1]


def _get_three_months_interval():
    now = datetime.now()
    three_months_ago = now - timedelta(days=30*3)

    now = now.strftime(DATE_FORMAT)
    three_months_ago = three_months_ago.strftime(DATE_FORMAT)
    return three_months_ago, now


if __name__ == '__main__':
    main()
