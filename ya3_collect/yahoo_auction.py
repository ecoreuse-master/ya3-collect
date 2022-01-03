# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from __future__ import annotations
import re
import logging
import dataclasses
import concurrent.futures as cf
from datetime import datetime
from typing import Pattern, Callable, Any

import bs4
import requests


Tags = list[bs4.element.Tag]
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class SellingItemInfo:
    aID: str
    title: str
    seller_name: str
    stock: int
    start_datetime: datetime
    end_datetime: datetime
    refundable: bool
    startprice: str
    timeleft: str
    count_bid: int
    count_access: int
    count_watch: int

    @staticmethod
    def from_soup(soup: bs4.BeautifulSoup) -> SellingItemInfo:
        return SellingItemInfo(
            aID=_get_aID(soup),
            title=_get_title(soup),
            seller_name=_get_seller_name(soup),
            stock=_get_stock(soup),
            start_datetime=_get_start_datetime(soup),
            end_datetime=_get_end_datetime(soup),
            refundable=_get_refundable(soup),
            startprice=_get_startprice(soup),
            timeleft=_get_timeleft(soup),
            count_bid=_get_count_bid(soup),
            count_access=_get_count_access(soup),
            count_watch=_get_count_watch(soup),
        )


def _get_aID(soup: bs4.BeautifulSoup) -> str:
    tags: Tags = list(soup.find_all("dt", text="オークションID"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "ProductDetail__description"})
        if isinstance(tag, bs4.element.Tag):
            return str(tag.text[1:])
    return ""  # pragma: no cover


def _get_title(soup: bs4.BeautifulSoup) -> str:
    tags: Tags = list(soup.find_all("h1", attrs={"class": "ProductTitle__text"}))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        return str(tags[0].text)
    return ""  # pragma: no cover


def _get_seller_name(soup: bs4.BeautifulSoup) -> str:
    pattern: Pattern[str] = re.compile(r"^rsec:seller;slk:slfinfo;")
    tags: Tags = list(soup.find_all("a", attrs={"data-ylk": pattern}))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        return str(tags[0].text)
    return ""  # pragma: no cover


def _get_stock(soup: bs4.BeautifulSoup) -> int:
    tags: Tags = list(soup.find_all("dt", text="個数"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "ProductDetail__description"})
        if isinstance(tag, bs4.element.Tag):
            return int(tag.text[1:])
    return 0  # pragma: no cover


def _from_yahoo_datetime(datetimestr: str) -> datetime:
    year: int = int(datetimestr[:4])
    month: int = int(datetimestr[5:7])
    day: int = int(datetimestr[8:10])
    hour: int = int(datetimestr[13:15])
    minute: int = int(datetimestr[16:18])
    return datetime(year, month, day, hour, minute)


def _get_start_datetime(soup: bs4.BeautifulSoup) -> datetime:
    tags: Tags = list(soup.find_all("dt", text="開始日時"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "ProductDetail__description"})
        if isinstance(tag, bs4.element.Tag):
            return _from_yahoo_datetime(tag.text[1:])
    return datetime(2000, 1, 1)  # pragma: no cover


def _get_end_datetime(soup: bs4.BeautifulSoup) -> datetime:
    tags: Tags = list(soup.find_all("dt", text="終了日時"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "ProductDetail__description"})
        if isinstance(tag, bs4.element.Tag):
            return _from_yahoo_datetime(tag.text[1:])
    return datetime(2000, 1, 1)  # pragma: no cover


def _get_refundable(soup: bs4.BeautifulSoup) -> bool:
    tags: Tags = list(soup.find_all("dt", text="返品"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "ProductDetail__description"})
        if isinstance(tag, bs4.element.Tag):
            return bool(tag.text[1:] != "返品不可")
    return False  # pragma: no cover


def _get_startprice(soup: bs4.BeautifulSoup) -> str:
    tags: Tags = list(soup.find_all("dt", text="開始価格"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "ProductDetail__description"})
        if isinstance(tag, bs4.element.Tag):
            return str(tag.text[1:])
    return ""  # pragma: no cover


def _get_timeleft(soup: bs4.BeautifulSoup) -> str:
    tags: Tags = list(soup.find_all("dt", text="残り時間"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "Count__number"})
        if isinstance(tag, bs4.element.Tag):
            return str(tag.text.splitlines()[0])
    return ""  # pragma: no cover


def _get_count_bid(soup: bs4.BeautifulSoup) -> int:
    tags: Tags = list(soup.find_all("dt", text="入札件数"))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("dd", attrs={"class": "Count__number"})
        if isinstance(tag, bs4.element.Tag):
            return int(tag.text[:-4])
    return 0  # pragma: no cover


def _get_count_access(soup: bs4.BeautifulSoup) -> int:
    tags: Tags = list(soup.find_all("span", {"class": "StatisticsInfo__term--access"}))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("span", attrs={"class": "StatisticsInfo__data"})
        if isinstance(tag, bs4.element.Tag):
            return int(tag.text)
    return 0  # pragma: no cover


def _get_count_watch(soup: bs4.BeautifulSoup) -> int:
    tags: Tags = list(soup.find_all("span", {"class": "StatisticsInfo__term--watch"}))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        tag = tags[0].find_next_sibling("span", attrs={"class": "StatisticsInfo__data"})
        if isinstance(tag, bs4.element.Tag):
            return int(tag.text)
    return 0  # pragma: no cover


def _get_urls(source_url: str, cookies: dict[str, str], pattern: Pattern[str], timeout: int = 60) -> list[str]:
    response: requests.Response = requests.get(source_url, cookies=cookies, timeout=timeout)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, "lxml")
    urls: list[str] = []
    for tag in soup.find_all("a", attrs={"data-ylk": pattern}):
        try:
            urls.append(tag.get("href"))
        except Exception:
            continue
    if next_page_url := _get_next_page_url(soup):
        urls.extend(_get_urls(next_page_url, cookies, pattern, timeout))
    return urls


def _get_next_page_url(soup: bs4.BeautifulSoup) -> str:
    pattern: Pattern[str] = re.compile(r"^rsec:pagination;slk:next;")
    tags: Tags = list(soup.find_all("a", attrs={"data-ylk": pattern}))
    if len(tags) > 0 and isinstance(tags[0], bs4.element.Tag):
        return str(tags[0].get("href", ""))
    return ""


def get_selling_urls(cookies: dict[str, str], timeout: int = 60) -> list[str]:
    url: str = "https://auctions.yahoo.co.jp/openuser/jp/show/mystatus?select=selling"
    pattern: Pattern[str] = re.compile(r"^rsec:itm;slk:tc;")
    return _get_urls(url, cookies, pattern, timeout)


def get_infos(cookies: dict[str, str], timeout: int = 60) -> list[SellingItemInfo]:
    selling_urls: list[str] = get_selling_urls(cookies, timeout=timeout)
    logger.info(f"{len(selling_urls)} items are selling")
    selling_infos: list[SellingItemInfo] = []
    with cf.ThreadPoolExecutor() as executor:
        submit: Callable[[Any], cf.Future[requests.Response]] = lambda url: executor.submit(
            requests.get, url, cookies=cookies, timeout=timeout
        )
        futures: list[cf.Future[requests.Response]] = list(cf.as_completed(submit(url) for url in selling_urls))
    for fut in futures:
        if err := fut.exception():  # pragma: no cover
            logger.error(err, exc_info=True)
            continue
        info: SellingItemInfo = SellingItemInfo.from_soup(
            bs4.BeautifulSoup(fut.result().content, "lxml")
        )
        if info.aID:
            selling_infos.append(info)
    return selling_infos


if __name__ == "__main__":  # pragma: no cover
    import pprint
    import json
    import time

    with open("cookies.json") as f:
        cookies = {cookie["name"]: cookie["value"] for cookie in json.load(f)}
    start = time.time()
    infos = get_infos(cookies)
    pprint.pprint(infos, indent=2)
    print(f"{len(infos)} items, elapsed: {time.time() - start} [s]")
