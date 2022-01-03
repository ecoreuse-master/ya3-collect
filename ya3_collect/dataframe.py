# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
from __future__ import annotations
import dataclasses
from datetime import datetime
from typing import Any

import pandas as pd

from ya3_collect import exceptions


@dataclasses.dataclass
class Record:
    aID: str
    title: str
    datetime: datetime
    access: int
    watch: int
    bid: int


class DataFrame(pd.DataFrame):  # type: ignore

    def __new__(cls, *args: Any, **kwargs: Any) -> DataFrame:
        self = super(DataFrame, cls).__new__(cls)
        self.__init__(*args, **kwargs)
        self.check_format()
        return self  # type: ignore

    @staticmethod
    def new() -> DataFrame:
        df = DataFrame(columns=["aID", "title", "datetime", "access", "watch", "bid"])
        return df

    def check_format(self) -> None:
        """
        Check dataframe is valid format.

        Raises
        ------
        InvalidFormatError
            Raises when the format is invalid.
        """
        if self.columns[0] != "aID":
            raise exceptions.InvalidFormatError(f"Columns[0] of dataframe should be `aID`, got {self.columns[0]}")

        if self.columns[1] != "title":
            raise exceptions.InvalidFormatError(f"df.colomns[1] should be `title`, got {self.columns[1]}")

        if self.columns[2] != "datetime":
            raise exceptions.InvalidFormatError(f"df.colomns[2] should be `datetime`, got {self.columns[2]}")
        
        if self.columns[3] != "access":
            raise exceptions.InvalidFormatError(f"df.colomns[3] should be `access`, got {self.columns[3]}")
        
        if self.columns[4] != "watch":
            raise exceptions.InvalidFormatError(f"df.colomns[4] should be `watch`, got {self.columns[4]}")
        
        if self.columns[5] != "bid":
            raise exceptions.InvalidFormatError(f"df.colomns[5] should be `bid`, got {self.columns[5]}")

    def add_record(self, record: Record) -> DataFrame:
        df = DataFrame(self.append(pd.DataFrame({
            "aID": [record.aID],
            "title": [record.title],
            "datetime": [record.datetime.isoformat(timespec="seconds")],
            "access": [record.access],
            "watch": [record.watch],
            "bid": [record.bid]
        })))
        return df

