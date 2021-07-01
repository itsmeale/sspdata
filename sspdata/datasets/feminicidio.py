import io
from typing import Dict

import pandas as pd
import requests as req
from bs4 import BeautifulSoup

ENDPOINT: str = "http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx"
ERROR_MESSAGE: str = "Os dados para o período selecionado não podem ser exportados."


def data_dict_build(key_values):
    return {key: value for key, value in key_values}


def get_id_value(input):
    return input.get("id"), input.get("value")


def extract_hidden_form_data(page_text: str) -> Dict:
    soup = BeautifulSoup(page_text, "html.parser")
    hidden_inputs = soup.find_all("input", {"type": "hidden"})
    return data_dict_build([get_id_value(input) for input in hidden_inputs])


def make_request(endpoint, method, data: Dict = None, return_bytes: bool = False):
    with req.Session() as session:
        if method == "POST":
            response = session.post(endpoint, data=data)
        elif method == "GET":
            response = session.get(endpoint)

        if response.status_code == 200:
            page = response.text
            if return_bytes:
                return response.content
            return page, extract_hidden_form_data(page)
        else:
            raise Exception("Error")


def fix_tabs(xls_str):
    return xls_str.replace(r"\t+", r"\t")


def extrair_feminicidios(ano: int, mes: int):
    ano = str(ano - 2000)
    mes = str(mes)
    _, data_dict = make_request(endpoint=ENDPOINT, method="GET")

    data_dict.update({"__EVENTTARGET": "ctl00$cphBody$btnFeminicidio"})
    _, data_dict = make_request(endpoint=ENDPOINT, method="POST", data=data_dict)

    data_dict.update({"__EVENTTARGET": f"ctl00$cphBody$lkAno{ano}"})
    _, data_dict = make_request(endpoint=ENDPOINT, method="POST", data=data_dict)

    data_dict.update({"__EVENTTARGET": f"ctl00$cphBody$lkMes{mes}"})
    _, data_dict = make_request(endpoint=ENDPOINT, method="POST", data=data_dict)

    data_dict.update({"__EVENTTARGET": "ctl00$cphBody$ExportarBOLink"})
    response_text, _ = make_request(
        endpoint=ENDPOINT, method="POST", data=data_dict, return_bytes=False
    )

    if ERROR_MESSAGE in response_text:
        raise Exception(f"{ERROR_MESSAGE}: Ano: 20{ano}, Mês: {mes}")

    xls = fix_tabs(response_text)

    return pd.read_csv(io.StringIO(xls), sep="\t")


if __name__ == "__main__":
    df = extrair_feminicidios(ano=2021, mes=1)
    df.to_csv("teste.csv", index=False)
