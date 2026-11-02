"""V5 : décider quoi faire, et fabriquer le rapport HTML.

Pour chaque alerte, Vigie propose une décision :
  COMPROMISSION  l'attaquant a fini par se connecter : urgence maximale
  BLOQUER        adresse externe qui attaque : on la bloque au pare-feu
  ENQUETER       adresse interne : on ne bloque pas à l'aveugle, on va voir
                 sur place ce qui se passe (poste infecté ? script oublié ?)

Dans ce fichier, tu écris trois petites fonctions (decider, ligne_tableau,
recommandations). La page complète est construite par construire_rapport,
que tu n'as pas à modifier.
"""
import html
import os

from outils import formater_date, DOSSIER_DONNEES

ECOLE = 'ENSITECH · Saint-Quentin-en-Yvelines'

BLOQUER = "BLOQUER"
ENQUETER = "ENQUETER"
COMPROMISSION = "COMPROMISSION"

LIBELLES = {
    BLOQUER: "Bloquer",
    ENQUETER: "Enquêter",
    COMPROMISSION: "Compromission",
}


def decider(classe, compromis):
    """Rend BLOQUER, ENQUETER ou COMPROMISSION pour une alerte."""
    if compromis:
        decision = COMPROMISSION
    elif classe["type"] == "externe":
        decision = BLOQUER
    else:  
        decision = ENQUETER
    return decision
    


def ligne_tableau(alerte, classe, decision):
    """Rend le HTML d'une ligne du tableau des alertes (une balise <tr>)."""
    ip = html.escape(alerte["ip"])
    comptes = html.escape(", ".join(alerte["utilisateurs"]))
    origine = html.escape(classe["type"]) + " (" + html.escape(classe["site"]) + ")"
    debut = formater_date(alerte["debut"])
    fin = formater_date(alerte["fin"])
    ligne = (
        f"<tr><td>{ip}</td><td>{origine}</td><td>{comptes}</td>"
        f"<td>{alerte['nb_echecs']}</td><td>{debut}</td><td>{fin}</td>"
        f'<td><span class="badge {decision}">{LIBELLES[decision]}</span></td></tr>'
    )
    return ligne


def recommandations(decisions):
    """Rend une liste de phrases de recommandation, une par alerte."""
    phrases = []
    for d in decisions:
        ip = d["ip"]
        if d["decision"] == COMPROMISSION:
            phrases.append(f"URGENT : {ip} s'est connectée après son attaque. Changer le mot de passe du compte et fermer les sessions ouvertes.")
        elif d["decision"] == BLOQUER:
            phrases.append(f"Bloquer l'adresse {ip} au pare-feu.")
        else:
            phrases.append(f"Enquêter : aller vérifier sur place l'équipement {ip}.")
    return phrases


# ----------------------------------------------------------------------
# La suite construit la page. Tu n'as rien à modifier.
# ----------------------------------------------------------------------

CSS = """
*{box-sizing:border-box}
body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#EEF2F6;color:#1B232D}
header{background:#0B63A6;color:#fff;padding:22px 32px;display:flex;align-items:center;gap:20px}
header img{height:46px;background:#fff;padding:4px;border-radius:4px}
header h1{margin:0;font-size:24px}
header p{margin:2px 0 0;opacity:.85;font-size:14px}
main{max-width:1060px;margin:0 auto;padding:24px 32px 40px}
h2{font-size:18px;color:#0B63A6;border-bottom:2px solid #0B63A6;padding-bottom:4px;margin-top:34px}
.kpi{display:flex;gap:14px;flex-wrap:wrap}
.kpi div{flex:1 1 170px;background:#fff;border-radius:6px;padding:14px 16px;border-left:5px solid #0B63A6}
.kpi b{display:block;font-size:30px}
.kpi span{font-size:13px;color:#4a5866}
table{width:100%;border-collapse:collapse;background:#fff;font-size:14px}
th{background:#1B232D;color:#fff;text-align:left;padding:8px 10px}
td{padding:7px 10px;border-bottom:1px solid #DCE3EA;vertical-align:top}
td.ip{font-family:Consolas,monospace;font-weight:bold}
td.n{text-align:right}
.badge{display:inline-block;padding:2px 9px;border-radius:10px;font-size:12px;font-weight:bold;color:#fff}
.badge.BLOQUER{background:#B8541F}
.badge.ENQUETER{background:#6b7785}
.badge.COMPROMISSION{background:#B3261E}
.risque{color:#B3261E;font-weight:bold}
.ouvert{font-weight:bold}
ul.reco li{margin:6px 0}
pre{background:#1B232D;color:#E6EDF3;padding:14px;border-radius:6px;overflow-x:auto;font-size:13px}
.avert{background:#FFF4E5;border-left:5px solid #B8541F;padding:10px 14px;margin:18px 0;font-size:14px}
.vide{color:#6b7785;font-style:italic}
footer{text-align:center;color:#6b7785;font-size:12px;padding:20px}
"""


def _logo():
    """Lit le logo (texte base64) dans donnees/logo.txt, s'il existe."""
    try:
        with open(os.path.join(DOSSIER_DONNEES, "logo.txt"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def _tableau_vide(texte):
    return f'<p class="vide">{html.escape(texte)}</p>'


def construire_rapport(info):
    """Rend la page HTML complète. info est un dictionnaire préparé par main.py."""
    e = html.escape
    alertes = info.get("alertes") or []
    classes = info.get("classes") or {}
    decisions = info.get("decisions") or {}
    ports = info.get("ports") or []
    regles = info.get("regles") or []
    origine = info.get("origine") or {}
    etapes = info.get("etapes") or {}

    manquantes = [v for v, ok in sorted(etapes.items()) if not ok]
    bandeau = ""
    if manquantes:
        bandeau = ('<div class="avert">Ce rapport est incomplet : les étapes '
                   + e(", ".join(manquantes))
                   + " ne sont pas encore terminées. Lance verifier.bat pour savoir où ça coince.</div>")

    a_bloquer = sum(1 for d in decisions.values() if d in (BLOQUER, COMPROMISSION))
    ouverts = [p for p in ports if p.get("ouvert")]

    kpi = (
        '<div class="kpi">'
        f'<div><b>{info.get("nb_echecs", "?")}</b><span>échecs de connexion lus</span></div>'
        f'<div><b>{len(alertes)}</b><span>alertes de force brute</span></div>'
        f'<div><b>{a_bloquer}</b><span>adresses à bloquer</span></div>'
        f'<div><b>{len(ouverts)}</b><span>ports ouverts sur ce poste</span></div>'
        '</div>'
    )

    # Tableau des alertes
    if alertes:
        lignes = []
        for a in alertes:
            classe = classes.get(a["ip"]) or {"type": "?", "site": "?", "famille": "?"}
            decision = decisions.get(a["ip"]) or ENQUETER
            try:
                lignes.append(ligne_tableau(a, classe, decision) or "")
            except Exception:
                lignes.append(f'<tr><td colspan="7">{e(a["ip"])} : ligne_tableau a planté</td></tr>')
        tab_alertes = ("<table><tr><th>Adresse IP</th><th>Origine</th><th>Comptes visés</th>"
                       "<th>Échecs</th><th>Début</th><th>Fin</th><th>Décision</th></tr>"
                       + "".join(lignes) + "</table>")
    else:
        tab_alertes = _tableau_vide("Aucune alerte pour le moment.")

    # Origine des échecs
    if origine:
        lignes = "".join(f"<tr><td>{e(str(k))}</td><td class=\"n\">{v}</td></tr>" for k, v in sorted(origine.items()))
        tab_origine = f"<table><tr><th>Origine de l'adresse</th><th>Échecs</th></tr>{lignes}</table>"
    else:
        tab_origine = _tableau_vide("Origine des échecs non calculée.")

    # Ports
    if ports:
        lignes = []
        for p in ports:
            etat = "OUVERT" if p.get("ouvert") else "fermé"
            risque = ""
            if p.get("ouvert") and p.get("risque"):
                risque = '<span class="risque">service à risque</span>'
            classe_css = "ouvert" if p.get("ouvert") else ""
            lignes.append(f'<tr><td class="n">{p["port"]}</td><td>{e(str(p["service"]))}</td>'
                          f'<td class="{classe_css}">{etat}</td><td>{risque}</td></tr>')
        tab_ports = ("<table><tr><th>Port</th><th>Service</th><th>État</th><th>Remarque</th></tr>"
                     + "".join(lignes) + "</table>")
    else:
        tab_ports = _tableau_vide("Scan des ports non réalisé.")

    # Recommandations
    reco = info.get("recommandations") or []
    if reco:
        liste_reco = '<ul class="reco">' + "".join(f"<li>{e(r)}</li>" for r in reco) + "</ul>"
    else:
        liste_reco = _tableau_vide("Aucune recommandation.")

    # Règles de pare-feu
    if regles:
        bloc_regles = "<pre>" + e("\n".join(regles)) + "</pre>"
    else:
        bloc_regles = _tableau_vide("Aucune règle générée.")

    logo = _logo()
    img = f'<img alt="ENSITECH" src="data:image/png;base64,{logo}">' if logo else ""

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<title>Vigie : rapport de surveillance</title>
<style>{CSS}</style></head><body>
<header>{img}<div><h1>Vigie : rapport de surveillance</h1>
<p>Bergerat-Tournier, journaux d'authentification SSH du 27 octobre au 1er novembre</p></div></header>
<main>
{bandeau}
<h2>En bref</h2>
{kpi}
<h2>Alertes de force brute</h2>
{tab_alertes}
<h2>D'où viennent les échecs</h2>
{tab_origine}
<h2>Ports ouverts sur ce poste (127.0.0.1)</h2>
{tab_ports}
<h2>Ce qu'il faut faire</h2>
{liste_reco}
<h2>Règles de pare-feu proposées</h2>
<div class="avert">Ces commandes sont seulement affichées. Vigie ne les exécute jamais : un administrateur les relit avant de les lancer.</div>
{bloc_regles}
</main>
<footer>{e(ECOLE)}</footer>
</body></html>
"""
