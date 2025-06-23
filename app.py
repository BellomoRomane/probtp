import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# ---------- CONFIGURATION ----------
FICHIER_DONNEES = "donnees.xlsx"
FICHIER_OPTIONS = "options.json"

# ---------- CHARGEMENT / INIT OPTIONS ----------
def charger_options():
    if os.path.exists(FICHIER_OPTIONS):
        with open(FICHIER_OPTIONS, "r") as f:
            return json.load(f)
    else:
        return {
            "environnements": ["PROBTP", "NHCB", "LOURMEL"],
            "assureurs": ["PROBTP", "PRODIGEO", "BOISSIERE"],
            "produits": ["Produit A", "Produit B"]
        }

def sauvegarder_options(options):
    with open(FICHIER_OPTIONS, "w") as f:
        json.dump(options, f)

options = charger_options()

# ---------- INTERFACE ----------
st.title("Formulaire de sélection")

# ENVIRONNEMENT
env = st.selectbox("Choisissez un environnement :", options["environnements"] + ["Information non présente"])
if env == "Information non présente":
    nouveau_env = st.text_input("Entrez un nouvel environnement :")
    if nouveau_env:
        options["environnements"].append(nouveau_env)
        sauvegarder_options(options)
        st.success(f"{nouveau_env} ajouté aux environnements.")
        env = nouveau_env

# ASSUREUR (si PROBTP)
assureur = ""
if env == "PROBTP":
    assureur = st.selectbox("Choisissez un assureur :", options["assureurs"] + ["Information non présente"])
    if assureur == "Information non présente":
        nouveau_ass = st.text_input("Entrez un nouvel assureur :")
        if nouveau_ass:
            options["assureurs"].append(nouveau_ass)
            sauvegarder_options(options)
            st.success(f"{nouveau_ass} ajouté aux assureurs.")
            assureur = nouveau_ass

# PRODUIT (si NHCB)
produit = ""
if env == "NHCB":
    produit = st.selectbox("Choisissez un produit :", options["produits"] + ["Information non présente"])
    if produit == "Information non présente":
        nouveau_prod = st.text_input("Entrez un nouveau produit :")
        if nouveau_prod:
            options["produits"].append(nouveau_prod)
            sauvegarder_options(options)
            st.success(f"{nouveau_prod} ajouté aux produits.")
            produit = nouveau_prod

# Variables automatiques si cas spécifique
institution, pseudo1, millesime, pseudo23 = "", "", None, None
if env == "PROBTP" and assureur == "PROBTP":
    produit = "FMC"
    institution = "FMC BTP-P"
    pseudo1 = "PSEUDO_AUTO"
    millesime = 20
    pseudo23 = 20

# ---------- ENREGISTREMENT ----------
if st.button("Valider"):
    donnees = {
        "ENVIRONNEMENT": env,
        "ASSUREUR": assureur,
        "PRODUIT": produit,
        "INSTITUTION": institution,
        "PSEUDO1": pseudo1,
        "MILLESIME": millesime,
        "PSEUDO23": pseudo23,
        "Horodatage": datetime.now()
    }

    try:
        df = pd.read_excel(FICHIER_DONNEES)
    except FileNotFoundError:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([donnees])], ignore_index=True)
    df.to_excel(FICHIER_DONNEES, index=False)
    st.success("✅ Données enregistrées avec succès.")

# ---------- AFFICHAGE + TELECHARGEMENT ----------
st.subheader("📊 Données enregistrées")

try:
    df_saved = pd.read_excel(FICHIER_DONNEES)
    st.dataframe(df_saved)
    st.download_button("📥 Télécharger le fichier Excel", data=df_saved.to_excel(index=False), file_name="donnees.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
except:
    st.info("Aucune donnée enregistrée pour l'instant.")
