"""
Envoi de mails via Gmail (SMTP + mot de passe d'application).
"""

import mimetypes
import os
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable, Optional, Union

from .client import get_credentials, get_notify_address, get_smtp_connection


def _build_message(
    to: Union[str, Iterable[str]],
    subject: str,
    body: str,
    from_addr: str,
    html: bool = False,
    attachments: Optional[Iterable[Union[str, Path]]] = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to if isinstance(to, str) else ", ".join(to)

    if html:
        msg.set_content("Ce mail nécessite un client compatible HTML.")
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    for path in attachments or []:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Pièce jointe introuvable : {path}")
        mime_type, _ = mimetypes.guess_type(path.name)
        maintype, subtype = (mime_type or "application/octet-stream").split("/", 1)
        with open(path, "rb") as f:
            msg.add_attachment(
                f.read(), maintype=maintype, subtype=subtype, filename=path.name
            )

    return msg


def send_mail(
    to: Union[str, Iterable[str]],
    subject: str,
    body: str,
    html: bool = False,
    attachments: Optional[Iterable[Union[str, Path]]] = None,
) -> None:
    """
    Envoie un mail à un ou plusieurs destinataires.

    Exemple :
        send_mail("ami@example.com", "Salut", "Ça va ?")
        send_mail(["a@x.com", "b@x.com"], "Rapport", "<b>ok</b>", html=True)
    """
    address, _ = get_credentials()
    msg = _build_message(to, subject, body, from_addr=address, html=html, attachments=attachments)

    with get_smtp_connection() as server:
        server.send_message(msg)


def notify_me(
    subject: str,
    body: str,
    html: bool = False,
    attachments: Optional[Iterable[Union[str, Path]]] = None,
) -> None:
    """
    S'envoie une notif à soi-même (utile pour des scripts/cron/alertes).

    Exemple :
        notify_me("Script terminé", "Le job de sauvegarde s'est bien passé.")
    """
    to = get_notify_address()
    send_mail(to, subject, body, html=html, attachments=attachments)
