<!--
Fiche de réalisation professionnelle (modèle pour l'épreuve E5).
Remplace ce qui est entre [crochets], supprime ce commentaire.
-->

# Fiche de réalisation : console de surveillance réseau Vigie

**Étudiant :** [Prénom Nom]
**Formation :** BTS SIO 1re année, option [SLAM ou SISR], [établissement]
**Période :** [mois année] · Durée réelle : [à compléter]

## Cadre

Cas fictif Bergerat-Tournier, distributeur de pièces industrielles de 380 salariés, trois sites
(Lyon Part-Dieu, Saint-Priest, Nantes). Les adresses et les journaux sont inventés.

## Contexte

[Décris la situation avec tes mots : qui est l'organisation, quel est ton rôle de technicien, pourquoi la surveillance des connexions pose problème.]

## Demande

Le responsable informatique veut une console qui lit le journal d'authentification SSH, signale les
adresses qui multiplient les échecs, dit si elles sont internes ou externes, et lui remet un rapport
lisible. Il veut aussi un contrôle des ports ouverts sur un poste, sans toucher au reste du réseau.

## Environnement

Windows 11, Python 3.12 (version embarquée du kit), VS Code, Git et GitHub. Modules de la bibliothèque
standard seulement. Données : `donnees\auth.log` et `donnees\plan-adressage.csv`.

## Réalisation

| Étape | Ce que j'ai fait | Preuve |
|---|---|---|
| V1 | [lecture d'une ligne du journal] | [capture de `verifier.bat V1`] |
| V2 | [détection des rafales d'échecs] | [capture de `verifier.bat V2`] |
| V3 | [classement des adresses selon le plan] | [capture de `verifier.bat V3`] |
| V4 | [test de ports sur 127.0.0.1] | [capture de `verifier.bat V4`] |
| V5 | [rapport HTML] | [capture du rapport] |
| V6 | [règles de pare-feu proposées] | [extrait du rapport] |

## Compétences du bloc 1 mobilisées

- Gérer le patrimoine informatique : [en quoi]
- Répondre aux incidents et aux demandes d'assistance et d'évolution : [en quoi]
- Développer la présence en ligne de l'organisation : [en quoi, ou supprime la ligne]
- Travailler en mode projet : [en quoi]
- Mettre à disposition des utilisateurs un service informatique : [en quoi]
- Organiser son développement professionnel : [en quoi]

## Difficultés et solutions

| Difficulté | Comment je l'ai résolue |
|---|---|
| [une erreur que tu as rencontrée] | [ce que tu as fait] |
| [une autre] | [ce que tu as fait] |

## Bilan

[Ce qui fonctionne, ce qui reste à améliorer, ce que tu as retenu sur la surveillance réseau.]
