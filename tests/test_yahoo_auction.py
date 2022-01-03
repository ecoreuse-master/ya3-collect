# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase, mock
from datetime import datetime

import bs4
import requests

from ya3_collect import yahoo_auction


TEST_RESPONSE = requests.Response()
with open("tests/test_yahoo_auction.html", "rb") as f:
    TEST_RESPONSE._content = f.read()
TEST_INFO = yahoo_auction.SellingItemInfo(
    aID="1000000000",
    title="title",
    seller_name="seller_name",
    stock=1,
    start_datetime=datetime(2021, 10, 12, 19, 54),
    end_datetime=datetime(2021, 10, 15, 19, 54),
    refundable=False,
    startprice="10,000 円（税 0 円）",
    timeleft="19時間",
    count_bid=1,
    count_access=10,
    count_watch=10
)


class TestSellingItemInfo_from_soup(TestCase):
    def setUp(self) -> None:
        self.soup = bs4.BeautifulSoup(TEST_RESPONSE.content, "lxml")

    def test_default(self) -> None:
        info = yahoo_auction.SellingItemInfo.from_soup(self.soup)
        self.assertEqual(info, TEST_INFO)



@mock.patch("requests.get", return_value=TEST_RESPONSE)
class Test_get_infos(TestCase):

    @mock.patch("ya3_collect.yahoo_auction.get_selling_urls")
    def test_no_selling_url(
        self,
        get_selling_urls_mock: mock.Mock,
        get_mock: mock.Mock
    ) -> None:
        get_selling_urls_mock.return_value = []
        infos = yahoo_auction.get_infos(dict())
        self.assertEqual(len(infos), 0)

    
    @mock.patch("ya3_collect.yahoo_auction.get_selling_urls")
    def test_3_selling_urls(
        self,
        get_selling_urls_mock: mock.Mock,
        get_mock: mock.Mock
    ) -> None:
        get_selling_urls_mock.return_value = [
            "http://example.com/1",
            "http://example.com/2",
            "http://example.com/3"
        ]
        cookies: dict[str, str] = dict()
        timeout = 60
        infos = yahoo_auction.get_infos(cookies, timeout)
        for i, info in enumerate(infos):
            with self.subTest(i=i):
                self.assertEqual(info, TEST_INFO)
        get_selling_urls_mock.assert_called_once_with(cookies, timeout=timeout)
        self.assertEqual(len(get_mock.mock_calls), len(get_selling_urls_mock.return_value))
