import html
import re
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

try:
    import pandas as pd
except ImportError:
    pd = None

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.api import build_dashboard
from backend.services.real_pipeline import run_real_pipeline


st.set_page_config(
    page_title="Tnassnissa Dashboard",
    page_icon="T",
    layout="wide",
    initial_sidebar_state="expanded",
)

PERSONAS = {
    "Journaliste": "journaliste",
    "Entreprise": "entreprise",
    "Influenceur": "influenceur",
    "Citoyen": "citoyen",
    "ONG": "ong",
}

PERSONA_ICONS = {
    "Journaliste": "J",
    "Entreprise": "E",
    "Influenceur": "I",
    "Citoyen": "C",
    "ONG": "O",
}

BUSINESS_INTERESTS = {
    "Mode": "mode",
    "Grand surface / magasin": "grand_surface",
    "Sport": "sport",
}


def clean_text(value):
    text = str(value or "")
    replacements = {
        "ActualitÃƒÂ©": "Actualite",
        "dÃƒÂ©tectÃƒÂ©": "detecte",
        "Ãƒ ": "a ",
        "ÃƒÂ©": "e",
        "ÃƒÂ¨": "e",
        "Ãƒâ€°": "E",
        "Ã‚Â·": "-",
        "Ã¢â‚¬â€": "-",
        "dÃ¢â‚¬â„¢": "d'",
        "ÃƒÂª": "e",
        "ÃƒÂ§": "c",
        "ÃƒÂ´": "o",
        "Â·": "-",
        "â€”": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[\U0001F300-\U0001FAFF]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def safe(value):
    return html.escape(clean_text(value), quote=True)


def html_to_text(value):
    text = clean_text(value)
    text = re.sub(r"</?(strong|b)>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def as_dataframe(rows):
    if pd:
        return pd.DataFrame(rows)
    return rows


def status_badge_class(status):
    normalized = clean_text(status).lower()
    if "danger" in normalized:
        return "danger"
    if "buzz" in normalized or "warning" in normalized:
        return "warning"
    return "info"


def fake_score_for(*parts):
    text = "|".join(clean_text(part) for part in parts)
    if not text:
        return 20
    return 10 + (sum(ord(ch) for ch in text) % 70)


def set_detail(title, body, posts=None):
    st.session_state["detail_panel"] = {
        "title": clean_text(title),
        "body": clean_text(body),
        "posts": posts or [],
    }


def metric_card(label, value, accent="red", change="LIVE"):
    st.markdown(
        f"""
        <div class="kpi-card">
          <div class="kpi-label">{safe(label)}</div>
          <div class="kpi-value {accent}">{safe(value)}</div>
          <div class="kpi-change">{safe(change)}</div>
          <div class="kpi-bar" style="width:72%"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, side=""):
    st.markdown(
        f"""
        <div class="section-header">
          <div class="section-title">{safe(title)}</div>
          <div class="section-side">{safe(side)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_collection():
    with st.spinner("Collecte RSS + Google Trends + YouTube, analyse NLP et sauvegarde..."):
        return run_real_pipeline(save=True)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

    :root {
      --red: #e60e0f;
      --red-dark: #a50a0b;
      --red-faint: rgba(230,14,15,0.08);
      --bg: #060608;
      --bg-2: #0d0d12;
      --bg-card: rgba(255,255,255,0.035);
      --bg-card-hover: rgba(255,255,255,0.065);
      --border: rgba(230,14,15,0.2);
      --border-light: rgba(255,255,255,0.075);
      --text: #f0f0f0;
      --text-dim: #8a8a9a;
      --green: #00e676;
      --orange: #ff9800;
      --cyan: #00b4d8;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
      background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(230,14,15,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(230,14,15,0.045) 0%, transparent 50%),
        #060608 !important;
      color: var(--text) !important;
      font-family: 'Rajdhani', sans-serif;
    }

    [data-testid="stAppViewContainer"]::before {
      content: "";
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(230,14,15,0.032) 1px, transparent 1px),
        linear-gradient(90deg, rgba(230,14,15,0.032) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 0;
    }

    .block-container {
      padding-top: 1.1rem;
      padding-bottom: 2rem;
      max-width: 1420px;
      position: relative;
      z-index: 1;
    }

    [data-testid="stSidebar"] {
      background: rgba(8,8,12,0.98) !important;
      border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
      color: var(--text) !important;
      font-family: 'Rajdhani', sans-serif;
    }

    [data-testid="stSidebar"] h1 {
      color: var(--red) !important;
      font-family: 'Orbitron', monospace;
      text-transform: uppercase;
      letter-spacing: 3px;
      font-size: 1.15rem;
    }

    .stSelectbox label, .stButton button, .stTextInput label {
      font-family: 'Rajdhani', sans-serif !important;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      font-size: .78rem !important;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput input {
      background: rgba(255,255,255,0.04) !important;
      border: 1px solid var(--border-light) !important;
      color: var(--text) !important;
      border-radius: 8px !important;
    }

    .stButton button {
      background: var(--red) !important;
      color: white !important;
      border: 1px solid rgba(230,14,15,.55) !important;
      border-radius: 8px !important;
      font-weight: 700 !important;
      transition: all .2s ease;
    }

    .stButton button:hover {
      box-shadow: 0 12px 32px rgba(230,14,15,.24);
      transform: translateY(-1px);
    }

    h1, h2, h3, p, span, div, label {
      color: var(--text);
    }

    .topbar {
      min-height: 64px;
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 13px 18px;
      margin-bottom: 18px;
      background: rgba(6,6,8,0.95);
      border: 1px solid var(--border);
      border-radius: 10px;
      backdrop-filter: blur(12px);
    }

    .logo-tile {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      display: grid;
      place-items: center;
      background: var(--red);
      color: white;
      font-family: 'Orbitron', monospace;
      font-weight: 900;
      box-shadow: 0 0 26px rgba(230,14,15,.28);
    }

    .brand-title {
      color: var(--red);
      font-family: 'Orbitron', monospace;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      line-height: 1.1;
    }

    .brand-subtitle {
      color: var(--text-dim);
      font-size: 11px;
      letter-spacing: 1px;
      margin-top: 3px;
    }

    .live-pill {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--green);
      font-size: 11px;
      letter-spacing: 1px;
      text-transform: uppercase;
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 0 0 rgba(0,230,118,.6);
      animation: pulse 1.6s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(0,230,118,.6); }
      50% { box-shadow: 0 0 0 7px rgba(0,230,118,0); }
    }

    .clock {
      color: var(--text-dim);
      font-family: 'Orbitron', monospace;
      font-size: 12px;
      margin-left: 16px;
    }

    .persona-chip {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      border: 1px solid var(--red);
      background: var(--red-faint);
      color: var(--red);
      padding: 9px 12px;
      border-radius: 8px;
      margin-bottom: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
    }

    .persona-icon {
      width: 24px;
      height: 24px;
      display: grid;
      place-items: center;
      color: white;
      background: var(--red);
      border-radius: 6px;
      font-family: 'Orbitron', monospace;
    }

    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 16px 0 10px;
    }

    .section-title {
      font-family: 'Orbitron', monospace;
      font-size: 11px;
      letter-spacing: 3px;
      color: var(--red);
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .section-title::before {
      content: "";
      width: 3px;
      height: 14px;
      background: var(--red);
      border-radius: 2px;
    }

    .section-side {
      font-size: 11px;
      color: var(--text-dim);
      letter-spacing: .5px;
    }

    .card, .news-card, .reco-card, .pipeline-card, .region-card {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 10px;
      padding: 15px 16px;
      position: relative;
      overflow: hidden;
      transition: all .25s ease;
      margin-bottom: 10px;
    }

    .card::before, .news-card::before, .reco-card::before, .pipeline-card::before, .region-card::before, .kpi-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--red), transparent);
      opacity: .45;
    }

    .news-card:hover, .reco-card:hover, .pipeline-card:hover, .region-card:hover {
      border-color: var(--border);
      background: var(--bg-card-hover);
    }

    .kpi-card {
      min-height: 118px;
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 10px;
      padding: 14px 16px;
      position: relative;
      overflow: hidden;
      margin-bottom: 12px;
    }

    .kpi-label {
      font-size: 9px;
      letter-spacing: 2px;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-bottom: 9px;
    }

    .kpi-value {
      font-family: 'Orbitron', monospace;
      font-size: 25px;
      font-weight: 800;
      color: white;
      line-height: 1;
      margin-bottom: 7px;
    }

    .kpi-value.red { color: var(--red); }
    .kpi-value.green { color: var(--green); }
    .kpi-value.orange { color: var(--orange); }
    .kpi-value.cyan { color: var(--cyan); }

    .kpi-change {
      color: var(--green);
      font-size: 11px;
      letter-spacing: .5px;
    }

    .kpi-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      height: 3px;
      background: var(--red);
      border-radius: 0 2px 0 0;
    }

    .alert-title {
      color: white;
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 6px;
    }

    .alert-desc {
      color: var(--text-dim);
      font-size: 12px;
      line-height: 1.55;
    }

    .alert-meta {
      color: var(--text-dim);
      font-size: 10px;
      margin-top: 8px;
    }

    .badge {
      display: inline-block;
      font-size: 9px;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 1px;
      text-transform: uppercase;
      font-weight: 700;
      margin-bottom: 8px;
    }

    .badge-danger {
      background: rgba(230,14,15,.2);
      color: var(--red);
      border: 1px solid rgba(230,14,15,.34);
    }

    .badge-warning {
      background: rgba(255,152,0,.15);
      color: var(--orange);
      border: 1px solid rgba(255,152,0,.32);
    }

    .badge-info {
      background: rgba(0,180,216,.1);
      color: var(--cyan);
      border: 1px solid rgba(0,180,216,.24);
    }

    .reco-card {
      display: flex;
      gap: 12px;
      align-items: flex-start;
      color: var(--text);
      font-size: 13px;
      line-height: 1.5;
    }

    .reco-icon {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      flex: 0 0 28px;
      background: var(--red-faint);
      border: 1px solid var(--border);
      color: var(--red);
      font-family: 'Orbitron', monospace;
      font-size: 10px;
      font-weight: 800;
    }

    .pipeline-step {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid var(--border-light);
      color: var(--text-dim);
      font-size: 12px;
    }

    .pipeline-step:last-child { border-bottom: 0; }
    .pipeline-step strong { color: white; font-weight: 700; }

    .summary-grid, .score-grid, .trend-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 10px;
    }

    .summary-card, .score-card, .trend-side, .detail-panel {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 10px;
      padding: 15px 16px;
      position: relative;
      overflow: hidden;
    }

    .summary-card::before, .score-card::before, .trend-side::before, .detail-panel::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--red), transparent);
      opacity: .42;
    }

    .summary-icon {
      width: 30px;
      height: 30px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: var(--red-faint);
      border: 1px solid var(--border);
      color: var(--red);
      font-family: 'Orbitron', monospace;
      font-weight: 800;
      margin-bottom: 8px;
    }

    .summary-title, .score-name, .trend-title {
      color: white;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .8px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    .summary-text, .trend-text {
      color: var(--text-dim);
      font-size: 12px;
      line-height: 1.55;
    }

    .score-number {
      font-family: 'Orbitron', monospace;
      font-size: 32px;
      font-weight: 900;
      color: var(--red);
      line-height: 1;
      margin-bottom: 8px;
    }

    .fake-score-box {
      padding: 9px;
      background: rgba(255,255,255,.04);
      border-radius: 8px;
      margin-top: 10px;
    }

    .fake-score-label {
      color: var(--text-dim);
      font-size: 11px;
      margin-bottom: 5px;
    }

    .fake-score-line {
      height: 4px;
      background: rgba(255,255,255,.08);
      border-radius: 2px;
      overflow: hidden;
    }

    .fake-score-fill {
      height: 100%;
      background: var(--red);
    }

    .fake-score-value {
      color: var(--red);
      font-size: 13px;
      font-weight: 800;
      margin-top: 5px;
      font-family: 'Orbitron', monospace;
    }

    .region-radar {
      min-height: 300px;
      border: 1px solid var(--border-light);
      border-radius: 16px;
      padding: 18px;
      background:
        radial-gradient(circle at 50% 45%, rgba(230,14,15,.13), transparent 42%),
        linear-gradient(145deg, rgba(255,255,255,.04), rgba(255,255,255,.015));
    }

    .region-card {
      min-height: 116px;
      text-align: center;
      cursor: pointer;
    }

    .region-name {
      font-family: 'Orbitron', monospace;
      font-size: 12px;
      color: white;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }

    .region-mini-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      margin-top: 8px;
    }

    .region-mini {
      padding: 5px;
      border-radius: 6px;
      background: rgba(255,255,255,.04);
      color: var(--text-dim);
      font-size: 10px;
    }

    .ticker-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(6,6,8,.95);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      margin: 12px 0;
      overflow: hidden;
    }

    .ticker-label {
      color: var(--red);
      font-family: 'Orbitron', monospace;
      font-size: 11px;
      letter-spacing: 2px;
      white-space: nowrap;
    }

    .ticker-text {
      color: var(--text-dim);
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .detail-panel {
      border-color: var(--border);
      box-shadow: 0 18px 48px rgba(0,0,0,.35), 0 0 24px rgba(230,14,15,.16);
    }

    .detail-title {
      font-family: 'Orbitron', monospace;
      color: var(--red);
      font-size: 13px;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .detail-body {
      color: var(--text);
      font-size: 13px;
      line-height: 1.6;
    }

    @media (max-width: 900px) {
      .summary-grid, .score-grid, .trend-grid {
        grid-template-columns: 1fr;
      }
    }

    .stDataFrame {
      border: 1px solid var(--border-light);
      border-radius: 10px;
      overflow: hidden;
    }

    [data-testid="stExpander"] {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 10px;
    }

    [data-testid="stAlert"] {
      background: var(--red-faint);
      border: 1px solid var(--border);
      color: var(--text);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "client_name" not in st.session_state:
    st.session_state["client_name"] = "Utilisateur"
if "detail_panel" not in st.session_state:
    st.session_state["detail_panel"] = None

if not st.session_state["logged_in"]:
    st.markdown(
        """
        <div style="min-height:72vh;display:flex;align-items:center;justify-content:center;">
          <div class="card" style="width:min(520px,100%);padding:28px;">
            <div style="display:flex;gap:16px;align-items:center;margin-bottom:18px;">
              <div class="logo-tile">T</div>
              <div>
                <div class="brand-title" style="font-size:18px;">Tnassnissa</div>
                <div class="brand-subtitle">Connexion client personnalisee</div>
              </div>
            </div>
            <div class="summary-text" style="margin-bottom:16px;">
              Selectionnez le type de client pour charger un dashboard adapte avec news, scores, regions et recommandations.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("login_form"):
        client_name = st.text_input("Nom du client", placeholder="Nom ou organisation")
        login_persona_label = st.selectbox("Type de client", list(PERSONAS.keys()))
        login_interest = None
        if login_persona_label == "Entreprise":
            login_interest = st.selectbox("Secteur entreprise", list(BUSINESS_INTERESTS.keys()))
        submitted = st.form_submit_button("Se connecter", use_container_width=True)
    if submitted:
        st.session_state["logged_in"] = True
        st.session_state["client_name"] = client_name.strip() or "Utilisateur"
        st.session_state["persona_label"] = login_persona_label
        st.session_state["business_label"] = login_interest
        st.rerun()
    st.stop()


with st.sidebar:
    st.title("Tnassnissa")
    st.caption("Intelligence sociale tunisienne")
    st.caption(f"Client: {st.session_state.get('client_name', 'Utilisateur')}")

    default_persona = st.session_state.get("persona_label", "Journaliste")
    persona_label = st.selectbox(
        "Persona mode",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(default_persona) if default_persona in PERSONAS else 0,
    )
    persona = PERSONAS[persona_label]

    business_interest = None
    if persona == "entreprise":
        default_interest = st.session_state.get("business_label", "Mode")
        interest_label = st.selectbox(
            "Secteur entreprise",
            list(BUSINESS_INTERESTS.keys()),
            index=list(BUSINESS_INTERESTS.keys()).index(default_interest) if default_interest in BUSINESS_INTERESTS else 0,
        )
        business_interest = BUSINESS_INTERESTS[interest_label]
        st.info(f"News filtrees uniquement sur: {interest_label}.")
    else:
        st.session_state["business_label"] = None

    st.divider()
    if st.button("Lancer le pipeline", use_container_width=True):
        st.session_state["last_collection"] = run_collection()
    if st.button("Deconnexion", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["detail_panel"] = None
        st.rerun()

    last_collection = st.session_state.get("last_collection")
    if last_collection:
        backup_count = last_collection.get("backup_count", 0)
        mode = "backup simulation" if backup_count else "reel"
        st.success(f"{last_collection.get('count', 0)} signaux - {mode}")
        st.caption(", ".join(last_collection.get("sources", [])))
    else:
        st.caption("Lecture des dernieres donnees disponibles.")


data = build_dashboard(persona, business_interest)
kpis = data.get("kpis", {})
regions = data.get("regions", [])
alerts = data.get("alerts", [])
recos = data.get("recos", [])
mood = data.get("mood", [])
scores = data.get("scores", {})

business_label = data.get("businessInterestLabel")
mode_label = f"{clean_text(data.get('label', persona_label))}"
display_label = f"{persona_label} - {business_label}" if business_label else persona_label
now = datetime.now().strftime("%H:%M:%S")

st.markdown(
    f"""
    <div class="topbar">
      <div class="logo-tile">T</div>
      <div>
        <div class="brand-title">Tnassnissa</div>
        <div class="brand-subtitle">Intelligence sociale tunisienne</div>
      </div>
      <div class="live-pill"><span class="pulse-dot"></span> LIVE - NATIONAL</div>
      <div class="clock">{now}</div>
    </div>
    <div class="persona-chip">
      <span class="persona-icon">{safe(PERSONA_ICONS[persona_label])}</span>
      PERSONA MODE - {safe(display_label)}
    </div>
    """,
    unsafe_allow_html=True,
)

ticker_items = data.get("ticker", [])
if ticker_items:
    st.markdown(
        f"""
        <div class="ticker-bar">
          <div class="ticker-label">LIVE FEED</div>
          <div class="ticker-text">{safe('  |  '.join(ticker_items[:8]))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

cols = st.columns(5)
with cols[0]:
    metric_card("Regions actives", kpis.get("pulse", 0), "cyan", "Backend connecte")
with cols[1]:
    metric_card("Viral moyen", kpis.get("viral", 0), "red", "Score live")
with cols[2]:
    metric_card("SafeAd score", kpis.get("safe", 0), "green", "Brand safety")
with cols[3]:
    metric_card("Risque", kpis.get("risk", "N/A"), "orange", "Monitoring")
with cols[4]:
    metric_card("Heat", scores.get("heat", 0), "red", "Radar social")

section_title("Resume rapide", "persona engine")
summary_cards = data.get("summary", [])
if summary_cards:
    summary_html = '<div class="summary-grid">'
    for item in summary_cards[:3]:
        summary_html += f"""
        <div class="summary-card">
          <div class="summary-icon">TN</div>
          <div class="summary-title">{safe(item.get('title', 'Signal'))}</div>
          <div class="summary-text">{safe(item.get('text', ''))}</div>
        </div>
        """
    summary_html += "</div>"
    st.markdown(summary_html, unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

with left:
    section_title("News resumees & scores", mode_label)
    if alerts:
        for alert in alerts:
            badge_class = status_badge_class(alert.get("badge") or alert.get("title"))
            fake_score = fake_score_for(alert.get("title"), alert.get("desc"), alert.get("meta"))
            st.markdown(
                f"""
                <div class="news-card">
                  <span class="badge badge-{badge_class}">{safe(alert.get("badge", "info")).upper()}</span>
                  <div class="alert-title">{safe(alert.get("title", "Alerte"))}</div>
                  <div class="alert-desc">{safe(alert.get("desc", ""))}</div>
                  <div class="alert-meta">{safe(alert.get("meta", ""))}</div>
                  <div class="fake-score-box">
                    <div class="fake-score-label">Fake News Score</div>
                    <div class="fake-score-line"><div class="fake-score-fill" style="width:{fake_score}%"></div></div>
                    <div class="fake-score-value">{fake_score}/100</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Details news {clean_text(alert.get('title', 'Alerte'))[:36]}", key=f"alert_{fake_score}_{clean_text(alert.get('title'))[:24]}"):
                all_posts = [post for region in regions for post in region.get("posts", [])]
                set_detail(alert.get("title", "Alerte"), alert.get("desc", ""), all_posts[:4])
                st.rerun()
    else:
        st.info("Aucune news disponible pour ce filtre.")

with right:
    section_title("Recommandations IA")
    if recos:
        for reco in recos:
            st.markdown(
                f"""
                <div class="reco-card">
                  <div class="reco-icon">IA</div>
                  <div>{safe(html_to_text(reco.get("text", "")))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Aucune recommandation pour le moment.")

    section_title("Pipeline")
    last_collection = st.session_state.get("last_collection")
    backup_count = last_collection.get("backup_count", 0) if last_collection else 0
    pipeline_mode = "backup simulation" if backup_count else "donnees disponibles"
    st.markdown(
        f"""
        <div class="pipeline-card">
          <div class="pipeline-step"><strong>Sources</strong><span>RSS + Google Trends + YouTube</span></div>
          <div class="pipeline-step"><strong>Collector</strong><span>Python</span></div>
          <div class="pipeline-step"><strong>Summarizer</strong><span>Claude API / NLP</span></div>
          <div class="pipeline-step"><strong>Persona engine</strong><span>Regles metier</span></div>
          <div class="pipeline-step"><strong>UI</strong><span>Dashboard Streamlit</span></div>
          <div class="pipeline-step"><strong>Backup</strong><span>{safe(pipeline_mode)}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

section_title("Scores", "tnassnissa / safead / heat")
st.markdown(
    f"""
    <div class="score-grid">
      <div class="score-card">
        <div class="score-name">Tnassnissa Score</div>
        <div class="score-number">{safe(scores.get('tnassnissa', 0))}</div>
        <div class="summary-text">Intensite sociale moyenne detectee sur les signaux du persona.</div>
      </div>
      <div class="score-card">
        <div class="score-name">SafeAd Score</div>
        <div class="score-number" style="color:var(--green)">{safe(scores.get('safead', 0))}</div>
        <div class="summary-text">Niveau de securite pour une campagne ou une prise de parole.</div>
      </div>
      <div class="score-card">
        <div class="score-name">Heat Score</div>
        <div class="score-number" style="color:var(--orange)">{safe(scores.get('heat', 0))}</div>
        <div class="summary-text">Chaleur du radar social selon viralite et zones sensibles.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

section_title("Mood national", "signaux emotionnels")
mood_cols = st.columns(4)
for idx, item in enumerate((mood or [])[:4]):
    with mood_cols[idx]:
        metric_card(item.get("name", "Neutre"), f"{item.get('pct', 0)}%", ["red", "orange", "cyan", "green"][idx], "Emotion")

section_title("Radar regions", "cliquez une region")
if regions:
    st.markdown('<div class="region-radar">', unsafe_allow_html=True)
    region_cols = st.columns(4)
    for idx, region in enumerate(regions[:8]):
        badge_class = status_badge_class(region.get("status"))
        with region_cols[idx % 4]:
            st.markdown(
                f"""
                <div class="region-card">
                  <span class="badge badge-{badge_class}">{safe(region.get('status', 'Stable'))}</span>
                  <div class="region-name">{safe(region.get('name', 'Region'))}</div>
                  <div class="summary-text">{safe(region.get('category', 'Actualite'))}</div>
                  <div class="region-mini-grid">
                    <div class="region-mini">Viral<br>{safe(region.get('viral', 0))}</div>
                    <div class="region-mini">Safe<br>{safe(region.get('safe', 0))}</div>
                    <div class="region-mini">Fake<br>{safe(region.get('fake', 0))}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Voir {clean_text(region.get('name', 'Region'))}", key=f"region_{idx}_{clean_text(region.get('name'))}"):
                info = region.get("info", {})
                body = " ".join(
                    clean_text(info.get(key, ""))
                    for key in ["event", "trend", "advice", "source"]
                    if info.get(key)
                ) or region.get("summary", "")
                set_detail(region.get("name", "Region"), body, region.get("posts", []))
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

trend_battle = data.get("trendBattle", {})
left_trend = trend_battle.get("left")
right_trend = trend_battle.get("right")
if left_trend or right_trend:
    section_title("Trend battle", "comparaison regionale")
    st.markdown(
        f"""
        <div class="trend-grid">
          <div class="trend-side">
            <div class="trend-title">{safe((left_trend or {}).get('name', 'N/A'))}</div>
            <div class="score-number">{safe((left_trend or {}).get('viral', 0))}</div>
            <div class="trend-text">{safe((left_trend or {}).get('summary', ''))}</div>
          </div>
          <div class="trend-side">
            <div class="trend-title">{safe((right_trend or {}).get('name', 'N/A'))}</div>
            <div class="score-number" style="color:var(--orange)">{safe((right_trend or {}).get('viral', 0))}</div>
            <div class="trend-text">{safe((right_trend or {}).get('summary', ''))}</div>
          </div>
          <div class="trend-side">
            <div class="trend-title">Decision IA</div>
            <div class="trend-text">Prioriser la zone avec viralite haute, fake risk bas et SafeAd acceptable selon le persona choisi.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

detail = st.session_state.get("detail_panel")
if detail:
    section_title("Detail backend", "panneau interactif")
    posts_html = ""
    for post in detail.get("posts", [])[:4]:
        posts_html += f"""
        <div class="news-card">
          <div class="alert-title">{safe(post.get('platform', 'Source'))} - {safe(post.get('region', ''))}</div>
          <div class="alert-desc">{safe(post.get('content', ''))}</div>
        </div>
        """
    st.markdown(
        f"""
        <div class="detail-panel">
          <div class="detail-title">{safe(detail.get('title', 'Detail'))}</div>
          <div class="detail-body">{safe(detail.get('body', ''))}</div>
          {posts_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Fermer le detail"):
        st.session_state["detail_panel"] = None
        st.rerun()

section_title("Regions et signaux", "table backend")
if regions:
    rows = []
    for region in regions:
        rows.append(
            {
                "Region": clean_text(region.get("name")),
                "Status": clean_text(region.get("status")),
                "Categorie": clean_text(region.get("category")),
                "Emotion": clean_text(region.get("emotion")),
                "Viral": region.get("viral"),
                "SafeAd": region.get("safe"),
                "Fake risk": region.get("fake"),
                "Resume": clean_text(region.get("summary")),
            }
        )
    st.dataframe(as_dataframe(rows), use_container_width=True, hide_index=True)
else:
    st.warning("Aucune region active pour ce persona.")

with st.expander("Voir les posts backend"):
    posts = []
    for region in regions:
        for post in region.get("posts", []):
            posts.append(
                {
                    "Region": clean_text(post.get("region")),
                    "Source": clean_text(post.get("source")),
                    "Platform": clean_text(post.get("platform")),
                    "Categorie": clean_text(post.get("category")),
                    "Viral": post.get("viral_score"),
                    "Fake": post.get("fake_score"),
                    "Contenu": clean_text(post.get("content")),
                }
            )
    if posts:
        st.dataframe(as_dataframe(posts), use_container_width=True, hide_index=True)
    else:
        st.info("Aucun post a afficher.")
