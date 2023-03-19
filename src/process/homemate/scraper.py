import pdb
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from model.nayose import Nayose
from process.common.scraper import Scraper


class HomemateScraper(Scraper):
    def __init__(self, default_dl_path="", is_headless=False):
        super().__init__(default_dl_path, is_headless)
        self.base_url = "https://www.homemate.co.jp"
        self.liblary_url = "https://www.homemate.co.jp/keyword/"
        self.row_data = []

    def filtering_prefecture(self, record: Nayose):
        select_element = Select(self.find_element(By.ID, "list-city-select2"))
        pref = record.prefecture
        if pref not in [option.text for option in select_element.options]:
            return

        select_element.select_by_visible_text(pref)
        self.wait_presence_of_element_by_cssselector("#beacon img", 1)

    def __get_table_links(self, record: Nayose):
        tmp_elm = self.get_element_by_find("span", class_="m_prpty_result_head_hit")
        total_num = int(re.sub(r"[^\d]+", "", tmp_elm.text))
        if total_num == 0:
            return

        boxes = self.get_elements_by_select("section.m_prpty_box")

        # 出力されたデータの件数が多い場合、地域の選択から絞り込みを行う
        if len(boxes) > 5:
            self.filtering_prefecture(record)

            # 変化したHTMLを再度取得する
            boxes = self.get_elements_by_select("section.m_prpty_box")
            # 絞り込んでもデータ数が多い場合、ブランド名や地域名などのエラーデータの可能性あり
            if len(boxes) > 25:
                return

        search_address = f"{record.prefecture}{record.city}"

        links = []
        for box in boxes:
            box_address = self.get_element_by_select_one(
                "p.m_prpty_maininfo_txt", box
            ).text
            if search_address in box_address:
                link = self.get_element_by_select_one(
                    "div.m_prpty_itemlist_wrap > div.m_prpty_itemlist > div:nth-child(1) a.m_prpty_item_linkarea_btn.kpi_click"
                )["href"]
                links.append(link)

        if links:
            return links

    def __scrape_contents(self):
        # 物件名・階数・物件種別・所在地・アクセス・構造
        ths = self.get_elements_by_select("table th.m_table_ws")
        data_element = [th.find_parent("table") for th in ths]

        ths_in_data = [re.sub(r"[^\w]+", "", d.find("th").text) for d in data_element]
        tds_in_data = [re.sub(r"[^\w]+", "", d.find("td").text) for d in data_element]
        property_dict = dict(zip(ths_in_data, tds_in_data))

        self.row_data.append(property_dict)

    def scrape_homemate(self, record: Nayose):
        self.open_page(f"{self.liblary_url}{record.name}/")
        self.wait_presence_of_element_by_cssselector("#beacon img", 1)

        links = self.__get_table_links(record)

        # 該当するデータが一つもない場合、returnする
        if not links:
            return "not links"

        for link in links:
            self.open_page(url=f"{self.base_url}{link}")
            self.wait_presence_of_element_by_cssselector("#beacon img", 1)
            self.__scrape_contents(record)
