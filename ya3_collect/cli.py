# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
import logging
import json
from pathlib import Path
from datetime import datetime

import click
import pandas as pd

from ya3_collect import log, dataframe, yahoo_auction


DATAFILE_SUFFIX = ".csv.gz"
COOKIES_FILE = "cookies.json"

logger = logging.getLogger("ya3_collect")
logging.getLogger().setLevel("DEBUG")

@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["critical", "error", "warning", "info", "debug"]),
    default="info",
    help="logging level",
    show_default=True,
)
def main(
    log_level: str
) -> None:
    fomatter = log.Formatter("%(levelprefix)s %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(fomatter)
    handler.setLevel(log_level.upper())
    logging.getLogger("ya3_collect").addHandler(handler)


@main.command()
def login() -> None:
    raise NotImplementedError("This feature will be implemented at v 0.1.0")


@main.command()
def logout() -> None:
    raise NotImplementedError("This feature will be implemented at v 0.1.0")


@main.command()
@click.option(
    "--data-dir",
    type=click.types.Path(),
    default=Path("data"),
    help="directory where data is saved",
    show_default=True
)
def run(
    data_dir: Path
) -> None:
    ###################### temporary implements ############################
    with open(COOKIES_FILE) as f:
        cookies = {cookie["name"]:cookie["value"] for cookie in json.load(f)}
    ########################################################################
    now = datetime.now()
    with log.measure_time():
        selling_infos = yahoo_auction.get_infos(cookies)
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    file = (data_dir / datetime.now().strftime('%Y-%m-%d')).with_suffix(DATAFILE_SUFFIX)
    if file.exists():
        df = dataframe.DataFrame(pd.read_csv(file))
    else:
        df = dataframe.DataFrame.new()
    for info in selling_infos:
        df = df.add_record(
            dataframe.Record(
                aID=info.aID,
                title=info.title,
                datetime=now,
                access=info.count_access,
                watch=info.count_watch,
                bid=info.count_bid
            )
        )
    df.to_csv(file, compression="gzip", index=False)
    logger.info(f"Data is saved as {file.as_posix()}")

