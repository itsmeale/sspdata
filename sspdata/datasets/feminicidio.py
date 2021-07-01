from sspdata.base.crawler import BaseCrawler
from sspdata.base.datasets import BaseDataset

DATASET_NAME: str = "feminicidio"
DATASET_EVENT_TARGET: str = "ctl00$cphBody$btnFeminicidio"
MIN_YEAR: int = 2015
MAX_YEAR: int = 2021


def extrair_feminicidios(ano: int, mes: int):
    dataset = BaseDataset(DATASET_NAME, 2015, 2021, DATASET_EVENT_TARGET)
    crawler = BaseCrawler(dataset, ano, mes)
    return crawler.extract_as_dataframe()


if __name__ == "__main__":
    df = extrair_feminicidios(ano=2015, mes=10)
    df.to_csv("aaa.csv")
