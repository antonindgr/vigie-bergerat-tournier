"""V1 : lire le journal d'authentification SSH.

Le fichier donnees/auth.log est le journal du service SSH des serveurs.
Une ligne de connexion ressemble à ça :

  Oct 27 07:55:42 srv-wms-01 sshd[23688]: Failed password for op-entrepot3 from 10.30.10.58 port 43574 ssh2

Si tu la coupes avec split(), tu obtiens une liste de morceaux numérotés
à partir de 0 :

   0 Oct        1 27          2 07:55:42     3 srv-wms-01   4 sshd[23688]:
   5 Failed     6 password    7 for          8 op-entrepot3 9 from
  10 10.30.10.58  11 port     12 43574       13 ssh2

Quand le compte n'existe pas, la ligne contient deux mots de plus :

  Oct 29 03:12:08 srv-web-01 sshd[2211]: Failed password for invalid user admin from 203.0.113.45 port 50122 ssh2

Le nom du compte n'est alors plus au même endroit (morceau 10 au lieu de 8).
C'est le piège de cette étape : cherche les repères "for", "user" et "from"
plutôt que de compter les positions.

Le journal contient aussi du bruit (déconnexions, sessions PAM, "Invalid user"...).
On ne garde que deux sortes de lignes : "Failed password" et "Accepted".
"""
from outils import lire_date


def parse_ligne(ligne):
    morceaux = ligne.split()
    if len(morceaux) <11:
        return None

    if morceaux[5] == "Failed" and morceaux [6] == "password":
        resultat = "echec"
    elif morceaux[5] == "Accepted":
        resultat = "succes"
    else:
        return None

    ip = morceaux[morceaux.index("from") + 1]

    if "invalid" in morceaux:
        utilisateur = morceaux[morceaux.index("user") +1]
    else:
        utilisateur = morceaux[morceaux.index("for") +1]

    evenement = {
        "date": lire_date(morceaux[0], morceaux[1], morceaux[2]),
        "hote": morceaux[3],
        "resultat": resultat,
        "ip": ip,
        "utilisateur": utilisateur,
    }
    return evenement


def lire_journal(chemin):
  evenements = []
  with open(chemin, encoding="utf-8") as f:
    for ligne in f:
        evenement = parse_ligne(ligne)
        if evenement is not None:
            evenements.append(evenement)
  return evenements
