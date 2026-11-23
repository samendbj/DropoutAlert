# DropoutAlert

**À quel moment du parcours peut-on repérer un étudiant à risque d'abandon, et avec quelle fiabilité ?**

DropoutAlert prédit si un étudiant va abandonner ou obtenir son diplôme, à trois moments : à l'inscription, après le 1er semestre et après le 2e semestre. Le but est de proposer de l'aide aux étudiants à risque, jamais de les sanctionner.

## Résumé

- 3 modèles comparés : régression logistique, Random Forest, XGBoost.
- 3 scénarios : A (inscription), B (A + 1er semestre), C (B + 2e semestre).
- Évaluation : F1, rappel, ROC-AUC et PR-AUC de la classe « abandon », avec intervalles de confiance à 95 %.
- Seuil d'alerte choisi pour avoir un rappel d'au moins 80 % (on préfère une fausse alerte à un abandon raté).
- Explication des facteurs de risque avec SHAP.
- Interface Streamlit avec les 3 scénarios.

## Données

Dataset « Predict Students' Dropout and Academic Success » (UCI, id 697), licence CC BY 4.0.

- 4 424 étudiants d'un institut polytechnique portugais, une trentaine de variables.
- Version binaire : on retire les « Enrolled ». Il reste 3 630 étudiants (environ 39 % d'abandons).
- Les données sont téléchargées automatiquement avec la bibliothèque `ucimlrepo`. Elles ne sont pas dans ce dépôt.

## Méthode

1. Audit des données (valeurs manquantes, doublons, types).
2. Exploration : taux d'abandon par groupe.
3. Séparation 80 % / 20 % stratifiée (`random_state=42`). Le jeu de test sert seulement à la fin.
4. Un Pipeline (encodage + normalisation) appris sur l'apprentissage seulement, pour éviter les fuites de données.
5. Comparaison des modèles par validation croisée stratifiée (5 plis), avec une référence naïve (toujours « diplômé »).
6. Réglage des paramètres avec `RandomizedSearchCV` (critère : F1).
7. Choix du meilleur modèle de chaque scénario avec la validation croisée, puis choix du seuil (rappel ≥ 80 %) sur l'apprentissage.
8. Évaluation finale sur le test, avec intervalles de confiance (bootstrap, 1000 tirages).
9. Explication avec SHAP.

## Résultats

> À REMPLIR : colle ici le tableau de `results/resultats_finaux.csv` (scénarios A, B, C).

| Scénario | Modèle | Rappel | Fausses alertes | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| A | À remplir | | | | | |
| B | À remplir | | | | | |
| C | À remplir | | | | | |

> À REMPLIR : 2 ou 3 phrases de conclusion qui répondent à la question centrale (par exemple : de combien le résultat progresse entre A et B, puis entre B et C).

## Lancer le projet

```bash
git clone https://github.com/TON_NOM/DropoutAlert.git
cd DropoutAlert
pip install -r requirements.txt
```

- Pour tout refaire : ouvre `notebooks/DropOut.ipynb` (Jupyter ou Google Colab) et lance les cellules dans l'ordre. Le réglage des modèles prend plusieurs minutes.
- Pour lancer l'interface :

```bash
streamlit run app.py
```

## Structure du dépôt

```
DropoutAlert/
├── README.md
├── requirements.txt
├── app.py                  # interface Streamlit
├── notebooks/DropOut.ipynb # analyse complète
├── models/                 # modèles (A, B, C), seuils, valeurs par défaut
└── results/                # tableaux de résultats
```

## Limites

- **Un seul établissement portugais :** les résultats ne se transposent pas automatiquement à la Tunisie.
- **Les « Enrolled » sont retirés :** en vrai, on veut prédire pour des étudiants encore en cours d'études.
- **Scénario A :** certaines variables (par exemple les frais payés ou la dette) sont peut-être connues un peu après l'inscription.
- **Petit jeu de test (environ 726 étudiants) :** les résultats peuvent varier, d'où les intervalles de confiance.
- **Corrélation n'est pas causalité :** les facteurs trouvés avec SHAP sont des associations.

## Éthique

Le modèle sert à proposer de l'aide, jamais à sanctionner. Il se trompe parfois : la décision finale revient toujours à un humain.

## Source des données

Realinho, V., Vieira Martins, M., Machado, J., Baptista, L. (2021). *Predict Students' Dropout and Academic Success* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89

Article de référence : Realinho, V., Machado, J., Baptista, L., Martins, M. V. (2022). Predicting Student Dropout and Academic Success. *Data*, 7(11), 146. https://doi.org/10.3390/data7110146
