import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Démonstration de Prédiction de Blessures au Rugby",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Titre et Avertissement ---
st.title("🏉 Application de Démonstration de Prédiction de Blessures au Rugby")
st.subheader("Analyse des Facteurs de Risque et Pathologies Probables")
st.write("---")

st.warning("""
    ⚠️ **AVERTISSEMENT CRUCIAL :**
    Cette application est une **démonstration conceptuelle à des fins éducatives uniquement**.
    Elle est basée sur des corrélations et des conclusions tirées de la littérature scientifique, mais elle **ne fournit aucune prédiction médicale ou clinique valide**.
    La prédiction de blessures dans le sport est un domaine complexe qui nécessite des modèles d'apprentissage automatique entraînés sur de vastes ensembles de données réelles et validées.
    **Ne pas utiliser cette application pour prendre des décisions concernant la santé, l'entraînement ou la gestion des blessures d'un individu.**
    Consultez toujours un professionnel de la santé qualifié (médecin du sport, kinésithérapeute, préparateur physique) pour toute préoccupation ou décision médicale.
""")
st.write("---")

# --- Section Profil du Joueur ---
st.header("1. Profil du Joueur")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Âge du Joueur (années)", 18, 40, 25)
    poids_corporel = st.number_input("Poids Corporel (kg)", min_value=50.0, max_value=150.0, value=90.0, step=1.0)
    position_joueur = st.selectbox(
        "Position du Joueur",
        ["Avant (Pack)", "Arrière (Ligne)", "Mêlée", "Ouverture", "Autre"],
        help="Les avants sont plus à risque de blessures graves aux membres inférieurs non-contact."
    )

with col2:
    st.write("---")
    st.markdown("**Historique de Blessures :**")
    hist_blessure_membres_inf = st.checkbox("Antécédent de blessure aux membres inférieurs ?", help="Facteur de risque primaire pour les blessures récurrentes et nouvelles.")
    hist_entorse_cheville = st.checkbox("Antécédent d'entorse de la cheville ?", help="Facteur de risque pour les blessures à la cheville.")
    hist_commotion = st.checkbox("Antécédent de commotion cérébrale (saison précédente) ?", help="Augmente le risque de blessures aux membres inférieurs.")

# --- Section Données d'Entraînement et de Performance ---
st.header("2. Données d'Entraînement et de Performance")
col4, col5, col6 = st.columns(3)

with col4:
    monotonie_charge = st.slider(
        "Monotonie de la Charge d'Entraînement (échelle 1-10)",
        1, 10, 5,
        help="Une valeur élevée (ex: >7) indique une faible variation de la charge hebdomadaire, augmentant le risque de blessures graves non-contact. (1: Grande variation, 10: Faible variation)"
    )
    douleur_musculaire = st.slider(
        "Douleur Musculaire Perçue (échelle 1-10)",
        1, 10, 3,
        help="Une augmentation significative (ex: >6) est un symptôme pré-blessure des membres inférieurs graves. (1: Aucune douleur, 10: Douleur extrême)"
    )

with col5:
    sprint_10m = st.number_input("Temps de Sprint 10m (secondes)", min_value=1.0, max_value=3.0, value=1.7, step=0.05, help="Temps plus lents (ex: >1.7s) associés à un risque accru de blessures non-contact aux membres inférieurs.")
    sprint_40m = st.number_input("Temps de Sprint 40m (secondes)", min_value=4.0, max_value=7.0, value=5.3, step=0.05, help="Temps plus lents (ex: >5.4s) associés à un risque accru de blessures non-contact aux membres inférieurs.")

# --- Section Données Musculo-Squelettiques et Biomécaniques Clés ---
st.header("3. Données Musculo-Squelettiques et Biomécaniques Clés")
col7, col8, col9 = st.columns(3)

with col7:
    dorsiflexion_cheville = st.number_input("Angle de Dorsiflexion de la Cheville (degrés)", min_value=15.0, max_value=45.0, value=30.0, step=0.5, help="Un angle réduit (ex: <25°) ou une réduction en cours de saison est un prédicteur de blessures non-contact aux membres inférieurs et aux chevilles.")
    force_adducteurs = st.slider("Force des Adducteurs (score 1-10)", 1, 10, 7, help="Une réduction de force (ex: <5) est un prédicteur de blessures graves aux membres inférieurs non-contact. (1: Très faible, 10: Très forte)")

with col8:
    force_ischios = st.slider("Force des Ischio-jambiers (score 1-10)", 1, 10, 7, help="Une réduction de force (ex: <5) est un prédicteur de blessures graves aux membres inférieurs non-contact. (1: Très faible, 10: Très forte)")
    taux_changement_angle_art = st.slider(
        "Taux de Changement d'Angle Articulaire (échelle 1-10)",
        1, 10, 5,
        help="Indique des changements drastiques d'angle. Une valeur élevée (ex: >7) est fortement corrélée à un très haut risque de blessure générale aux membres inférieurs."
    )

with col9:
    force_reaction_sol = st.slider(
        "Force de Réaction au Sol (GRF) (échelle 1-10)",
        1, 10, 5,
        help="Indique une mauvaise utilisation de la force. Une valeur élevée (ex: >7) est corrélée à un risque moyen de blessure générale aux membres inférieurs."
    )

st.write("---")

# --- Logique de Prédiction et Calcul des Scores ---
st.header("4. Analyse du Risque et Recommandations")

if st.button("Calculer le Risque de Blessure"):
    score_risque_global = 0
    facteurs_risque_contributeurs = []
    recommandations = []
    pathologies_probables = {
        "Blessures Cheville": 0,
        "Blessures Ischio-jambiers": 0,
        "Blessures Genou (non-ACL)": 0,
        "Blessures Aine/Hanche": 0,
        "Blessures Graves Membres Inférieurs": 0,
        "Blessures Générales Membres Inférieurs": 0,
    }

    # --- Évaluation des facteurs de risque et mise à jour du score global ---

    # Historique de blessures
    if hist_blessure_membres_inf:
        score_risque_global += 20
        facteurs_risque_contributeurs.append("Historique de blessures aux membres inférieurs")
        recommandations.append("- Un suivi particulier est recommandé en raison des antécédents de blessures aux membres inférieurs.")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 2
    if hist_entorse_cheville:
        score_risque_global += 15
        facteurs_risque_contributeurs.append("Historique d'entorse de la cheville")
        recommandations.append("- Concentrez-vous sur la réhabilitation et la prévention des entorses de la cheville.")
        pathologies_probables["Blessures Cheville"] += 3
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 1
    if hist_commotion:
        score_risque_global += 10
        facteurs_risque_contributeurs.append("Historique de commotion cérébrale")
        recommandations.append("- Un suivi neurologique et une attention particulière à la coordination sont conseillés.")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 1

    # Charge d'entraînement et douleur musculaire
    if monotonie_charge >= 7:
        score_risque_global += 25
        facteurs_risque_contributeurs.append(f"Faible variation de la charge d'entraînement (monotonie élevée: {monotonie_charge}/10)")
        recommandations.append("- Optimisez la variation de la charge d'entraînement hebdomadaire pour éviter la monotonie.")
        pathologies_probables["Blessures Graves Membres Inférieurs"] += 3
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 2
    if douleur_musculaire >= 6:
        score_risque_global += 15
        facteurs_risque_contributeurs.append(f"Douleur musculaire perçue élevée ({douleur_musculaire}/10)")
        recommandations.append("- Surveillez attentivement la douleur musculaire et ajustez les temps de récupération.")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 2

    # Temps de sprint
    if sprint_10m > 1.7:
        score_risque_global += 10 * ((sprint_10m - 1.7) / 0.1) # Augmente le score plus le temps est élevé
        facteurs_risque_contributeurs.append(f"Temps de sprint 10m lent ({sprint_10m}s)")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 1
    if sprint_40m > 5.4:
        score_risque_global += 15 * ((sprint_40m - 5.4) / 0.1) # Augmente le score plus le temps est élevé
        facteurs_risque_contributeurs.append(f"Temps de sprint 40m lent ({sprint_40m}s)")
        recommandations.append("- Travaillez l'amélioration de la vitesse de sprint.")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 2
        pathologies_probables["Blessures Cheville"] += 1

    # Dorsiflexion de la cheville
    if dorsiflexion_cheville < 25:
        score_risque_global += 20
        facteurs_risque_contributeurs.append(f"Angle de dorsiflexion de la cheville réduit ({dorsiflexion_cheville}°)")
        recommandations.append("- Améliorez l'amplitude de mouvement de la dorsiflexion de la cheville.")
        pathologies_probables["Blessures Cheville"] += 3
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 2
        pathologies_probables["Blessures Genou (non-ACL)"] += 1 # Impact sur genou/hanche aussi.

    # Forces musculaires
    if force_adducteurs < 5:
        score_risque_global += 20
        facteurs_risque_contributeurs.append(f"Force des adducteurs faible ({force_adducteurs}/10)")
        recommandations.append("- Renforcez spécifiquement les muscles adducteurs.")
        pathologies_probables["Blessures Aine/Hanche"] += 3
        pathologies_probables["Blessures Graves Membres Inférieurs"] += 2
    if force_ischios < 5:
        score_risque_global += 25
        facteurs_risque_contributeurs.append(f"Force des ischio-jambiers faible ({force_ischios}/10)")
        recommandations.append("- Priorisez le renforcement excentrique des ischio-jambiers.")
        pathologies_probables["Blessures Ischio-jambiers"] += 4
        pathologies_probables["Blessures Graves Membres Inférieurs"] += 3

    # Facteurs biomécaniques (Zhao)
    if taux_changement_angle_art >= 7:
        score_risque_global += 25
        facteurs_risque_contributeurs.append(f"Taux de changement d'angle articulaire élevé ({taux_changement_angle_art}/10)")
        recommandations.append("- Travaillez la technique de mouvement pour éviter les changements d'angle drastiques.")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 3
    if force_reaction_sol >= 7:
        score_risque_global += 15
        facteurs_risque_contributeurs.append(f"Force de réaction au sol élevée ({force_reaction_sol}/10)")
        recommandations.append("- Évaluez et corrigez l'utilisation de la force lors des impacts au sol.")
        pathologies_probables["Blessures Générales Membres Inférieurs"] += 2

    # Poids corporel
    # Un poids corporel plus élevé est associé à un risque accru de blessures non-contact à la cheville.
    if poids_corporel > 100 and position_joueur == "Avant (Pack)": # Seuil adapté pour les avants
        score_risque_global += 15
        facteurs_risque_contributeurs.append(f"Poids corporel élevé ({poids_corporel} kg) pour un avant")
        recommandations.append("- Optimisez la composition corporelle si cela est pertinent pour la performance et le risque de blessure.")
        pathologies_probables["Blessures Cheville"] += 2
    elif poids_corporel > 95 and position_joueur != "Avant (Pack)": # Seuil un peu plus bas pour les arrières
        score_risque_global += 10
        facteurs_risque_contributeurs.append(f"Poids corporel élevé ({poids_corporel} kg) pour un arrière")
        recommandations.append("- Optimisez la composition corporelle si cela est pertinent pour la performance et le risque de blessure.")
        pathologies_probables["Blessures Cheville"] += 1

    # Position du joueur
    if position_joueur == "Avant (Pack)": # Les avants sont plus susceptibles de subir des blessures graves aux membres inférieurs non-contact.
        score_risque_global += 10
        facteurs_risque_contributeurs.append("Position d'avant (risque accru de blessures graves aux membres inférieurs)")
        recommandations.append("- Les avants doivent être particulièrement vigilants sur les mesures préventives des membres inférieurs.")
        pathologies_probables["Blessures Graves Membres Inférieurs"] += 1

    # Ajustement du score global pour être dans une plage raisonnable (0-100)
    score_risque_global = min(score_risque_global, 100)
    score_risque_global = max(score_risque_global, 0) # S'assurer que le score ne soit pas négatif

    # Détermination du niveau de risque
    if score_risque_global >= 70:
        niveau_risque = "ÉLEVÉ 🔴"
        st.error(f"### Niveau de Risque Simulé : {niveau_risque}")
        st.write("Le joueur présente plusieurs facteurs de risque importants qui, combinés, indiquent une probabilité simulée élevée de blessure. Une attention immédiate et des mesures préventives ciblées sont fortement recommandées.")
    elif score_risque_global >= 40:
        niveau_risque = "MODÉRÉ 🟠"
        st.warning(f"### Niveau de Risque Simulé : {niveau_risque}")
        st.write("Le joueur présente des facteurs de risque nécessitant une surveillance attentive et des ajustements progressifs pour réduire le risque de blessure.")
    else:
        niveau_risque = "FAIBLE 🟢"
        st.success(f"### Niveau de Risque Simulé : {niveau_risque}")
        st.write("Le risque de blessure simulé est actuellement faible. Continuez à maintenir de bonnes pratiques d'entraînement et de récupération, et restez vigilant aux changements.")

    st.write(f"**Score de Risque Global Simulé :** {score_risque_global:.0f}/100")

    if facteurs_risque_contributeurs:
        st.write("**Facteurs de Risque Contribuants Détectés :**")
        for facteur in sorted(list(set(facteurs_risque_contributeurs))): # Utiliser set pour éviter les doublons, puis trier pour la cohérence
            st.markdown(f"- {facteur}")
    else:
        st.info("Aucun facteur de risque majeur détecté pour cette simulation. Continuez à suivre les bonnes pratiques.")

    st.write("---")
    st.header("5. Vue d'Ensemble des Risques (Toile d'Araignée)")

    # Préparation des données pour la toile d'araignée
    # Normaliser les scores des pathologies de 0 à 5 (pour une meilleure visualisation)
    max_patho_score = max(pathologies_probables.values()) if pathologies_probables else 1
    if max_patho_score == 0: max_patho_score = 1 # Éviter division par zéro

    categories = list(pathologies_probables.keys())
    # Scale pathologies to 0-5. For demonstration, we just show relative "intensity"
    values_pathologies = [ (v / max_patho_score) * 5 for v in pathologies_probables.values()]

    # Préparation des facteurs de risque pour la toile d'araignée
    # Utiliser des noms plus courts et clairs pour la visualisation
    # Scaler tous les facteurs binaires à 5 si présents, les sliders sur une échelle 0-5
    radar_factors = {
        "Hist. Bless.": 0,
        "Monot. Charge": 0,
        "Sprint Lent": 0,
        "Dorsiflex. Réd.": 0,
        "Faibl. Adduct.": 0,
        "Faibl. Ischios": 0,
        "Chgmt. Angle Élevé": 0,
        "GRF Élevée": 0,
        "Poids Élevé": 0,
        "Position Avant": 0,
        "Douleur Musc. Élevée": 0
    }

    if hist_blessure_membres_inf or hist_entorse_cheville or hist_commotion:
        radar_factors["Hist. Bless."] = 5
    if monotonie_charge >= 7:
        radar_factors["Monot. Charge"] = (monotonie_charge - 5) * 2.5 if monotonie_charge > 5 else 0
    if sprint_10m > 1.7 or sprint_40m > 5.4:
        radar_factors["Sprint Lent"] = 5
    if dorsiflexion_cheville < 25:
        radar_factors["Dorsiflex. Réd."] = 5
    if force_adducteurs < 5:
        radar_factors["Faibl. Adduct."] = 5
    if force_ischios < 5:
        radar_factors["Faibl. Ischios"] = 5
    if taux_changement_angle_art >= 7:
        radar_factors["Chgmt. Angle Élevé"] = (taux_changement_angle_art - 5) * 2.5 if taux_changement_angle_art > 5 else 0
    if force_reaction_sol >= 7:
        radar_factors["GRF Élevée"] = (force_reaction_sol - 5) * 2.5 if force_reaction_sol > 5 else 0
    if (poids_corporel > 100 and position_joueur == "Avant (Pack)") or (poids_corporel > 95 and position_joueur != "Avant (Pack)"):
        radar_factors["Poids Élevé"] = 5
    if position_joueur == "Avant (Pack)":
        radar_factors["Position Avant"] = 5
    if douleur_musculaire >= 6:
        radar_factors["Douleur Musc. Élevée"] = (douleur_musculaire - 5) * 2.5 if douleur_musculaire > 5 else 0

    # Combine all categories and values for the radar chart
    radar_categories_combined = list(pathologies_probables.keys()) + list(radar_factors.keys())
    radar_values_combined = values_pathologies + list(radar_factors.values())

    df_radar = pd.DataFrame(dict(
        r=radar_values_combined,
        theta=radar_categories_combined
    ))

    fig_radar = px.line_polar(df_radar, r="r", theta="theta", line_close=True,
                              title="Toile d'Araignée des Risques (Pathologies Probables & Facteurs à Surveiller)")
    fig_radar.update_traces(fill='toself', name="Niveau de Risque")
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],  # Échelle de 0 à 5 pour une meilleure visibilité
                tickvals=np.arange(0, 6, 1),
                ticktext=[f'{i}' for i in np.arange(0, 6, 1)]
            )),
        showlegend=False,
        font=dict(size=12) # Ajuste la taille de la police pour les labels
    )
    st.plotly_chart(fig_radar, use_container_width=True)


    st.write("---")
    st.header("6. Recommandations Ciblées")
    if recommandations:
        for rec in sorted(list(set(recommandations))): # Utiliser set pour éviter les doublons, puis trier pour la cohérence
            st.markdown(rec)
        st.markdown("""
        **Rappel :** Ces recommandations sont génériques et basées sur des corrélations scientifiques.
        Une évaluation individuelle par un professionnel de la santé ou un préparateur physique est indispensable pour des conseils précis et adaptés.
        """)
    else:
        st.info("Aucune recommandation spécifique ne ressort des entrées actuelles. Continuez à suivre les bonnes pratiques d'entraînement et de récupération.")

    st.write("---")
    st.markdown("""
    <small>Application développée à des fins de démonstration par votre assistant IA, basée sur les recherches de Leckey et al. (2025) , Zhao (2025), Evans et al. (2024), et Owen et al. (2024).</small>
    """, unsafe_allow_html=True)
