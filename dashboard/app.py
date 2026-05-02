# app.py — PulseTN Persona | TNessnisa Brand Dashboard
# =====================================================
# streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from database import get_posts, get_stats
from persona_engine import get_persona_dashboard, REGION_COORDS, EMOTION_EMOJI

st.set_page_config(
    page_title="TNessnisa — Intelligence Sociale",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

ASSETS = os.path.join(os.path.dirname(__file__), "assets")

def img_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

LOGO_B64 = img_b64(os.path.join(ASSETS, "logo.png"))
LOGO_SIDE_B64 = img_b64(os.path.join(ASSETS, "logo_side.png"))

CSS_PATH = os.path.join(os.path.dirname(__file__), "style.css")
try:
    with open(CSS_PATH, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.markdown("""
<style>
div[data-testid="stRadio"] label { color: #ccc !important; font-size:14px !important; }
div[data-testid="stRadio"] > div { gap: 4px !important; }
div[data-testid="stSelectbox"] select { background:#1e1e1e !important; color:white !important; }
div[data-testid="stButton"] button {
  background: #e60e0f !important; color: white !important;
  border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; font-size: 15px !important;
  padding: 10px 0 !important; width: 100% !important;
}
div[data-testid="stButton"] button:hover {
  background: #b50b0c !important;
}
.stMetric { background:#141414 !important; border-radius:12px !important; padding:12px !important; }
.stMetric label { color:#888 !important; font-size:11px !important; text-transform:uppercase !important; }
.stMetric [data-testid="stMetricValue"] { color:#e60e0f !important; font-size:28px !important; font-weight:800 !important; }
.stTabs [data-baseweb="tab"] { background:#1e1e1e !important; color:#888 !important; border-radius:8px 8px 0 0 !important; }
.stTabs [aria-selected="true"] { background:#e60e0f !important; color:white !important; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.persona = None

# PAGE LOGIN
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    .stApp { background: radial-gradient(ellipse at 50% 0%, rgba(230,14,15,0.08) 0%, #000 60%) !important; }
    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.6, 1])
    with center:
        if LOGO_B64:
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:8px">
              <img src="data:image/png;base64,{LOGO_B64}" style="width:220px;filter:drop-shadow(0 0 30px rgba(230,14,15,0.5))"/>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;font-size:48px">📡</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="login-wrap">
          <div class="login-title">Intelligence Sociale Tunisienne</div>
          <div class="login-sub">
            <span class="pulse-dot"></span>
            Plateforme en temps réel · Sélectionnez votre profil
          </div>
        </div>
        """, unsafe_allow_html=True)

        PERSONAS = {
            "🏢 Entreprise": "Entreprise",
            "📰 Journalisme": "Journalisme",
            "🎬 Influenceur": "Influenceur",
            "⚽ Sport": "Sport",
            "👗 Mode": "Mode",
            "🏪 Grande Surface": "Grande Surface",
            "👤 Personne ordinaire": "Citoyen",
        }

        persona_choice = st.radio("Votre profil", list(PERSONAS.keys()))

        if st.button("🚀 Accéder à mon dashboard"):
            st.session_state.logged_in = True
            st.session_state.persona = PERSONAS[persona_choice]
            st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:24px;font-size:11px;color:#555">
          TNessnisa © 2026 · ما نحكيوش برشا... أما نعرفو برشا
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# DASHBOARD
persona = st.session_state.persona

with st.sidebar:
    if LOGO_SIDE_B64:
        st.markdown(f"""
        <div style="padding:12px 0 8px;text-align:center">
          <img src="data:image/png;base64,{LOGO_SIDE_B64}" style="width:170px;filter:drop-shadow(0 0 12px rgba(230,14,15,.4))"/>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:20px;font-weight:800;color:#e60e0f;padding:12px 0">📡 TNessnisa</div>', unsafe_allow_html=True)

    PERSONA_ICONS = {
        "Entreprise": "🏢",
        "Journalisme": "📰",
        "Influenceur": "🎬",
        "Sport": "⚽",
        "Mode": "👗",
        "Grande Surface": "🏪",
        "Citoyen": "👤",
    }

    st.markdown(f"""
    <div style="background:#1e1e1e;border:1px solid #3a3a3a;border-radius:10px;padding:10px 14px;margin-bottom:16px">
      <div style="font-size:11px;color:#888;text-transform:uppercase">Profil actif</div>
      <div style="font-size:16px;font-weight:700;color:#fff;margin-top:2px">
        {PERSONA_ICONS.get(persona,'👤')} {persona}
      </div>
    </div>
    """, unsafe_allow_html=True)

    REGIONS_LIST = ["Toutes"] + sorted(REGION_COORDS.keys())
    PLATFORMS = ["Toutes", "Facebook", "TikTok", "Instagram", "RSS", "Google Trends", "News"]

    region_filter = st.selectbox("🗺️ Région", REGIONS_LIST)
    platform_filter = st.selectbox("📱 Plateforme", PLATFORMS)

    st.markdown("---")

    if st.button("🔄 Actualiser"):
        st.cache_data.clear()
        st.rerun()

    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.persona = None
        st.rerun()

@st.cache_data(ttl=30)
def load_data(region, platform, persona_value):
    posts = get_posts(
        200,
        region if region != "Toutes" else None,
        platform if platform != "Toutes" else None
    )
    dash = get_persona_dashboard(persona_value, posts)
    return posts, dash

posts, dash = load_data(region_filter, platform_filter, persona)
stats = dash["stats"]

PERSONA_DESCS = {
    "Entreprise": "Brand Safety · Publicité contextuelle · Gestion de réputation",
    "Journalisme": "Breaking news · Fake detection · Sources dominantes",
    "Influenceur": "Trends viraux · Hashtags · Meilleur timing de publication",
    "Sport": "Buzz sportif · Clubs · Scores & réactions",
    "Mode": "Fashion trends · Hashtags · Influenceurs mode",
    "Grande Surface": "Sentiment consommateur · Promotions · Risques régionaux",
    "Citoyen": "Alertes sécurité · Actualité locale · Fake warnings",
}

st.markdown(f"""
<div style="padding: 8px 0 16px">
  <div style="font-size:24px;font-weight:800;color:#fff">
    {PERSONA_ICONS.get(persona,'📡')} Dashboard {persona}
  </div>
  <div style="font-size:13px;color:#888;margin-top:3px">
    {PERSONA_DESCS.get(persona,'Intelligence sociale personnalisée')}
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:4px;background:linear-gradient(90deg,#e60e0f,transparent);border-radius:2px;margin-bottom:20px"></div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📋 Posts analysés", stats["total"])
k2.metric("🚨 Alertes critiques", stats["crises"])
k3.metric("🚀 Opportunités", stats["oppos"])
k4.metric("📍 Région active", stats["top_region"])
k5.metric("📡 Source dominante", stats["top_source"][:18] + "…" if len(stats["top_source"]) > 18 else stats["top_source"])

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ENTREPRISE
if persona == "Entreprise":
    tab1, tab2, tab3 = st.tabs(["🗺️ Carte Tunisie", "🚨 Crises & Risques", "🚀 Opportunités"])

    with tab1:
        st.markdown('<div class="section-title">Carte d’activité — Tunisie</div>', unsafe_allow_html=True)
        region_data = dash["region_data"]

        lats, lons, labels, colors, sizes, hover_texts = [], [], [], [], [], []

        for reg, info in region_data.items():
            if reg not in REGION_COORDS:
                continue

            xp = REGION_COORDS[reg]["x"]
            yp = REGION_COORDS[reg]["y"]

            lat = 37.5 - (yp / 100) * 8.5
            lon = 7.5 + (xp / 100) * 4.5

            lats.append(lat)
            lons.append(lon)
            labels.append(reg)
            colors.append(info["color"])
            sizes.append(max(12, min(40, 12 + info["score"] // 4)))

            hover_texts.append(
                f"<b>{reg}</b><br>"
                f"{info['label']}<br>"
                f"Score: {info['score']}<br>"
                f"Posts: {info['count']}"
            )

        fig_map = go.Figure()

        fig_map.add_trace(go.Scattergeo(
            lat=lats,
            lon=lons,
            text=labels,
            hovertext=hover_texts,
            hoverinfo="text",
            marker=dict(
                size=sizes,
                color=colors,
                opacity=0.85,
                line=dict(width=1.5, color="rgba(255,255,255,0.3)")
            ),
            mode="markers+text",
            textposition="top center",
            textfont=dict(size=9, color="white")
        ))

        fig_map.update_layout(
            geo=dict(
                scope="africa",
                center=dict(lat=33.8, lon=9.5),
                projection_scale=8,
                showland=True,
                landcolor="#1a1a1a",
                showocean=True,
                oceancolor="#0d0d0d",
                showcoastlines=True,
                coastlinecolor="#3a3a3a",
                showframe=False,
                bgcolor="#000000"
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=480,
            paper_bgcolor="#000000",
            plot_bgcolor="#000000",
            showlegend=False,
        )

        st.plotly_chart(fig_map, use_container_width=True)

        leg_cols = st.columns(4)
        legend_items = [
            ("#e60e0f", "🔴 Crise / Accident"),
            ("#22c55e", "🟢 Opportunité"),
            ("#f59e0b", "🟡 Sensible / Triste"),
            ("#3a3a3a", "⚪ Neutre"),
        ]

        for col, (color, label) in zip(leg_cols, legend_items):
            col.markdown(
                f'<div style="display:flex;align-items:center;gap:6px;font-size:12px;color:#ccc">'
                f'<div style="width:10px;height:10px;border-radius:50%;background:{color}"></div>{label}</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="section-title">Détail par région</div>', unsafe_allow_html=True)

        active_regions = [(reg, info) for reg, info in region_data.items() if info["count"] > 0]
        rcols = st.columns(3)

        for idx, (reg, info) in enumerate(active_regions):
            with rcols[idx % 3]:
                action = "PAUSE" if "Crise" in info["label"] else "GO" if "Opport" in info["label"] else "WATCH"
                ac_cls = "action-pause" if action == "PAUSE" else "action-go" if action == "GO" else "action-watch"
                top_post = info["posts"][0]["content"][:70] + "…" if info["posts"] else ""

                st.markdown(f"""
                <div class="tn-card">
                  <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:4px">📍 {reg}</div>
                  <div style="font-size:12px;color:#888;margin-bottom:8px">{info['label']} · {info['count']} posts</div>
                  <div class="gauge-wrap">
                    <div class="gauge-label"><span>Viral Score</span><span>{info['score']}</span></div>
                    <div class="gauge-track">
                      <div class="gauge-fill" style="width:{info['score']}%;background:{info['color']}"></div>
                    </div>
                  </div>
                  <div style="font-size:11px;color:#666;margin-top:6px;font-style:italic">{top_post}</div>
                  <span class="action-btn {ac_cls}">{action}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        crises = dash["crises"]
        if not crises:
            st.info("✅ Aucune crise détectée actuellement.")
        else:
            st.markdown(
                f'<div style="background:rgba(230,14,15,.1);border:1px solid rgba(230,14,15,.3);border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:#ff6666">'
                f'⚠️ {len(crises)} situation(s) critique(s) détectée(s) — Recommandation : <b>Pause publicitaire</b></div>',
                unsafe_allow_html=True
            )

            for p in crises:
                vs = int(p.get("viral_score", 0))
                st.markdown(f"""
                <div class="tn-card">
                  <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:6px">{p.get('content','')[:120]}…</div>
                  <span class="badge badge-red">📍 {p.get('region','')}</span>
                  <span class="badge badge-gray">{p.get('platform','')}</span>
                  <span class="badge badge-red">{EMOTION_EMOJI.get(p.get('emotion',''),'')}{p.get('emotion','')}</span>
                  <div style="font-size:24px;font-weight:800;color:#e60e0f;margin-top:8px">{vs}</div>
                  <span class="action-btn action-pause">STOP PUB</span>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        oppos = dash["opportunities"]
        if not oppos:
            st.info("Aucune opportunité marquante pour le moment.")
        else:
            for p in oppos:
                vs = int(p.get("viral_score", 0))
                st.markdown(f"""
                <div class="tn-card green">
                  <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:6px">{p.get('content','')[:120]}…</div>
                  <span class="badge badge-green">📍 {p.get('region','')}</span>
                  <span class="badge badge-gray">{p.get('platform','')}</span>
                  <span class="badge badge-green">🔥 Trend</span>
                  <div style="font-size:24px;font-weight:800;color:#22c55e;margin-top:8px">{vs}</div>
                  <span class="action-btn action-go">EXPLOITER</span>
                </div>
                """, unsafe_allow_html=True)

# JOURNALISME
elif persona == "Journalisme":
    tab1, tab2, tab3 = st.tabs(["🚨 Breaking News", "⚠️ Fake Radar", "📊 Analyse"])

    with tab1:
        urgent = dash["urgent"]
        if not urgent:
            st.info("Aucune actualité urgente détectée.")
        else:
            for i, p in enumerate(urgent):
                vs = int(p.get("viral_score", 0))
                fs = int(p.get("fake_score", 0))
                st.markdown(f"""
                <div class="tn-card">
                  <div style="font-size:22px;font-weight:900;color:#e60e0f">#{i+1}</div>
                  <div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:6px">{p.get('content','')}</div>
                  <span class="badge badge-red">📍 {p.get('region','')}</span>
                  <span class="badge badge-gray">{p.get('source','')}</span>
                  <span class="badge badge-yellow">Fake {fs}%</span>
                  <div style="font-size:26px;font-weight:900;color:#e60e0f">{vs}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        fake_sus = dash["fake_suspicious"]
        if not fake_sus:
            st.success("✅ Aucune fake news suspecte détectée.")
        else:
            for p in fake_sus:
                fs = int(p.get("fake_score", 0))
                st.markdown(f"""
                <div class="tn-card yellow">
                  <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:8px">{p.get('content','')[:120]}…</div>
                  <span class="badge badge-yellow">⚠️ Risque fake {fs}%</span>
                  <span class="badge badge-gray">{p.get('source','')}</span>
                  <span class="badge badge-gray">📍 {p.get('region','')}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        df = pd.DataFrame(posts)
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            if not df.empty and "region" in df.columns:
                reg_counts = df.groupby("region").size().reset_index(name="count").sort_values("count", ascending=False).head(10)
                fig = px.bar(
                    reg_counts,
                    x="count",
                    y="region",
                    orientation="h",
                    color="count",
                    color_continuous_scale=["#1e1e1e", "#e60e0f"],
                    title="Activité par région"
                )
                fig.update_layout(
                    paper_bgcolor="#000",
                    plot_bgcolor="#000",
                    font_color="#ccc",
                    title_font_color="#fff",
                    coloraxis_showscale=False,
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_g2:
            if not df.empty and "emotion" in df.columns:
                em_counts = df["emotion"].value_counts().reset_index()
                em_counts.columns = ["emotion", "count"]
                fig2 = px.pie(
                    em_counts,
                    values="count",
                    names="emotion",
                    title="Distribution émotions",
                    hole=0.55
                )
                fig2.update_layout(
                    paper_bgcolor="#000",
                    font_color="#ccc",
                    title_font_color="#fff",
                    height=300
                )
                st.plotly_chart(fig2, use_container_width=True)

# INFLUENCEUR / SPORT / MODE / GRANDE SURFACE
elif persona in ["Influenceur", "Sport", "Mode", "Grande Surface"]:
    tab1, tab2, tab3 = st.tabs(["🔥 Trends", "🚫 À éviter", "📊 Analyse"])

    with tab1:
        trends = dash["trends"]
        if not trends:
            st.info("Aucun trend viral pour le moment.")
        else:
            for i, p in enumerate(trends):
                vs = int(p.get("viral_score", 0))
                st.markdown(f"""
                <div class="tn-card green">
                  <div style="font-size:28px;font-weight:900;color:#22c55e">#{i+1}</div>
                  <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:6px">{p.get('content','')[:120]}…</div>
                  <span class="badge badge-green">📍 {p.get('region','')}</span>
                  <span class="badge badge-gray">{p.get('platform','')}</span>
                  <span class="badge badge-green">🔥 Viral</span>
                  <div style="font-size:30px;font-weight:900;color:#22c55e">{vs}</div>
                  <span class="action-btn action-go">UTILISER</span>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        avoid = dash["avoid"]
        if not avoid:
            st.success("✅ Aucun contenu problématique détecté.")
        else:
            for p in avoid:
                st.markdown(f"""
                <div class="tn-card">
                  <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:6px">{p.get('content','')[:120]}…</div>
                  <span class="badge badge-red">📍 {p.get('region','')}</span>
                  <span class="badge badge-red">{EMOTION_EMOJI.get(p.get('emotion',''),'')}{p.get('emotion','')}</span>
                  <span class="badge badge-gray">{p.get('platform','')}</span>
                  <div style="font-size:11px;color:#888;margin-top:6px">⚠️ Éviter ce contexte — risque de bad buzz</div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        df = pd.DataFrame(posts)
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            if not df.empty and "platform" in df.columns:
                plt_counts = df["platform"].value_counts().reset_index()
                plt_counts.columns = ["platform", "count"]
                fig = px.bar(
                    plt_counts,
                    x="platform",
                    y="count",
                    title="Posts par plateforme",
                    color="count",
                    color_continuous_scale=["#1e1e1e", "#e60e0f"]
                )
                fig.update_layout(
                    paper_bgcolor="#000",
                    plot_bgcolor="#000",
                    font_color="#ccc",
                    title_font_color="#fff",
                    coloraxis_showscale=False,
                    height=280
                )
                st.plotly_chart(fig, use_container_width=True)

        with col_g2:
            if not df.empty and "viral_score" in df.columns:
                df_vs = df[df["viral_score"] > 0].sort_values("viral_score", ascending=False).head(8)
                fig2 = px.bar(
                    df_vs,
                    x="viral_score",
                    y="region",
                    orientation="h",
                    title="Top viral par région",
                    color="viral_score",
                    color_continuous_scale=["#22c55e", "#e60e0f"]
                )
                fig2.update_layout(
                    paper_bgcolor="#000",
                    plot_bgcolor="#000",
                    font_color="#ccc",
                    title_font_color="#fff",
                    coloraxis_showscale=False,
                    height=280
                )
                st.plotly_chart(fig2, use_container_width=True)

# CITOYEN
else:
    tab1, tab2 = st.tabs(["🔔 Alertes", "📰 Actualité locale"])

    with tab1:
        alerts = dash["alerts"]
        if not alerts:
            st.success("✅ Aucune alerte dans votre région.")
        else:
            for p in alerts:
                st.markdown(f"""
                <div class="tn-card">
                  <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:6px">
                    {EMOTION_EMOJI.get(p.get('emotion',''),'🔔')} {p.get('content','')[:120]}…
                  </div>
                  <span class="badge badge-red">📍 {p.get('region','')}</span>
                  <span class="badge badge-gray">{p.get('source','')}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        local = dash["local"]
        for p in local:
            vs = int(p.get("viral_score", 0))
            st.markdown(f"""
            <div class="tn-card blue">
              <div style="font-size:13px;color:#fff;margin-bottom:6px">{p.get('content','')[:120]}…</div>
              <span class="badge badge-blue">📍 {p.get('region','')}</span>
              <span class="badge badge-gray">{p.get('platform','')}</span>
              <span class="badge badge-green">🔥 {vs}</span>
            </div>
            """, unsafe_allow_html=True)

# TABLEAU COMPLET
with st.expander("📋 Tableau complet des données"):
    if posts:
        df_show = pd.DataFrame(posts)
        columns_needed = ["region", "platform", "source", "content", "emotion", "viral_score", "fake_score", "timestamp"]
        existing_cols = [c for c in columns_needed if c in df_show.columns]

        df_show = df_show[existing_cols].copy()

        if "content" in df_show.columns:
            df_show["content"] = df_show["content"].astype(str).str[:80] + "…"

        st.dataframe(df_show, use_container_width=True, height=280)
    else:
        st.info("Aucune donnée disponible.")

st.markdown("""
<div style="text-align:center;padding:20px 0 8px;font-size:11px;color:#444;border-top:1px solid #1e1e1e;margin-top:30px">
  📡 TNessnisa · Intelligence Sociale Tunisienne · ما نحكيوش برشا... أما نعرفو برشا
</div>
""", unsafe_allow_html=True) 