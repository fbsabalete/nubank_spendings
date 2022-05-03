import datetime
from pathlib import Path

import pandas as pd


def write_excel(data, table_path: Path):
    table_path.parent.mkdir(parents=True, exist_ok=True)
    old_table = table_path
    if old_table.exists():
        date_now = datetime.datetime\
            .fromtimestamp(int(old_table.stat().st_mtime)).replace(microsecond=0).isoformat().replace(":", "-")
        old_table.rename(old_table.with_name(f"{old_table.stem}_{date_now}.xlsx"))

    df = pd.DataFrame.from_dict(data)
    df.to_excel(table_path)