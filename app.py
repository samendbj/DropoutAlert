"""DropoutAlert : interface de démonstration (Streamlit).

Lancer :  streamlit run app.py
Fichiers nécessaires dans le même dossier :
modele_A.joblib, modele_B.joblib, modele_C.joblib, config_modeles.json, defaults.json
"""
import json

import joblib
import pandas as pd
import streamlit as st

CATEGORIELLES = [
    "Marital Status", "Application mode", "Course", "Previous qualification",
    "Nacionality", "Mother's qualification", "Father's qualification",
    "Mother's occupation", "Father's occupation",
]

NOMS = {
    "A": "A. À l'inscription",
    "B": "B. Après le 1er semestre",
    "C": "C. Après le 2e semestre",
}

st.set_page_config(page_title="DropoutAlert", layout="centered")


@st.cache_resource
def charger():
    with open("config_modeles.json", encoding="utf-8") as f:
        cfg = json.load(f)
    with open("defaults.json", encoding="utf-8") as f:
        defaults = json.load(f)
    modeles = {sc: joblib.load(f"modele_{sc}.joblib") for sc in cfg}
    return cfg, defaults, modeles


cfg, defaults, modeles = charger()


def nombre(label, cle, mini, maxi, pas=1.0):
    return st.number_input(
        label, min_value=float(mini), max_value=float(maxi),
        value=float(defaults[cle]), step=float(pas), key=cle,
    )


def oui_non(label, cle):
    choix = st.selectbox(label, ["Non", "Oui"], index=int(defaults[cle]), key=cle)
    return 1 if choix == "Oui" else 0


st.title("DropoutAlert")
st.write(
    "Estime le risque d'abandon d'un étudiant. Projet pédagogique : "
    "l'outil sert à proposer de l'aide, jamais à sanctionner."
)

sc = st.radio("Moment de l'alerte", list(NOMS), format_func=NOMS.get, horizontal=True)
st.caption(f"Modèle utilisé : {cfg[sc]['modele']}")

saisie = {}

st.subheader("Profil à l'inscription")
g, d = st.columns(2)
with g:
    saisie["Age at enrollment"] = nombre("Âge à l'inscription", "Age at enrollment", 16, 70)
    saisie["Admission grade"] = nombre("Note d'admission (0 à 200)", "Admission grade", 0, 200, 0.5)
    saisie["Previous qualification (grade)"] = nombre(
        "Note du diplôme précédent (0 à 200)", "Previous qualification (grade)", 0, 200, 0.5
    )
    genre = st.selectbox("Genre", ["Femme", "Homme"], index=int(defaults["Gender"]), key="Gender")
    saisie["Gender"] = 1 if genre == "Homme" else 0
with d:
    saisie["Scholarship holder"] = oui_non("Boursier", "Scholarship holder")
    saisie["Debtor"] = oui_non("Endetté (Debtor)", "Debtor")
    saisie["Tuition fees up to date"] = oui_non("Frais de scolarité à jour", "Tuition fees up to date")
    saisie["Displaced"] = oui_non("Déplacé (Displaced)", "Displaced")


def semestre(prefixe, titre):
    st.subheader(titre)
    p = f"Curricular units {prefixe}"
    g, d = st.columns(2)
    with g:
        saisie[f"{p} (enrolled)"] = nombre("Unités inscrites", f"{p} (enrolled)", 0, 30)
        saisie[f"{p} (approved)"] = nombre("Unités validées", f"{p} (approved)", 0, 30)
    with d:
        saisie[f"{p} (evaluations)"] = nombre("Évaluations passées", f"{p} (evaluations)", 0, 50)
        saisie[f"{p} (grade)"] = nombre("Moyenne (0 à 20)", f"{p} (grade)", 0, 20, 0.1)


if sc in ("B", "C"):
    semestre("1st sem", "Résultats du 1er semestre")
if sc == "C":
    semestre("2nd sem", "Résultats du 2e semestre")

st.divider()
if st.button("Calculer le risque", type="primary"):
    variables = cfg[sc]["variables"]
    X = pd.DataFrame([{v: saisie.get(v, defaults[v]) for v in variables}])
    for c in CATEGORIELLES:
        if c in X.columns:
            X[c] = X[c].astype(int)

    proba = float(modeles[sc].predict_proba(X)[0, 1])
    seuil = float(cfg[sc]["seuil"])

    st.metric("Probabilité estimée d'abandon", f"{proba:.0%}")
    st.progress(min(max(proba, 0.0), 1.0))
    if proba >= seuil:
        st.error("Risque élevé : proposer un accompagnement (tutorat, aide financière, entretien).")
    else:
        st.success("Risque faible : pas d'alerte pour ce profil.")
    st.caption(
        f"Seuil d'alerte du scénario {sc} : {seuil:.2f} (choisi pour repérer au moins 80 % "
        "des abandons en validation croisée). Les variables non saisies (famille, filière, etc.) "
        "sont remplies par des valeurs typiques : le résultat est indicatif."
    )
