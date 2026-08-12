# lib_utils

Boîte à outils perso, réutilisable entre projets.

## Installation (en local, dans un autre projet)

```bash
pip install -e /chemin/vers/lib_utils
# ou si c'est un repo git :
pip install git+https://github.com/toncompte/lib_utils.git
```

## Configuration

```bash
cp .env.example .env
```

Puis remplir `GMAIL_ADDRESS` et `GMAIL_APP_PASSWORD` (mot de passe d'application
généré sur https://myaccount.google.com/apppasswords, nécessite la
validation en 2 étapes activée sur le compte Google).

`GMAIL_NOTIFY_TO` est optionnel : c'est l'adresse utilisée par `notify_me()`.
Si absent, elle prend la valeur de `GMAIL_ADDRESS`.

## Usage

```python
from lib_utils.gmail import send_mail, notify_me

# envoyer un mail à quelqu'un
send_mail("ami@example.com", "Salut", "Ça va ?")

# avec plusieurs destinataires, du HTML, et une pièce jointe
send_mail(
    ["a@x.com", "b@x.com"],
    "Rapport mensuel",
    "<h1>Résultats</h1><p>Tout va bien.</p>",
    html=True,
    attachments=["rapport.pdf"],
)

# s'envoyer une notif à soi-même (pratique en fin de script/cron)
notify_me("Backup terminé", "Le script de sauvegarde s'est bien exécuté.")
```

## Structure

```
lib_utils/
├── lib_utils/
│   ├── __init__.py
│   └── gmail/
│       ├── __init__.py
│       ├── client.py   # connexion SMTP + lecture des credentials
│       └── send.py     # send_mail(), notify_me()
├── .env.example
├── pyproject.toml
└── README.md
```

## Ajouter un nouvel outil

Créer un nouveau dossier à côté de `gmail/` (ex: `lib_utils/db/`), avec son
propre `__init__.py` qui expose les fonctions publiques.
