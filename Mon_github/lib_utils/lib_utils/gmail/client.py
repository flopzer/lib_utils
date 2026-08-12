"""
Connexion SMTP à Gmail via un mot de passe d'application.

Comment obtenir un mot de passe d'application :
https://myaccount.google.com/apppasswords
(nécessite la validation en 2 étapes activée sur le compte)
"""

import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


class GmailConfigError(Exception):
    """Levée quand les variables d'environnement gmail sont manquantes."""


def get_credentials() -> tuple[str, str]:
    address = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not address or not app_password:
        raise GmailConfigError(
            "GMAIL_ADDRESS et/ou GMAIL_APP_PASSWORD manquants. "
            "Copie .env.example en .env et remplis les valeurs."
        )
    return address, app_password


def get_notify_address() -> str:
    """Adresse utilisée par notify_me(), avec fallback sur GMAIL_ADDRESS."""
    address, _ = get_credentials()
    return os.getenv("GMAIL_NOTIFY_TO", address)


def get_smtp_connection() -> smtplib.SMTP_SSL:
    address, app_password = get_credentials()
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    server.login(address, app_password)
    return server
