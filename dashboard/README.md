# 📡 TNessnisa — PulseTN Persona Dashboard

> *ما نحكيوش برشا... أما نعرفو برشا*

Plateforme tunisienne d'intelligence sociale et médiatique personnalisée.

## 🚀 Lancement rapide

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Structure

```
pulseTN/
├── app.py              ← Dashboard principal
├── database.py         ← Lecture SQLite + mock data
├── persona_engine.py   ← Moteur de décision par persona
├── style.css           ← Thème TNessnisa (rouge/noir/blanc)
├── assets/
│   ├── logo.png        ← Logo centré (page login)
│   └── logo_side.png   ← Logo sidebar (horizontal)
├── data/
│   └── raw_data.db     ← Base SQLite (optionnelle)
├── requirements.txt
├── run.sh
└── run.bat
```

## 👥 Personas disponibles

| Persona | Dashboard |
|---|---|
| 🏢 Entreprise | Carte Tunisie + Brand Safety + GO/PAUSE |
| 📰 Journalisme | Breaking News + Fake Radar |
| 🎬 Influenceur | Trends viraux + Timing optimal |
| ⚽ Sport | Buzz sportif + Tendances |
| 👗 Mode | Fashion trends + Hashtags |
| 🏪 Grande Surface | Risques régionaux + Opportunités |
| 👤 Citoyen | Alertes sécurité + Actualité locale |

## 🎨 Palette

- Rouge `#e60e0f` · Noir `#000000` · Blanc `#ffffff`

## 💾 Base de données

Le dashboard fonctionne sans base (mock data intégré).
Pour utiliser une vraie DB, placer `raw_data.db` dans `data/`.

Table `posts` : `post_id, platform, source, region, content, timestamp, engagement, url`
