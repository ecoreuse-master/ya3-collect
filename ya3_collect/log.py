# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import logging
import copy
import sys
import time
import contextlib
from typing import Callable, Iterator

import click

logger = logging.getLogger(__name__)


class Formatter(logging.Formatter):
    colorize: dict[int, Callable[[str], str]] = {
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"),
        logging.CRITICAL: lambda level_name: click.style(str(level_name), fg="bright_red"),
    }

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy.copy(record)
        levelname = recordcopy.levelname
        seperator = " " * (8 - len(recordcopy.levelname))
        if sys.stderr.isatty():
            if (levelno := getattr(logging, levelname)) in self.colorize:
                levelname = self.colorize[levelno](levelname)
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        return super().formatMessage(recordcopy)


@contextlib.contextmanager
def measure_time() -> Iterator[None]:
    start = time.time()
    try:
        yield
    finally:
        logger.info(f"elapsed: {time.time() - start:.5g} [sec]")