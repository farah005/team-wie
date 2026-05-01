# app.py — PulseTN Persona  |  Frontend Streamlit
# =================================================
# Lancer : streamlit run app.py
# Depuis la racine du projet (dossier contenant engine/)

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "engine"))

import streamlit as st
from persona_engine import get_dashboard
from database import create_tables, load_raw_posts_into_engine

# ─── Config page ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PulseTN Persona",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Palette couleurs par persona ─────────────────────────────────────────────
PERSONA_CONFIG = {
    "journaliste": {
        "label":  "Journaliste",
        "icon":   "📰",
        "color":  "#185FA5",
        "bg":     "#E6F1FB",
        "border": "#378ADD",
        "desc":   "Détection d'actualité émergente & vérification des sources",
    },
    "entreprise": {
        "label":  "Entreprise",
        "icon":   "🏢",
        "color":  "#3C3489",
        "bg":     "#EEEDFE",
        "border": "#7F77DD",
        "desc":   "Brand Safety, réputation & opportunités publicitaires",
    },
    "influenceur": {
        "label":  "Influenceur",
        "icon":   "🎬",
        "color":  "#854F0B",
        "bg":     "#FAEEDA",
        "border": "#EF9F27",
        "desc":   "Trends TikTok, hashtags viraux & meilleur moment de publication",
    },
    "citoyen": {
        "label":  "Citoyen",
        "icon":   "👤",
        "color":  "#27500A",
        "bg":     "#EAF3DE",
        "border": "#639922",
        "desc":   "Alertes sécurité, actualité locale & fake warnings",
    },
    "ong": {
        "label":  "ONG / Institution",
        "icon":   "🏛️",
        "color":  "#791F1F",
        "bg":     "#FCEBEB",
        "border": "#E24B4A",
        "desc":   "Crises sociales, catastrophes & zones prioritaires",
    },
}

# ─── Couleurs action ───────────────────────────────────────────────────────────
ACTION_STYLE = {
    "COVER":        ("#27500A", "#EAF3DE"),
    "MONITOR":      ("#185FA5", "#E6F1FB"),
    "GO":           ("#27500A", "#EAF3DE"),
    "ADAPT":        ("#854F0B", "#FAEEDA"),
    "PAUSE":        ("#791F1F", "#FCEBEB"),
    "UTILISE":      ("#27500A", "#EAF3DE"),
    "EVITE":        ("#791F1F", "#FCEBEB"),
    "DANGER":       ("#791F1F", "#FCEBEB"),
    "FAKE_WARNING": ("#854F0B", "#FAEEDA"),
    "INFO":         ("#185FA5", "#E6F1FB"),
    "VERIFY":       ("#854F0B", "#FAEEDA"),
    "SAFE":         ("#27500A", "#EAF3DE"),
    "WATCH":        ("#185FA5", "#E6F1FB"),
}

EMOTION_EMOJI = {
    "Panique":   "😨",
    "Colère":    "😡",
    "Hype":      "🔥",
    "Humour":    "😂",
    "Tristesse": "😢",
    "Solidarité":"❤️",
    "Neutre":    "😐",
}

# ─── CSS global ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Sidebar */
  section[data-testid="stSidebar"] { background: #0a0a0f; }
  section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background: #f8f8fc;
    border: 0.5px solid #e0e0ef;
    border-radius: 12px;
    padding: 12px 16px;
  }

  /* Cards posts */
  .post-card {
    background: white;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    border: 0.5px solid #e5e5ef;
    border-left-width: 4px;
  }
  .post-content { font-size: 14px; line-height: 1.5; color: #1a1a2e; margin-bottom: 8px; font-weight: 500; }
  .post-meta { font-size: 12px; color: #888; margin-bottom: 8px; }
  .tag {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 11px; margin-right: 4px; margin-bottom: 2px; font-weight: 500;
  }
  .rec { font-size: 13px; color: #333; padding: 6px 0 0 0; line-height: 1.5; }
  .action-badge {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 12px; font-weight: 500; margin-top: 8px;
  }

  /* Header */
  .pulse-header {
    padding: 1.5rem 0 1rem;
    border-bottom: 0.5px solid #e5e5ef;
    margin-bottom: 1.5rem;
  }
  .pulse-title { font-size: 28px; font-weight: 600; color: #0a0a1a; margin: 0; }
  .pulse-sub   { font-size: 14px; color: #888; margin: 4px 0 0; }

  /* Gauge bar */
  .gauge-wrap { margin: 6px 0; }
  .gauge-label { font-size: 11px; color: #888; margin-bottom: 2px; }
  .gauge-track {
    height: 6px; border-radius: 3px; background: #f0f0f8;
    overflow: hidden; margin-bottom: 2px;
  }
  .gauge-fill { height: 100%; border-radius: 3px; }
  .gauge-val { font-size: 11px; font-weight: 500; }

  /* Status bar */
  .status-ok {
    background: #EAF3DE; border-radius: 8px; padding: 8px 14px;
    font-size: 13px; color: #27500A; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 6px;
  }

  /* Section titre */
  .section-h { font-size: 13px; font-weight: 500; color: #888;
    text-transform: uppercase; letter-spacing: .06em; margin: 1.5rem 0 .7rem; }

  /* Heatmap */
  .region-pill {
    display: inline-block; margin: 3px; padding: 5px 14px;
    border-radius: 20px; font-size: 12px; font-weight: 500;
  }
</style>
""", unsafe_allow_html=True)

# ─── Init base de données ──────────────────────────────────────────────────────
@st.cache_resource
def init_db():
    create_tables()
    load_raw_posts_into_engine(limit=100)
    return True

init_db()

# ─── Sidebar : Persona Selection ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📡 PulseTN Persona")
    st.markdown("*Comprendre la Tunisie en temps réel, selon qui vous êtes.*")
    st.markdown("---")

    st.markdown("### Vous êtes :")
    persona_keys = list(PERSONA_CONFIG.keys())
    persona_labels = [f"{PERSONA_CONFIG[p]['icon']} {PERSONA_CONFIG[p]['label']}" for p in persona_keys]

    selected_idx = st.radio(
        "Persona",
        range(len(persona_keys)),
        format_func=lambda i: persona_labels[i],
        label_visibility="collapsed"
    )
    persona = persona_keys[selected_idx]
    cfg     = PERSONA_CONFIG[persona]

    st.markdown("---")

    # Filtre région
    REGIONS = ["national", "Tunis", "Sfax", "Gabès", "Sousse", "Bizerte", "Nabeul"]
    region_choice = st.selectbox("🗺️ Région", REGIONS)
    region = None if region_choice == "national" else region_choice

    st.markdown("---")
    if st.button("🔄 Actualiser les données"):
        st.cache_data.clear()
        st.rerun()

    st.markdown(f"""
    <div style="margin-top:2rem;padding:10px;background:#1a1a2e;border-radius:8px;font-size:11px;color:#888;">
      <b style="color:#aaa;">Membre 4</b><br>
      Persona Engine + BDD<br>
      <code style="color:#7F77DD">engine/persona_engine.py</code><br>
      <code style="color:#7F77DD">engine/database.py</code>
    </div>
    """, unsafe_allow_html=True)

# ─── Charger données ───────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_dashboard(persona, region):
    return get_dashboard(persona, region)

dashboard = load_dashboard(persona, region)
insights  = dashboard.get("insights", [])
total     = dashboard.get("total", 0)

# ─── Header ────────────────────────────────────────────────────────────────────
col_icon, col_title = st.columns([1, 11])
with col_icon:
    st.markdown(f"<div style='font-size:48px;line-height:1'>{cfg['icon']}</div>", unsafe_allow_html=True)
with col_title:
    st.markdown(f"""
    <div class="pulse-header">
      <div class="pulse-title" style="color:{cfg['color']}">{cfg['label']} Dashboard</div>
      <div class="pulse-sub">{cfg['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

# Status
with_scores = [i for i in insights if i.get("viral_score", 0) > 0]
st.markdown(f"""
<div class="status-ok">
  ✅ &nbsp; Base connectée — <b>{total} posts analysés</b> &nbsp;|&nbsp;
  {len(with_scores)} avec scores &nbsp;|&nbsp;
  Région : <b>{region_choice}</b>
</div>
""", unsafe_allow_html=True)

# ─── Métriques ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-h">Vue d\'ensemble</div>', unsafe_allow_html=True)

top_viral   = max((i.get("viral_score", 0) for i in insights), default=0)
alerts      = sum(1 for i in insights if i.get("action") in ["COVER","PAUSE","DANGER","UTILISE"])
avg_fake    = round(sum(i.get("fake_score",0) for i in insights if i.get("fake_score",0)>0) /
              max(len([i for i in insights if i.get("fake_score",0)>0]),1), 1)

# Métriques spécifiques par persona
if persona == "journaliste":
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("📋 Posts analysés", total)
    m2.metric("🚨 À couvrir", alerts)
    m3.metric("🔥 Top viral score", int(top_viral))
    m4.metric("⚠️ Fake score moyen", f"{avg_fake}%")

elif persona == "entreprise":
    high_bss = [i for i in insights if i.get("brand_safety_score",100) > 0]
    avg_bss  = round(sum(i.get("brand_safety_score",85) for i in insights)/max(len(insights),1),0)
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("📋 Posts analysés", total)
    m2.metric("🛡️ Brand Safety moyen", f"{int(avg_bss)}/100")
    m3.metric("⏸️ Campagnes à pauserr", sum(1 for i in insights if i.get("decision")=="PAUSE"))
    m4.metric("✅ Zones GO", sum(1 for i in insights if i.get("decision")=="GO"))

elif persona == "influenceur":
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("📋 Posts analysés", total)
    m2.metric("🔥 Trends exploitables", sum(1 for i in insights if i.get("action")=="UTILISE"))
    m3.metric("🚫 Trends à éviter", sum(1 for i in insights if i.get("action")=="EVITE"))
    m4.metric("📈 Top viral score", int(top_viral))

elif persona == "citoyen":
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("📋 Posts analysés", total)
    m2.metric("🔴 Alertes sécurité", sum(1 for i in insights if i.get("alert_level")=="DANGER"))
    m3.metric("⚠️ Fake warnings", sum(1 for i in insights if i.get("fake_warning",False)))
    m4.metric("ℹ️ Info normales", sum(1 for i in insights if i.get("alert_level")=="INFO"))

elif persona == "ong":
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("📋 Posts analysés", total)
    m2.metric("🆘 Interventions requises", sum(1 for i in insights if i.get("intervention_needed")))
    m3.metric("🗺️ Zones prioritaires", len(set(i.get("priority_zone","") for i in insights if i.get("intervention_needed"))))
    m4.metric("📊 Sentiment dominant", max(
        set(i.get("sentiment_collectif","") for i in insights if i.get("sentiment_collectif")),
        key=lambda e: sum(1 for i in insights if i.get("sentiment_collectif")==e),
        default="—"
    ))

# ─── Deux colonnes : Posts + Stats ────────────────────────────────────────────
col_posts, col_stats = st.columns([3, 2], gap="large")

with col_posts:
    st.markdown('<div class="section-h">Insights personnalisés</div>', unsafe_allow_html=True)

    if not insights:
        st.info("Aucune donnée disponible. Lance `python engine/seed_data.py` pour générer des données de test.")
    else:
        for i in insights:
            vs      = int(i.get("viral_score", 0))
            fs      = int(i.get("fake_score",  0))
            emotion = i.get("emotion", "")
            em_icon = EMOTION_EMOJI.get(emotion, "")
            region_ = i.get("region", "")
            cat     = i.get("category", "")
            content = i.get("content", "")[:110] + ("…" if len(i.get("content","")) > 110 else "")
            recs    = i.get("recommendations", [])

            # Déterminer action affichée
            action = (i.get("action") or i.get("decision") or
                      i.get("alert_level") or i.get("trend_safety_score") or "INFO")

            ac_color, ac_bg = ACTION_STYLE.get(str(action), ("#555","#f5f5f5"))

            # Couleur barre gauche selon urgence
            border_color = "#E24B4A" if action in ["PAUSE","DANGER","EVITE"] else \
                           "#639922" if action in ["GO","COVER","UTILISE","SAFE"] else \
                           cfg["border"]

            # Gauge colors
            vs_color = "#639922" if vs>70 else "#BA7517" if vs>40 else "#E24B4A"
            fs_color = "#E24B4A" if fs>60 else "#BA7517" if fs>30 else "#639922"

            tags_html = ""
            if region_: tags_html += f'<span class="tag" style="background:{cfg["bg"]};color:{cfg["color"]}">{region_}</span>'
            if cat:     tags_html += f'<span class="tag" style="background:#EEEDFE;color:#534AB7">{cat}</span>'
            if emotion: tags_html += f'<span class="tag" style="background:#f5f5f5;color:#555">{em_icon} {emotion}</span>'
            if i.get("platform"): tags_html += f'<span class="tag" style="background:#f5f5f5;color:#888">{i["platform"]}</span>'

            recs_html = "".join(f'<div class="rec">{r}</div>' for r in recs)

            extra_html = ""
            if persona == "entreprise" and i.get("brand_safety_score") is not None:
                bss = int(i["brand_safety_score"])
                bss_c = "#639922" if bss>70 else "#BA7517" if bss>40 else "#E24B4A"
                extra_html += f'<div class="gauge-wrap"><span class="gauge-label">Brand Safety</span><div class="gauge-track"><div class="gauge-fill" style="width:{bss}%;background:{bss_c}"></div></div><span class="gauge-val" style="color:{bss_c}">{bss}/100</span></div>'
            if persona == "influenceur" and i.get("best_posting_time"):
                extra_html += f'<div style="font-size:12px;color:#888;margin-top:4px">⏰ Meilleur moment : <b style="color:#854F0B">{i["best_posting_time"]}</b></div>'
            if persona == "ong" and i.get("intervention_needed"):
                extra_html += f'<div style="font-size:12px;color:#791F1F;margin-top:4px">🆘 Zone prioritaire : <b>{i.get("priority_zone","")}</b></div>'

            gauges_html = ""
            if vs > 0:
                gauges_html += f'<div class="gauge-wrap"><span class="gauge-label">Viral Score</span><div class="gauge-track"><div class="gauge-fill" style="width:{vs}%;background:{vs_color}"></div></div><span class="gauge-val" style="color:{vs_color}">{vs}/100</span></div>'
            if fs > 0:
                gauges_html += f'<div class="gauge-wrap"><span class="gauge-label">Fake Score</span><div class="gauge-track"><div class="gauge-fill" style="width:{fs}%;background:{fs_color}"></div></div><span class="gauge-val" style="color:{fs_color}">{fs}%</span></div>'

            st.markdown(f"""
            <div class="post-card" style="border-left-color:{border_color}">
              <div class="post-content">{content}</div>
              <div class="post-meta">{tags_html}</div>
              {gauges_html}
              {extra_html}
              {recs_html}
              <div><span class="action-badge" style="background:{ac_bg};color:{ac_color}">{action}</span></div>
            </div>
            """, unsafe_allow_html=True)

with col_stats:
    st.markdown('<div class="section-h">Statistiques</div>', unsafe_allow_html=True)

    # Distribution émotions
    from collections import Counter
    emotions = [i.get("emotion","") for i in insights if i.get("emotion")]
    if emotions:
        st.markdown("**Distribution des émotions**")
        em_count = Counter(emotions)
        total_em = sum(em_count.values())
        for em, cnt in em_count.most_common():
            pct = int(cnt/total_em*100)
            em_icon = EMOTION_EMOJI.get(em,"")
            color = {"Panique":"#E24B4A","Colère":"#BA7517","Hype":"#639922",
                     "Tristesse":"#185FA5","Humour":"#EF9F27"}.get(em,"#888")
            st.markdown(f"""
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px">
                <span>{em_icon} {em}</span><span style="color:#888">{cnt} post{'s' if cnt>1 else ''}</span>
              </div>
              <div class="gauge-track"><div class="gauge-fill" style="width:{pct}%;background:{color}"></div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")

    # Distribution régions
    regions_list = [i.get("region","") for i in insights if i.get("region")]
    if regions_list:
        st.markdown("**Régions actives**")
        reg_count = Counter(regions_list)
        pills_html = ""
        for reg, cnt in reg_count.most_common():
            intensity = min(int(cnt/max(reg_count.values())*100), 100)
            alpha = max(0.3, intensity/100)
            r,g,b = (
                int(cfg["border"][1:3],16),
                int(cfg["border"][3:5],16),
                int(cfg["border"][5:7],16),
            )
            pills_html += f'<span class="region-pill" style="background:rgba({r},{g},{b},{alpha:.1f});color:{cfg["color"]}">{reg} ({cnt})</span>'
        st.markdown(f'<div style="line-height:2">{pills_html}</div>', unsafe_allow_html=True)
        st.markdown("")

    # Top posts viral
    top_vs = sorted([i for i in insights if i.get("viral_score",0)>0],
                    key=lambda x: x["viral_score"], reverse=True)[:5]
    if top_vs:
        st.markdown("**Top viral scores**")
        for i in top_vs:
            vs = int(i["viral_score"])
            vs_c = "#639922" if vs>70 else "#BA7517" if vs>40 else "#E24B4A"
            reg = i.get("region","")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:13px">
              <span style="color:{vs_c};font-weight:500;min-width:32px">{vs}</span>
              <div class="gauge-track" style="flex:1"><div class="gauge-fill" style="width:{vs}%;background:{vs_c}"></div></div>
              <span style="color:#888;min-width:50px">{reg}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")

    # Actions summary
    if insights:
        st.markdown("**Résumé des décisions**")
        actions = [i.get("action") or i.get("decision") or i.get("alert_level","") for i in insights]
        act_count = Counter(a for a in actions if a)
        for act, cnt in act_count.most_common():
            ac_c, ac_bg = ACTION_STYLE.get(act, ("#555","#f5f5f5"))
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
              <span class="action-badge" style="background:{ac_bg};color:{ac_c}">{act}</span>
              <span style="font-size:13px;color:#888">{cnt} post{'s' if cnt>1 else ''}</span>
            </div>
            """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:12px;color:#aaa;padding:8px 0">'
    '📡 PulseTN Persona — Média + IA + Marketing + Sociologie + Personnalisation'
    '</div>',
    unsafe_allow_html=True
)