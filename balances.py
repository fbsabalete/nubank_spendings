
from pynubank import Nubank
from excel_writer import write_excel
from pathlib import Path
import logging


def update_balance_data(nu: Nubank, table_path: str):
    logger = logging.getLogger(__name__)
    balance = nu.get_account_balance()
    logger.info(f"Successful balance request")
    data = [create_balance_dict(balance)]
    full_path = (Path(table_path) / "balances/nubank_balance.xlsx")
    write_excel(data, full_path)


def create_balance_dict(balance):
    final_dict = {
        "balance": balance,
    }
    return final_dict
