import argparse
import logging
import sys
from pathlib import Path

from pynubank import Nubank, MockHttpClient
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


def get_from_nubank(table_path: str, all_pages: bool, nu: Nubank = Nubank()):
    authenticate(nu)

    update_bills_data(nu, table_path)
    update_debit_statements_data(nu, table_path, all_pages)


def mock_nubank(table_path: str, nu):
    # authenticate(nu)
    nu.authenticate_with_cert("1231", "password", "cert.p12")
    update_bills_data(nu, table_path)
    update_debit_statements_data(nu, table_path)


def main(args):
    logger.info(args.path)
    if args.path:
        table_path = str(Path(args.path).resolve().parent)
    else:
        table_path = str(Path(__file__).resolve().parent)

    if args.mock:
        table_path = str(Path(__file__).resolve().parent)
        mock_nubank(table_path, Nubank(MockHttpClient()))
    else:
        get_from_nubank(table_path, args.all)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", "--path", "-p",
                        help="Path to store .xlsx. Parent folder will be created if needed")
    parser.add_argument("-m", "--mock", "-mock", action='store_true')
    parser.add_argument("-a", "--all", "-all", action='store_true',
                        help="If should request all pages recursively, initial load of data")
    main(parser.parse_args())
