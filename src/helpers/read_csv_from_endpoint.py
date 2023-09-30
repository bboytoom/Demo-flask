import logging
import requests


def get_data_from_endpoint(url: str):

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f'Error in the endpoint {url} error: {err}')

        return None

    return response


def file_data_read_from_csv(url: str):
    get_file = get_data_from_endpoint(url)

    if not get_file:
        return None

    return get_file
