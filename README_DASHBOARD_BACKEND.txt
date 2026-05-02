Dashboard conservé avec la même apparence que la pièce jointe, connecté au backend réel.

Lancement backend:
  cd team-wie-master
  pip install -r requirements.txt
  uvicorn backend.api:app --reload --port 8000

Puis ouvrir tnassnissa_dashboard.html dans le navigateur.

Pipeline cible:
  Sources (RSS + Google Trends + YouTube)
        -> Data Collector Python
        -> Summarizer Claude API si ANTHROPIC_API_KEY existe, sinon NLP local
        -> Persona Engine / Dashboard Builder
        -> Dashboard Streamlit ou HTML

Lancement Streamlit:
  streamlit run streamlit_app.py

Variables optionnelles:
  ANTHROPIC_API_KEY  active le resume Claude
  YOUTUBE_API_KEY    active la collecte YouTube reelle

Endpoints ajoutés:
  /api/dashboard/{persona}
  /api/regions
  /api/region/{region}
  /api/detail/{kind}/{key}
