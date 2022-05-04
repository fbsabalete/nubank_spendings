import argparse
import logging
import sys
from pathlib import Path

from pynubank import Nubank, MockHttpClient
from balances import update_balance_data
from debit_statements import update_debit_statements_data

from auth import authenticate
from bills import update_bills_data

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO, handlers=[
    logging.FileHandler((Path(__file__).resolve().parent / "debug.log"), mode="w"),
    logging.StreamHandler()
])

logger = logging.getLogger(__name__)


def get_from_nubank(table_path: str, nu: Nubank = Nubank()):

    authenticate(nu)

    update_bills_data(nu, table_path)
    update_debit_statements_data(nu, table_path)
    # update_balance_data(nu, table_path)


def mock_nubank(table_path: str, nu):
    nu = Nubank(MockHttpClient())
    # authenticate(nu)
    nu.authenticate_with_cert("1231", "password", "cert.p12")
    statements = list(filter(lambda x: x["__typename"] == "DebitPurchaseEvent", nu.get_account_statements()))
    logger.info(statements)
    # update_bills_data(nu, table_path)
    # update_balance_data(nu, table_path)


def main(args):
    if args.path:
        table_path = str(Path(args.path).resolve().parent)
    else:
        table_path = str(Path(__file__).resolve().parent)

    if args.mock:
        table_path = str(Path(__file__).resolve().parent)
        mock_nubank(table_path, Nubank(MockHttpClient()))
    else:
        get_from_nubank(table_path)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", "--path", "-p", help="Path to store .xlsx. Parent folder bills/ will be created if needed")
    parser.add_argument("-m", "--mock", "-mock", action='store_true')
    main(parser.parse_args())
