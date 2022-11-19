from pynubank import Nubank
from excel_writer import write_excel
from pathlib import Path
import logging


def update_credit_balance_data(nu: Nubank, table_path: str):
    logger = logging.getLogger(__name__)
    credit_balance = nu.get_credit_card_balance()
    logger.info(f"Successful credit card balance request")
    data = get_relevant_balance_data(credit_balance)
    full_path = (Path(table_path) / "credit_balance/balance.xlsx")
    write_excel(data, full_path)


def get_relevant_balance_data(balance: dict):
    return {
        "limit_available": balance["available"] / 100,
    }
