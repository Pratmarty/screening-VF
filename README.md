# Application de Démonstration de Prédiction de Blessures au Rugby

Cette application Streamlit est une démonstration interactive des facteurs de risque de blessures au rugby, basée sur des conclusions tirées de la littérature scientifique. Elle permet d'entrer des données sur un joueur et de visualiser une analyse de risque simulée sous forme de graphique en toile d'araignée, accompagnée de recommandations ciblées.

**⚠️ AVERTISSEMENT IMPORTANT :**
Cette application est à des fins **éducatives et de démonstration uniquement**. Elle **ne fournit aucune prédiction médicale ou clinique valide** et ne doit en aucun cas être utilisée pour prendre des décisions réelles concernant la santé, l'entraînement ou la gestion des blessures d'un individu. Consultez toujours un professionnel de la santé qualifié pour toute préoccupation.

## Fonctionnalités

* **Entrée de données joueur :** Saisie de diverses informations (profil, historique de blessures, données d'entraînement et de performance, mesures musculo-squelettiques et biomécaniques).
* **Analyse de risque simulée :** Calcul d'un score de risque global et identification des facteurs de risque contribuants, basés sur des règles simplifiées inspirées de la recherche scientifique.
* **Visualisation en toile d'araignée :** Un graphique radar résumant les pathologies probables et les principaux facteurs de risque à surveiller.
* **Recommandations ciblées :** Suggestions génériques pour la prévention des blessures basées sur les facteurs de risque identifiés.

## Comment l'exécuter localement

1.  **Pré-requis :** Assurez-vous d'avoir [Python](https://www.python.org/downloads/) installé sur votre machine (version 3.8 ou supérieure recommandée).

2.  **Cloner le dépôt GitHub (ou télécharger les fichiers) :**
    Si vous avez Git, ouvrez votre terminal et exécutez :
    ```bash
    git clone <URL_de_votre_dépôt>
    cd <nom_de_votre_dépôt>
    ```
    Sinon, téléchargez les fichiers `streamlit_app.py` et `requirements.txt` dans un même dossier.

3.  **Créer un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    # Sur Windows
    .\venv\Scripts\activate
    # Sur macOS/Linux
    source venv/bin/activate
    ```

4.  **Installer les dépendances :**
    Avec l'environnement virtuel activé, installez les bibliothèques nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

5.  **Exécuter l'application Streamlit :**
    ```bash
    streamlit run streamlit_app.py
    ```
    Ceci ouvrira l'application dans votre navigateur web par défaut.

## Déploiement sur Streamlit Community Cloud

Vous pouvez facilement déployer cette application sur [Streamlit Community Cloud](https://streamlit.io/cloud). Voici les étapes générales :

1.  **Créer un dépôt GitHub :** Assurez-vous que tous les fichiers (`streamlit_app.py`, `requirements.txt`, `README.md`) sont dans un dépôt GitHub public.
2.  **Se connecter à Streamlit Community Cloud :** Allez sur `share.streamlit.io` et connectez-vous avec votre compte GitHub.
3.  **Déployer une nouvelle application :** Cliquez sur "New app" ou "Deploy an app".
4.  **Sélectionner le dépôt :** Choisissez votre dépôt GitHub, la branche (généralement `main` ou `master`), et le fichier principal de l'application (qui est `streamlit_app.py`).
5.  **Déployer !** Streamlit Cloud construira et déploiera automatiquement votre application. Il utilisera `requirements.txt` pour installer les dépendances.

L'application sera ensuite accessible via une URL publique (par exemple, `votre-utilisateur.streamlit.app/votre-app`).

## Références Scientifiques (sources principales d'inspiration)

* Leckey C, et al. (2025). *Machine learning approaches to injury risk prediction in sport: a scoping review with evidence synthesis*. [cite_start]Br J Sports Med. 
* Zhao Y. (2025). *New paths to promote athletic injury prevention by integrating statistics and sports biomechanics*. [cite_start]Molecular & Cellular Biomechanics. 
* Evans SL, et al. (2024). *Non-contact lower limb injuries in Rugby Union: A two-year pattern recognition analysis of injury risk factors*. [cite_start]PLOS ONE. 
* Owen R, et al. (2024). *Artificial Intelligence for Sport Injury Prediction*. [cite_start]Book Chapter Preprint.
