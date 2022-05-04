from pynubank import Nubank
from excel_writer import write_excel
from pathlib import Path
import logging


def update_debit_statements_data(nu: Nubank, table_path: str):
    logger = logging.getLogger(__name__)
    statements = nu.get_account_statements()
    statements = list(filter(lambda x: x["__typename"] in ["DebitPurchaseEvent", "PixTransferOutEvent"], statements))
    logger.info(f"Successful statements request, returned {len(statements)} statements")
    data = list(map(get_relevant_data, statements))
    full_path = (Path(table_path) / "statements/debit_statements.xlsx")
    write_excel(data, full_path)


def get_relevant_data(statement: dict):
    return {
        "postDate": statement.get("postDate"),
        "amount": statement.get("amount"),
        "detail": statement.get("detail"),
    }
