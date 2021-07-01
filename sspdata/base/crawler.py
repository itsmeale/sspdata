import io
from typing import Dict, List, Tuple

import pandas as pd

from sspdata.base.datasets import BaseDataset
from sspdata.base.requests import make_request

ENDPOINT: str = "http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx"
ERROR_MESSAGE: str = "Os dados para o período selecionado não podem ser exportados."


class BaseCrawler:
    def __init__(
        self, dataset: BaseDataset, extraction_year: int, extraction_month: int
    ):
        self.dataset: BaseDataset = dataset
        self.request_data: Dict = None
        self.extraction_year: int = extraction_year
        self.extraction_month: int = extraction_month
        self.default_pipeline: List[Tuple[str, str]] = [
            ("__EVENTTARGET", self.dataset.event_target),
            ("__EVENTTARGET", f"ctl00$cphBody$lkAno{self.extraction_year-2000}"),
            ("__EVENTTARGET", f"ctl00$cphBody$lkMes{self.extraction_month}"),
            ("__EVENTTARGET", "ctl00$cphBody$ExportarBOLink"),
        ]

    @staticmethod
    def __preprocessing_fix_tabs(response_text: str) -> str:
        return response_text.replace(r"\t+", r"\t")

    def extract_as_dataframe(self):
        if not self.dataset.is_valid_date(self.extraction_year, self.extraction_month):
            raise Exception(
                f"Invalid date: year: {self.extraction_year}, month: {self.extraction_month}"
            )

        response, self.request_data = make_request(endpoint=ENDPOINT, method="GET")

        for step in self.default_pipeline:
            id, value = step
            self.request_data.update({id: value})
            response, self.request_data = make_request(
                endpoint=ENDPOINT, method="POST", data=self.request_data
            )

        processed_response = BaseCrawler.__preprocessing_fix_tabs(response)
        return pd.read_csv(io.StringIO(processed_response), sep="\t")
