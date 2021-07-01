from typing import Dict

import requests as req
from bs4 import BeautifulSoup


def data_dict_build(key_values):
    return {key: value for key, value in key_values}


def get_id_value(input):
    return input.get("id"), input.get("value")


def extract_hidden_form_data(page_text: str) -> Dict:
    soup = BeautifulSoup(page_text, "html.parser")
    hidden_inputs = soup.find_all("input", {"type": "hidden"})
    return data_dict_build([get_id_value(input) for input in hidden_inputs])


def make_request(endpoint, method, data: Dict = None):
    with req.Session() as session:
        if method == "POST":
            response = session.post(endpoint, data=data)
        elif method == "GET":
            response = session.get(endpoint)
        else:
            raise Exception(f"Method not supported: {method}")

        if response.status_code == 200:
            page = response.text
            return page, extract_hidden_form_data(page)
        else:
            raise Exception(f"Invalid response status code: {response.status_code}")
