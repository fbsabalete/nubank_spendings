import argparse
import logging
import sys
from pathlib import Path

from pynubank import Nubank, MockHttpClient

from auth import authenticate
from bills import update_bills_data

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO, handlers=[
    logging.FileHandler((Path(__file__).resolve().parent / "debug.log"), mode="w"),
    logging.StreamHandler()
])

logger = logging.getLogger(__name__)


def get_from_nubank(table_path: str):
    nu = Nubank()

    authenticate(nu)

    update_bills_data(nu, table_path)


def mock_nubank(table_path: str):
    nu = Nubank(MockHttpClient())
    # authenticate(nu)
    nu.authenticate_with_cert("1231", "password", "cert.p12")
    update_bills_data(nu, table_path)


def main(args):
    if args.path:
        table_path = str(Path(args.path).resolve().parent)
    else:
        table_path = str(Path(__file__).resolve().parent)

    # get_from_nubank(table_path)
    mock_nubank(table_path)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", "--path", "-p", help="Path to store .xlsx. Parent folder bills/ will be created if needed")
    main(parser.parse_args())
