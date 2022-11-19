import datetime
from pathlib import Path

import pandas as pd
import logging


def write_excel(data, table_path: Path):
    table_path.parent.mkdir(parents=True, exist_ok=True)
    old_table = table_path
    if type(data) is not list:
        data = list(data.items())

    if old_table.exists():
        date_now = datetime.datetime\
            .fromtimestamp(int(old_table.stat().st_mtime)).replace(microsecond=0).isoformat().replace(":", "-")
        old_table.rename(old_table.with_name(f"{old_table.stem}_{date_now}.xlsx"))

    df = pd.DataFrame.from_dict(data)
    df.to_excel(table_path, index=False)


def write_excel_paginated(data, table_path: Path):
    logger = logging.getLogger(__name__)

    table_path.parent.mkdir(parents=True, exist_ok=True)
    old_table = table_path
    df = pd.DataFrame.from_dict(data)
    if old_table.exists():
        excel_df = pd.read_excel(old_table)
        df = pd.concat([df, excel_df], ignore_index=True).drop_duplicates(keep="last", subset="transactionId")
        logger.info(f"Inserting {len(df.index) - len(excel_df.index)} new transactions")
        date_now = datetime.datetime \
            .fromtimestamp(int(old_table.stat().st_mtime)).replace(microsecond=0).isoformat().replace(":", "-")
        old_table.rename(old_table.with_name(f"{old_table.stem}_{date_now}.xlsx"))

    df.to_excel(table_path, index=False)
