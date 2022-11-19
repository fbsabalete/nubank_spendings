from pynubank import Nubank
from excel_writer import write_excel
from pathlib import Path
import logging


def update_account_balance_data(nu: Nubank, table_path: str):
    logger = logging.getLogger(__name__)
    account_balance = nu.get_account_balance()
    logger.info(f"Successful account balance request")
    data = get_relevant_balance_data(account_balance)
    full_path = (Path(table_path) / "account_balance/balance.xlsx")
    write_excel(data, full_path)


def get_relevant_balance_data(balance: float):
    return {
        "current_balance": balance
    }
