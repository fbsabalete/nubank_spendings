import logging
from pathlib import Path

from pynubank import Nubank

from excel_writer import write_excel_paginated


def update_debit_statements_data(nu: Nubank, table_path: str, all_pages: bool = False):
    logger = logging.getLogger(__name__)
    statements = nu.get_account_statements_paginated()
    data = list(map(parse_relevant_data, clear_data(statements["edges"])))
    logger.info(f"Successful statements request, returned {len(statements['edges'])} statements")
    has_next_page = statements["pageInfo"]["hasNextPage"]
    while has_next_page and all_pages:
        cursor = statements['edges'][-1]['cursor']
        statements = nu.get_account_statements_paginated(cursor)
        logger.info(f"Successful statements request, returned {len(statements['edges'])} statements")
        data.extend(list(map(parse_relevant_data, clear_data(statements["edges"]))))
        has_next_page = statements["pageInfo"]["hasNextPage"]
    full_path = (Path(table_path) / "statements/debit_statements.xlsx")
    write_excel_paginated(data, full_path)


def clear_data(statements: list):
    return list(filter(lambda f: f["tags"] is not None and "money-out" in f["tags"] and "payments" not in f["tags"],
                       list(map(lambda s: s["node"], statements))))


def parse_relevant_data(statement: dict):
    return {
        "transactionId": statement.get("id"),
        "postDate": statement.get("postDate"),
        "amount": statement.get("amount"),
        "detail": statement.get("detail"),
    }
