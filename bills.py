from pynubank import Nubank
from excel_writer import write_excel
from pathlib import Path
import logging


def update_bills_data(nu: Nubank, table_path: str):
    logger = logging.getLogger(__name__)
    bills = nu.get_bills()
    logger.info(f"Successful bills request, returned {len(bills)} bills")
    data = list(map(get_relevant_bill_data, bills))
    full_path = (Path(table_path) / "bills/nubank_bills.xlsx")
    write_excel(data, full_path)


def get_relevant_bill_data(bill: dict):
    bill_summary = bill.get("summary", {})
    final_dict = {
        "close_date": bill_summary.get("close_date"),
        "due_date": bill_summary.get("due_date"),
        "total_balance": float(bill_summary.get("total_balance")) / 100,
        "state": bill.get("state")
    }
    return final_dict
