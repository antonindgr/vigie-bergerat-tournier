# Vigie, console de surveillance réseau

Outil en Python qui lit le journal de connexions SSH d'un distributeur de pièces industrielles
(cas fictif Bergerat-Tournier), repère les adresses qui attaquent, vérifie les adresses source
contre le plan d'adressage, teste quelques ports de la machine locale et produit un rapport HTML.

Réalisé par Antonin Degory, BTS SIO option SISR 1A(2026-2028), ENSITECH Saint-Quentin-en-Yvelines, novembre 2026.

## Ce que fait l'outil

Chaque nuit, des inconnus essaient des mots de passe sur le serveur SSH de l'entreprise, mais
personne ne lit le journal : il y a trop de lignes. Vigie le lit à notre place et dit quelles adresses
attaquent, d'où elles viennent, et ce qu'il faut faire pour chacune (bloquer, enquêter ou réagir vite
si l'attaquant a réussi à se connecter).

| Étape | Fichier | Ce qu'elle fait |
|---|---|---|
| V1 | `vigie/journal.py` | lit une ligne du journal et la transforme en événement |
| V2 | `vigie/detection.py` | repère les adresses avec au moins 5 échecs en 60 secondes |
| V3 | `vigie/reseau.py` | classe une adresse : interne (et dans quel site), ou externe |
| V4 | `vigie/ports.py` | teste une liste fermée de ports sur 127.0.0.1 uniquement |
| V5 | `vigie/rapport.py` | écrit le rapport HTML avec les alertes |
| V6 | `vigie/pare_feu.py` | propose des règles de pare-feu, en texte, sans les appliquer |

## Captures

![Rapport Vigie](captures/rapport.png)
![Vérification des étapes](captures/verifier.png)

## Lancer le projet

Le kit est prévu pour Windows avec des fichiers `.bat`. J'ai travaillé sur un Mac, où les `.bat`
ne fonctionnent pas : je lance donc Python directement dans le Terminal.

Sur Mac ou Linux (Python 3 installé) :

```
python3 vigie/main.py          # lance le programme, le rapport est écrit dans rapports/
python3 vigie/verifier.py      # vérifie les six étapes
open rapports/rapport.html     # ouvre le rapport (Mac)
```

Sur Windows : copier le dossier `python\` du kit à la racine, puis double-cliquer sur `lancer.bat`
ou `verifier.bat`.

## Organisation du code

Le code est dans le dossier `vigie/`, avec un fichier par étape (de `journal.py` à `pare_feu.py`).
`main.py` lance tout dans l'ordre, et `outils.py` contient les fonctions utilisées partout (dates,
vérification d'une adresse IP). Les données sont dans `donnees/` : le journal `auth.log` et le plan
d'adressage `plan-adressage.csv`. Le rapport est créé dans `rapports/`.

## Choix techniques

- Pour lire une ligne du journal, je la coupe en morceaux avec `split()`. Je ne compte pas les positions :
  je cherche des mots repères. L'IP est juste après `from`, et le compte est après `for`, ou après `user`
  quand la ligne contient « invalid user » (le compte n'existe pas et tout est décalé).
- Pour repérer une attaque, je range d'abord les échecs par adresse IP. Puis, pour chaque échec, je compte
  combien d'échecs suivent dans les 60 secondes et je garde le plus grand nombre. À partir de 5, c'est une
  alerte. Les valeurs 60 et 5 sont dans des constantes, faciles à changer.
- Le nom de compte vient du journal, donc c'est l'attaquant qui le choisit. Un attaquant a utilisé
  `<script>x</script>`, qui est du code pour navigateur. `html.escape` le transforme en simple texte, sinon
  le navigateur l'exécuterait en ouvrant le rapport (attaque XSS).

## Sécurité

- Le test de ports ne vise que `127.0.0.1` : le code refuse toute autre adresse.
- Sonder le réseau d'un tiers sans accord est une infraction (article 323-1 du Code pénal).
- Les règles de pare-feu sont affichées, jamais exécutées.
- Les adresses externes des données sont des adresses de documentation (RFC 5737), pas de vraies machines.

## Tests effectués

| Test | Résultat |
|---|---|
| `python3 vigie/verifier.py` | 52 / 52 contrôles OK, 6 / 6 étapes validées |
| Rapport comparé à la capture de la consigne | 136 échecs, 5 alertes, 4 adresses à bloquer, 1 compromission |
| Un nom d'utilisateur avec des balises HTML | le nom s'affiche comme du texte, rien ne s'exécute |

## Ce que j'ai appris

Ma principale difficulté a été de travailler sur Mac alors que le kit est fait pour Windows : les
fichiers `.bat` ne se lancent pas, j'ai dû les remplacer par des commandes Python dans le Terminal.
J'ai aussi appris des bases de Python : découper une ligne avec `split()`, utiliser des listes et des
dictionnaires, lire un fichier CSV.

## Compétences du référentiel

- Gérer le patrimoine informatique : utiliser le plan d'adressage pour savoir à quel site appartient une adresse.
- Répondre aux incidents : repérer les attaques dans le journal et proposer une action pour chacune.
- Mettre à disposition des utilisateurs un service informatique : un rapport lisible pour le responsable.
- Travailler en mode projet : six étapes, chacune vérifiée, et un dépôt Git.
- Organiser son développement professionnel : ce portfolio sur GitHub.
