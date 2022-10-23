import datetime
from pathlib import Path
import logging

from pynubank import Nubank
from jwt import decode
from getpass import getpass


def create_token_file(path: Path):
    with path.open("w", encoding="utf-8") as f:
        f.write("")


def authenticate(nu: Nubank):
    logger = logging.getLogger(__name__)
    resources_path = (Path(__file__).resolve().parent / "resources/")
    resources_path.mkdir(parents=True, exist_ok=True)
    token_file_path = resources_path / "refreshToken.txt"
    if not token_file_path.exists():
        create_token_file(token_file_path)
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
