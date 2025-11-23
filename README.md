# 🌦️ Météo & Humeur

**Étude observationnelle : Influence de la météo sur l'humeur**  
*Campus Université de Lille - Cité Scientifique*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
---

## 📊 Vue d'ensemble

Ce projet analyse l'impact des conditions météorologiques sur les manifestations comportementales d'humeur chez 2070 individus observés durant 29 sessions entre octobre et novembre 2024.

**Résultat principal** : Différence significative de **13.3 points** de proportion d'humeur positive entre temps variable (24.0%) et temps maussade (10.7%), *p* < 0.001.

---

## 🎯 Méthodologie

- **Population** : Usagers du campus (étudiants, personnel, visiteurs)
- **Lieux** : Lilliad (86.3%), Métro Cité Scientifique (13.7%)
- **Période** : 21 oct. - 21 nov. 2025
- **Indicateurs** : Expression faciale, interactions sociales
---

## 📁 Structure

```
meteo-humeur/
│
├── notebooks/
│   └── analyse_meteo_humeur.ipynb    # Analyse complète avec visualisations
│
├── CSVs/
│   └── meteo_humeur.csv              # Données brutes (29 sessions)
│
├── docs/
│   └── compte_rendu.pdf              # Rapport complet de l'étude
│
└── README.md
```

---

## 🔬 Résultats clés

| Météo | Humeur positive | IC 95% | n |
|-------|----------------|---------|---|
| **Variable** | 24.0% | [20.9% ; 27.2%] | 703 |
| **Couvert** | 17.9% | [15.4% ; 20.4%] | 900 |
| **Maussade** | 10.7% | [7.9% ; 13.5%] | 467 |

**Corrélations principales** :
- Humidité : *r* = -0.668
- Température ressentie : *r* = +0.629
- Nébulosité : *r* = -0.555

**Modèle de régression** : R² = 0.733 (73.3% variance expliquée)

---

## 👥 Équipe

**Auteurs de l'étude** :
- ROUSSEAU Rayane
- TCHASSOU Leonel
- LOUIS JOSEPH Hugo
- MARCOT Solenn

**Développement & Analyse** :  
[Rayane Rousseau](https://github.com/Rayane0001) - Code Jupyter & traitement des données

---

*Projet réalisé dans le cadre d'un module de méthodologie scientifique (DES) - Université de Lille, 2025*