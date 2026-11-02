# Fiche de réalisation : console de surveillance réseau Vigie

**Étudiant :** Antonin Degory
**Formation :** BTS SIO 1A, option SISR, ENSITECH Saint-Quentin-en-Yvelines
**Période :** novembre 2026 · Durée réelle : environ 4h

## Cadre

Cas fictif Bergerat-Tournier, distributeur de pièces industrielles de 380 salariés, trois sites
(Lyon Part-Dieu, Saint-Priest, Nantes). Les adresses et les journaux sont inventés.

## Contexte

Bergerat-Tournier distribue des pièces industrielles sur trois sites. Je suis technicien dans le service
informatique. Chaque nuit, des inconnus essaient des mots de passe sur le serveur SSH de l'entrepôt, mais
personne ne lit le journal des connexions : il y a plus de 400 lignes par semaine, c'est illisible à l'œil nu.
Si un attaquant trouve le bon mot de passe, personne ne s'en rend compte.

## Demande

Le responsable informatique veut une console qui lit le journal d'authentification SSH, signale les
adresses qui multiplient les échecs, dit si elles sont internes ou externes, et lui remet un rapport
lisible. Il veut aussi un contrôle des ports ouverts sur un poste, sans toucher au reste du réseau.

## Environnement

macOS (MacBook Pro), Python 3 du Mac, VS Code, Terminal, Git et GitHub. Le kit est prévu pour Windows avec des fichiers `.bat` : sur Mac je les ai remplacés par des commandes `python3` dans le Terminal. Modules de la bibliothèque
standard seulement. Données : `donnees/auth.log` et `donnees/plan-adressage.csv`.

## Réalisation

| Étape | Ce que j'ai fait | Preuve |
|---|---|---|
| V1 | Chaque ligne du journal devient un événement (date, serveur, échec ou succès, IP, compte). Je cherche les mots repères `from`, `for` et `user` pour gérer les lignes « invalid user ». | `python3 vigie/verifier.py V1` : 8 / 8 |
| V2 | Je range les échecs par adresse, puis je cherche la plus grosse série d'échecs en 60 secondes. À partir de 5, c'est une alerte : 5 adresses détectées. | `python3 vigie/verifier.py V2` : 10 / 10 |
| V3 | Je lis le plan d'adressage (CSV de 16 réseaux) et je classe chaque adresse : interne avec son site, interne hors plan, ou externe. | `python3 vigie/verifier.py V3` : 12 / 12 |
| V4 | Je teste 12 ports connus sur ma propre machine uniquement (127.0.0.1) avec un socket et un délai de 0,3 seconde. | `python3 vigie/verifier.py V4` : 5 / 5 |
| V5 | Le rapport HTML donne une décision par adresse (Bloquer, Enquêter, Compromission) et protège les noms de compte avec `html.escape`. | `captures/rapport.png` |
| V6 | Le programme écrit les 4 règles `netsh` pour bloquer les adresses externes, après avoir vérifié chaque adresse. Il ne les exécute pas. | `captures/verifier.png` : 52 / 52 |

## Compétences du bloc 1 mobilisées

- Gérer le patrimoine informatique : utiliser le plan d'adressage de l'entreprise pour savoir à quel site appartient une adresse.
- Répondre aux incidents et aux demandes d'assistance et d'évolution : repérer les attaques dans le journal et proposer une action pour chacune (bloquer, enquêter, réagir en urgence).
- Travailler en mode projet : six étapes, chacune vérifiée par un script, et le code suivi avec Git.
- Mettre à disposition des utilisateurs un service informatique : un rapport lisible pour le responsable, sans avoir à lire le journal.
- Organiser son développement professionnel : ce projet publié sur GitHub dans mon portfolio.

## Difficultés et solutions

| Difficulté | Comment je l'ai résolue |
|---|---|
| Les fichiers `.bat` ne marchent pas sur Mac. | J'ai lancé Python directement dans le Terminal : `python3 vigie/verifier.py V1` et `python3 vigie/main.py`. |
| En V1, le vérificateur affichait toujours les mêmes erreurs alors que j'avais écrit mon code. | Le fichier n'était pas enregistré au bon endroit : j'ai enregistré `vigie/journal.py` (Cmd+S) et relancé. J'avais aussi effacé la ligne `evenements = []`, ce qui aurait provoqué un `NameError` : je l'ai remise. |

## Bilan

Les six étapes fonctionnent (52 / 52 contrôles) et le rapport donne les mêmes résultats que la consigne :
136 échecs, 5 alertes, 4 adresses à bloquer et 1 compromission. Sur Mac, les ports 135 et 445 ne sont pas
ouverts car ce sont des services Windows. À améliorer : la détection ne voit pas un attaquant qui essaie
lentement (une tentative toutes les 90 secondes). J'ai retenu qu'un journal ne sert à rien si personne ne le
lit, et qu'on ne fait jamais confiance à un texte qui vient d'un attaquant.
