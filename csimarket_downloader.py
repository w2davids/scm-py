import requests
from bs4 import BeautifulSoup
import pandas as pd


class CSIMarket:
    BASE_URL: str = 'https://csimarket.com/stocks/competition2.php?supply&code='
    TARGET_TABLE_CLASS: str = {'class': "osnovna_tablica_bez_gifa"}

    @classmethod
    def get_symbol(cls, symbol=None):
        return CSIMarket.parse_from_url(CSIMarket.BASE_URL + symbol)

    @classmethod
    def parse_from_url(cls, url=None):
        return CSIMarket.parse(requests.get(url).text)

    @classmethod
    def parse_from_file(cls, html_file=None):
        with open(html_file, encoding="latin-1") as dataFile:
            return CSIMarket.parse(dataFile.read())

    @classmethod
    def parse(cls, contents):
        beautiful_soup = BeautifulSoup(contents, 'lxml')
        html_table = beautiful_soup.find('table', CSIMarket.TARGET_TABLE_CLASS)
        if not html_table : return
        table_rows = []
        for tr_row in html_table.select('tr'):
            row = tr_row.text.strip()
            if not row: pass
            data_row = []
            for td_item in tr_row.select('td'):
                line = td_item.text.strip()
                if not line: pass
                data_row.append(line)
            # Append to table_rows
            table_rows.append(data_row)

        return pd.DataFrame(
            table_rows[1:],
            columns=['COMPANY NAME', 'FISCAL YEAR' ,'TICKER', 'REVENUE', 'NET INCOME', 'NET MARGIN', 'CASH FLOW']
        )


if __name__ == '__main__':
    csi_market = CSIMarket()
    data_frame = csi_market.get_symbol('AAPL')
    print(data_frame)
