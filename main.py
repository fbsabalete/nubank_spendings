import datetime
import logging
import sys
from getpass import getpass
from pathlib import Path

from jwt import decode
import pandas as pd
from pynubank import Nubank, MockHttpClient

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
    bills = nu.get_bills()
    data = list(map(get_relevant_data, bills))
    logger.info(f"Successful bills request, returned {len(data)} bills")
    write_excel(data, table_path)


def authenticate(nu: Nubank):
    resources_path = (Path(__file__).resolve().parent / "resources/")
    resources_path.mkdir(parents=True, exist_ok=True)
    token_file_path = str(resources_path / "refreshToken.txt")
    cert_path = (resources_path / "cert.p12")
    if not cert_path.exists():
        raise AssertionError("cert was not generated, run 'pynubank' first")
    cert_path = str(cert_path)
    with open(token_file_path, "r") as file:
        lines = file.readlines()

    if len(lines) != 0:
        token = lines[0]
        exp = get_exp_from_token(token)
        if exp < datetime.datetime.now():
            print("Refresh token expirado. Faça login.")
            new_token = refresh_credentials(cert_path, nu)
        else:
            new_token = nu.authenticate_with_refresh_token(token, cert_path)
    else:
        print("Refresh Token não encontrado. Faça login.")
        new_token = refresh_credentials(cert_path, nu)

    lines = [new_token]
    logger.info("Updated token successfully")
    with open(token_file_path, "w") as file:
        file.writelines(lines)


def get_exp_from_token(token):
    decoded = decode(token, options={"verify_signature": False})
    exp = datetime.datetime.fromtimestamp(decoded["exp"])
    return exp


def refresh_credentials(cert_path, nu):
    cpf = input("CPF: ")
    pw = getpass("Senha: ")
    new_token = nu.authenticate_with_cert(cpf, pw, cert_path)
    return new_token


def get_relevant_data(bill: dict):
    bill_summary = bill.get("summary", {})
    final_dict = {
        "close_date": bill_summary.get("close_date"),
        "due_date": bill_summary.get("due_date"),
        "total_balance": float(bill_summary.get("total_balance")) / 100,
        "state": bill.get("state")
    }
    return final_dict


def mock_nubank(table_path: str):
    nu = Nubank(MockHttpClient())
    nu.authenticate_with_cert("1231", "password", "cert.p12")
    data = list(map(get_relevant_data, nu.get_bills()))
    write_excel(data, table_path)


def write_excel(data, table_path):
    old_table = Path(table_path)
    if old_table.exists():
        date_now = datetime.datetime.fromtimestamp(int(old_table.stat().st_mtime)).replace(
            microsecond=0).isoformat().replace(":", "-")
        old_table.rename(old_table.with_name("nubank_bills_" + date_now + ".xlsx"))
    df = pd.DataFrame.from_dict(data)
    df.to_excel(table_path)


def main(argv):
    if "-path" not in argv:
        table_path = (Path(__file__).resolve().parent / "bills/nubank_bills.xlsx")
    else:
        table_path = (Path(argv[2]).resolve().parent / "bills/nubank_bills.xlsx")

    table_path.parent.mkdir(parents=True, exist_ok=True)
    table_path_str = str(table_path)
    get_from_nubank(table_path_str)
    # mock_nubank(table_path_str)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

if __name__ == '__main__':
    main(sys.argv)
