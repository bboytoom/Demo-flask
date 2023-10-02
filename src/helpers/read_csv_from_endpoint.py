import csv
import socket
import logging
import requests

from io import StringIO


def get_data_from_endpoint(url: str) -> str | None:

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err_http:
        logging.error(f'Error in the endpoint {url} error: {err_http}')

        return None
    except requests.exceptions.ConnectTimeout as err_timeout:
        logging.error(f'Error in the endpoint {url} Timeout  -error: {err_timeout}')

        return None
    except socket.error as err_socket:
        logging.error(
            f'Error in the endpoint {url} Name or service not known - error: {err_socket}')

        return None

    return response.text


def file_data_read_from_csv(url: str) -> dict | None:
    result = {}
    get_file = get_data_from_endpoint(url)

    if not get_file or 'N/D' in get_file:
        return None

    csv_file = StringIO(get_file)
    csv_reader = csv.reader(csv_file)

    for value in list(csv_reader)[1:]:
        result.update({
            'symbol': value[0],
            'date': value[1],
            'time': value[2],
            'open': value[3],
            'high': value[4],
            'low': value[5],
            'close': value[6],
            'volume': value[7]
            })

    return result
