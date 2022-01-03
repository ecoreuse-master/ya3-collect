# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from unittest import TestCase
from datetime import datetime

from ya3_collect import dataframe, exceptions


class TestDataFrame_new(TestCase):

    def setUp(self) -> None:
        self.df = dataframe.DataFrame.new()

    def test_aID(self) -> None:
        self.assertEqual(self.df.columns[0], "aID")

    def test_title(self) -> None:
        self.assertEqual(self.df.columns[1], "title")

    def test_datetime(self) -> None:
        self.assertEqual(self.df.columns[2], "datetime")

    def test_access(self) -> None:
        self.assertEqual(self.df.columns[3], "access")

    def test_watch(self) -> None:
        self.assertEqual(self.df.columns[4], "watch")

    def test_bid(self) -> None:
        self.assertEqual(self.df.columns[5], "bid")


class TestDataFrame_check_format(TestCase):

    def setUp(self) -> None:
        self.df = dataframe.DataFrame.new()

    def test_aID(self) -> None:
        self.assertEqual(self.df.columns[0], "aID")
        del self.df["aID"]
        with self.assertRaises(exceptions.InvalidFormatError):
            self.df.check_format()

    def test_title(self) -> None:
        self.assertEqual(self.df.columns[1], "title")
        del self.df["title"]
        with self.assertRaises(exceptions.InvalidFormatError):
            self.df.check_format()

    def test_datetime(self) -> None:
        self.assertEqual(self.df.columns[2], "datetime")
        del self.df["datetime"]
        with self.assertRaises(exceptions.InvalidFormatError):
            self.df.check_format()

    def test_access(self) -> None:
        self.assertEqual(self.df.columns[3], "access")
        del self.df["access"]
        with self.assertRaises(exceptions.InvalidFormatError):
            self.df.check_format()

    def test_watch(self) -> None:
        self.assertEqual(self.df.columns[4], "watch")
        del self.df["watch"]
        with self.assertRaises(exceptions.InvalidFormatError):
            self.df.check_format()

    def test_bid(self) -> None:
        self.assertEqual(self.df.columns[5], "bid")
        del self.df["bid"]
        self.df["foo"] = None
        with self.assertRaises(exceptions.InvalidFormatError):
            self.df.check_format()


class TestDataFrame_add_record(TestCase):

    def setUp(self) -> None:
        self.record = dataframe.Record(
            aID="10000000",
            title="title",
            datetime=datetime(2021, 1, 1, 0, 0, 0),
            access=10,
            watch=3,
            bid=1
        )
        self.df = dataframe.DataFrame.new()

    def test_aID(self) -> None:
        self.assertEqual(len(self.df["aID"]), 0)
        df = self.df.add_record(self.record)
        self.assertEqual(df["aID"][0], self.record.aID)

    def test_title(self) -> None:
        self.assertEqual(len(self.df["title"]), 0)
        df = self.df.add_record(self.record)
        self.assertEqual(df["title"][0], self.record.title)

    def test_datetime(self) -> None:
        self.assertEqual(len(self.df["datetime"]), 0)
        df = self.df.add_record(self.record)
        self.assertEqual(df["datetime"][0], self.record.datetime.isoformat(timespec="seconds"))

    def test_access(self) -> None:
        self.assertEqual(len(self.df["access"]), 0)
        df = self.df.add_record(self.record)
        self.assertEqual(df["access"][0], self.record.access)

    def test_watch(self) -> None:
        self.assertEqual(len(self.df["watch"]), 0)
        df = self.df.add_record(self.record)
        self.assertEqual(df["watch"][0], self.record.watch)

    def test_bid(self) -> None:
        self.assertEqual(len(self.df["bid"]), 0)
        df = self.df.add_record(self.record)
        self.assertEqual(df["bid"][0], self.record.bid)


    