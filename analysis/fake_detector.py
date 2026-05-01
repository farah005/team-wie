"""
fake_detector.py — PulseTN Persona | Module 6 : Fake News Detector
====================================================================
Auteur : Membre 3 — Emotion & Fake Detection
Rôle   : Détecte la probabilité qu'un post soit une fake news ou contenu douteux.
         Inclut process_post() — point d'intégration principal pour Membre 4 et 5.

Inputs  : post dict { content, source, region, ... }
Outputs : post enrichi avec fake_score (0-100), risk_level, flags

Score logic :
    fake_score = sensationalism (30%) + source_risk (40%) + contradiction (30%)
  → 0-100, normalisé
  → risk_level : Low (<40) | Medium (40-69) | High (≥70)

Intégration :
  - process_post(post) → combine émotion + fake → structure standardisée complète
  - Compatible Membre 4 : persona_engine.process_post_scores(post)
  - Compatible SQLite  : colonnes post_id, region, platform, source, content,
                         category, emotion, viral_score, fake_score, timestamp
"""

import re
from datetime import datetime

from analysis.utils import (
    clean_text,
    normalize_text,
    extract_keywords,
    normalize_score,
    standardize_output,
    score_to_risk_level,
)
from analysis.emotion_analyzer import analyze_post


# ═══════════════════════════════════════════════════════════════════════════════
# DICTIONNAIRES DE RÉFÉRENCE
# Extensibles sans modifier la logique métier
# ═══════════════════════════════════════════════════════════════════════════════

# Mots/patterns sensationnalistes (FR + AR)
SENSATIONALISM_KEYWORDS: list[str] = [
    # Français
    "urgent", "breaking", "exclusif", "alerte", "choc",
    "incroyable", "scandaleux", "ahurissant", "fou", "jamais vu",
    "catastrophe", "apocalypse", "effondrement", "fin du monde",
    "secret", "caché", "vérité cachée", "ils ne veulent pas",
    "vous savez pas", "personne n'en parle", "médias cachent",
    "révélation", "exposé", "complot",
    # Arabe / Darija
    "عاجل", "خبر عاجل", "كارثة", "فضيحة", "مذهل",
    "لن تصدق", "سر مخفي", "الحقيقة", "المخفية",
    "3ajil", "fadhiha", "kathartha",
]

# Sources classées par niveau de crédibilité
# ── Officielles (score de confiance élevé)
OFFICIAL_SOURCE_CREDIBILITY_CAP: int = 90
OFFICIAL_SOURCES: list[str] = [
    "tap", "tap.info.tn", "agence tap",
    "mosaique fm", "mosaiquefm",
    "express fm", "expressfm",
    "shems fm", "shemsfm",
    "radio nationale", "rtci",
    "watania", "tv watania", "tvt",
    "gouvernement tunisien", "gouvernement",
    "ministère", "ministry",
    "présidence", "presidency",
    "onm", "inm", "inat", "ins",
    "municipalité", "gouvernorat",
    "page officielle",
]

# ── Sources à risque élevé (non vérifiées)
HIGH_RISK_SOURCES: list[str] = [
    "facebook group", "groupe facebook", "facebook page",
    "groupe whatsapp", "whatsapp", "telegram group",
    "tiktok user", "compte anonyme", "anonymous",
    "source inconnue", "source anonyme",
    "groupe privé",
]

# ── Sources neutres / moyennes
MEDIUM_RISK_SOURCES: list[str] = [
    "twitter", "x.com",
    "instagram", "youtube",
    "page facebook", "blog",
    "forum",
]

# Patterns de contradictions lexicales (indicateurs de contenu incohérent)
CONTRADICTION_PATTERNS: list[tuple[str, str]] = [
    # (mot_positif, mot_négatif) dont la co-présence est suspecte
    ("confirmé", "rumeur"),
    ("officiel", "non vérifié"),
    ("exclusif", "tout le monde sait"),
    ("urgent", "depuis longtemps"),
    ("premier", "déjà"),
    ("inédit", "comme toujours"),
    ("vérité", "selon des sources"),
]

# Seuils de pondération pour le fake_score final
WEIGHT_SENSATIONALISM: float = 0.30
WEIGHT_SOURCE_RISK:    float = 0.40
WEIGHT_CONTRADICTION:  float = 0.30


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS D'ANALYSE
# ═══════════════════════════════════════════════════════════════════════════════

def detect_sensationalism(text: str) -> dict:
    """
    Mesure le niveau de sensationnalisme d'un texte.

    Critères :
      - Mots-clés sensationnalistes
      - MAJUSCULES excessives (>30% des mots)
      - Ponctuation répétée (!!!, ???)
      - Présence de "URGENT" en majuscules

    Args:
        text : texte brut du post

    Returns:
        {
            "sensationalism_score": int 0-100,
            "flags": list[str]
        }
    """
    if not text or not text.strip():
        return {"sensationalism_score": 0, "flags": []}

    flags: list[str] = []
    raw_score: float = 0.0

    # 1. Mots-clés sensationnalistes ──────────────────────────
    found_kw = extract_keywords(text, SENSATIONALISM_KEYWORDS)
    if found_kw:
        kw_score = min(1.0, len(found_kw) * 0.25)   # 1 mot = 0.25, 4+ = 1.0
        raw_score += kw_score * 0.50
        flags.append("sensationalism_keywords")

    # 2. MAJUSCULES excessives ────────────────────────────────
    words = re.findall(r'\b[A-ZÀ-Ü]{2,}\b', text)
    total_words = len(text.split())
    if total_words > 0 and (len(words) / total_words) > 0.30:
        raw_score += 0.30
        flags.append("excessive_caps")

    # 3. Ponctuation répétée !!!, ??? ─────────────────────────
    exclamations = re.findall(r'!{2,}', text)
    questions    = re.findall(r'\?{2,}', text)
    if exclamations or questions:
        punct_score = min(0.20, (len(exclamations) + len(questions)) * 0.07)
        raw_score += punct_score
        flags.append("repeated_punctuation")

    # 4. "URGENT" en majuscules explicites ────────────────────
    if re.search(r'\bURGENT\b|\bBREAKING\b|\bEXCLUSIF\b', text):
        raw_score += 0.20
        if "sensationalism_keywords" not in flags:
            flags.append("urgent_caps_trigger")

    score = normalize_score(min(raw_score, 1.0), 0.0, 1.0)

    return {
        "sensationalism_score": score,
        "flags": flags,
    }


def source_credibility(source_name: str) -> dict:
    """
    Évalue la crédibilité d'une source.

    Logique :
      - Source officielle connue → crédibilité haute (score bas = peu de risque)
      - Source inconnue / Facebook group → crédibilité basse (risque élevé)
      - Source neutre → risque moyen

    Args:
        source_name : nom de la source (ex: "Facebook Group Gabès")

    Returns:
        {
            "credibility_score": int 0-100,   # 100 = très fiable
            "source_risk_score": int 0-100,   # 100 = très risqué (pour fake_score)
            "source_type": str,               # "official" | "high_risk" | "medium_risk" | "unknown"
            "flags": list[str]
        }
    """
    if not source_name or not source_name.strip():
        return {
            "credibility_score": 30,
            "source_risk_score": 70,
            "source_type": "unknown",
            "flags": ["missing_source"],
        }

    source_lower = normalize_text(source_name)
    flags: list[str] = []

    # Vérifie sources officielles
    for official in OFFICIAL_SOURCES:
        if normalize_text(official) in source_lower:
            credibility_score = OFFICIAL_SOURCE_CREDIBILITY_CAP
            return {
                "credibility_score": credibility_score,
                "source_risk_score": 100 - credibility_score,
                "source_type": "official",
                "flags": [],
            }

    # Vérifie sources à risque élevé
    for risky in HIGH_RISK_SOURCES:
        if normalize_text(risky) in source_lower:
            flags.append("unverified_source")
            return {
                "credibility_score": 20,
                "source_risk_score": 80,
                "source_type": "high_risk",
                "flags": flags,
            }

    # Vérifie sources moyennes
    for medium in MEDIUM_RISK_SOURCES:
        if normalize_text(medium) in source_lower:
            return {
                "credibility_score": 55,
                "source_risk_score": 45,
                "source_type": "medium_risk",
                "flags": ["social_media_source"],
            }

    # Source inconnue = risque par défaut
    flags.append("unknown_source")
    return {
        "credibility_score": 35,
        "source_risk_score": 65,
        "source_type": "unknown",
        "flags": flags,
    }


def _detect_contradictions(text: str) -> dict:
    """
    Détecte des paires de mots contradictoires dans le texte.
    Indicateur de contenu incohérent ou manipulé.

    Returns:
        {
            "contradiction_score": int 0-100,
            "flags": list[str]
        }
    """
    if not text:
        return {"contradiction_score": 0, "flags": []}

    normalized = normalize_text(text)
    found_pairs = 0
    flags: list[str] = []

    for word_a, word_b in CONTRADICTION_PATTERNS:
        na = normalize_text(word_a)
        nb = normalize_text(word_b)
        if na in normalized and nb in normalized:
            found_pairs += 1

    if found_pairs > 0:
        flags.append("lexical_contradiction")

    # 1 paire = 40pts, 2 paires = 70pts, 3+ = 90pts
    score_map = {0: 0, 1: 40, 2: 70}
    raw = score_map.get(found_pairs, 90)

    return {
        "contradiction_score": raw,
        "flags": flags,
    }


def calculate_fake_score(post: dict) -> dict:
    """
    Calcule le fake_score composite d'un post.

    Formule :
        fake_score = (sensationalism * 0.40)
                   + (source_risk    * 0.35)
                   + (contradiction  * 0.25)

    Args:
        post : { "content": str, "source": str, ... }

    Returns:
        {
            "fake_score": int 0-100,
            "risk_level": str,
            "sensationalism_score": int,
            "credibility_score": int,
            "contradiction_score": int,
            "flags": list[str]
        }
    """
    content = post.get("content", "")
    source  = post.get("source", "")

    # ── Analyse composants ────────────────────────────────────
    sens_result  = detect_sensationalism(content)
    src_result   = source_credibility(source)
    cont_result  = _detect_contradictions(content)

    sens_score   = sens_result["sensationalism_score"]    # 0-100
    src_risk     = src_result["source_risk_score"]         # 0-100 (plus = plus risqué)
    cont_score   = cont_result["contradiction_score"]      # 0-100

    # ── Score composite ───────────────────────────────────────
    raw_fake = (
        sens_score  * WEIGHT_SENSATIONALISM +
        src_risk    * WEIGHT_SOURCE_RISK    +
        cont_score  * WEIGHT_CONTRADICTION
    )
    fake_score = normalize_score(raw_fake, 0.0, 100.0)

    # ── Aggrégation des flags ─────────────────────────────────
    all_flags = (
        sens_result["flags"] +
        src_result["flags"]  +
        cont_result["flags"]
    )
    # Déduplique tout en préservant l'ordre
    all_flags = list(dict.fromkeys(all_flags))

    return {
        "fake_score":            fake_score,
        "risk_level":            score_to_risk_level(fake_score),
        "sensationalism_score":  sens_score,
        "credibility_score":     src_result["credibility_score"],
        "contradiction_score":   cont_score,
        "flags":                 all_flags,
    }


def analyze_fake_news(post: dict) -> dict:
    """
    Analyse complète fake news d'un post.
    Retourne le post enrichi avec tous les scores fake.

    Args:
        post : { "content": str, "source": str, ... }

    Returns:
        post enrichi avec :
            "fake_score"           : int 0-100
            "risk_level"           : "Low" | "Medium" | "High"
            "sensationalism_score" : int 0-100
            "credibility_score"    : int 0-100
            "contradiction_score"  : int 0-100
            "flags"                : list[str]
    """
    fake_result = calculate_fake_score(post)
    return {**post, **fake_result}


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'INTÉGRATION PRINCIPAL — MEMBRE 4 + MEMBRE 5
# ═══════════════════════════════════════════════════════════════════════════════

def process_post(post: dict) -> dict:
    """
    ┌─────────────────────────────────────────────────────────┐
    │  FONCTION D'INTÉGRATION PRINCIPALE — MEMBRE 3           │
    │                                                         │
    │  Combine émotion + fake detection en une seule passe.   │
    │  Retourne la structure standardisée complète.           │
    │                                                         │
    │  Utilisé par :                                          │
    │   → Membre 4 : persona_engine.process_post_scores(post) │
    │   → Membre 5 : backend pipeline                         │
    └─────────────────────────────────────────────────────────┘

    Input :
        post : {
            "content"    : str,       # texte du post (obligatoire)
            "source"     : str,       # ex: "Facebook Group Gabès"
            "region"     : str,       # ex: "Gabès"
            "platform"   : str,       # ex: "Facebook"
            "category"   : str,       # ex: "Accident" (fourni par Membre 2)
            "viral_score": int,       # 0-100 (fourni par Membre 2)
            "post_id"    : str,       # (optionnel, généré si absent)
            "timestamp"  : str,       # ISO8601 (optionnel)
        }

    Output : structure standardisée complète (voir standardize_output)
        {
            "post_id"              : str,
            "region"               : str,
            "platform"             : str,
            "source"               : str,
            "content"              : str,
            "category"             : str,
            "timestamp"            : str,
            "emotion"              : str,
            "emotion_score"        : int 0-100,
            "emojis"               : list[str],
            "fake_score"           : int 0-100,
            "risk_level"           : "Low" | "Medium" | "High",
            "flags"                : list[str],
            "viral_score"          : int 0-100,
            "sensationalism_score" : int 0-100,
            "credibility_score"    : int 0-100,
        }

    Score logic :
        emotion_score  = vote pondéré emoji + FR + AR/Darija
        fake_score     = sensationalism(40%) + source_risk(35%) + contradiction(25%)
        risk_level     = Low(<40) | Medium(40-69) | High(≥70)
    """
    # ── Étape 1 : Analyse émotionnelle ───────────────────────
    post_with_emotion = analyze_post(post)

    # ── Étape 2 : Analyse fake news ───────────────────────────
    post_with_fake = analyze_fake_news(post_with_emotion)

    # ── Étape 3 : Standardisation complète ───────────────────
    return standardize_output(post_with_fake)


# ═══════════════════════════════════════════════════════════════════════════════
# INTÉGRATION SQLITE
# ═══════════════════════════════════════════════════════════════════════════════

def save_to_db(post: dict, conn) -> None:
    """
    Sauvegarde un post analysé dans la table SQLite Posts.
    Compatible avec le schéma défini par Membre 4.

    Args:
        post : résultat de process_post()
        conn : connexion sqlite3 active

    Table Posts attendue (Membre 4) :
        post_id, region, platform, source, content, category,
        emotion, viral_score, fake_score, timestamp
    """
    defaults = {
        "post_id": post.get("post_id") or _generate_id(post),
        "region": post.get("region", "Unknown"),
        "platform": post.get("platform", "Unknown"),
        "source": post.get("source", "Unknown"),
        "content": post.get("content", ""),
        "category": post.get("category", "Unknown"),
        "emotion": post.get("emotion", "neutral"),
        "emotion_score": post.get("emotion_score", 0),
        "secondary_emotion": post.get("secondary_emotion"),
        "confidence_index": post.get("confidence_index", 0),
        "viral_score": post.get("viral_score", 0),
        "fake_score": post.get("fake_score", 0),
        "risk_level": post.get("risk_level", score_to_risk_level(post.get("fake_score", 0))),
        "sensationalism_score": post.get("sensationalism_score", 0),
        "credibility_score": post.get("credibility_score", 50),
        "contradiction_score": post.get("contradiction_score", 0),
        "flags": post.get("flags", []),
        "timestamp": post.get("timestamp", datetime.utcnow().isoformat()),
    }

    desired_columns = [
        "post_id",
        "region",
        "platform",
        "source",
        "content",
        "category",
        "emotion",
        "emotion_score",
        "secondary_emotion",
        "confidence_index",
        "viral_score",
        "fake_score",
        "risk_level",
        "sensationalism_score",
        "credibility_score",
        "contradiction_score",
        "flags",
        "timestamp",
    ]

    def _serialize_sqlite_value(value):
        if isinstance(value, (list, tuple, set)):
            return ", ".join(str(item) for item in value)
        if isinstance(value, dict):
            return str(value)
        return value

    available_columns = {
        row[1] for row in conn.execute("PRAGMA table_info(Posts)").fetchall()
    }
    columns_to_write = [column for column in desired_columns if column in available_columns]
    if not columns_to_write:
        columns_to_write = [
            "post_id",
            "region",
            "platform",
            "source",
            "content",
            "category",
            "emotion",
            "viral_score",
            "fake_score",
            "timestamp",
        ]

    values = [_serialize_sqlite_value(defaults.get(column)) for column in columns_to_write]

    cursor = conn.cursor()
    placeholders = ", ".join(["?"] * len(columns_to_write))
    columns_sql = ", ".join(columns_to_write)
    cursor.execute(
        f"""
        INSERT OR REPLACE INTO Posts (
            {columns_sql}
        ) VALUES ({placeholders})
        """,
        values,
    )
    conn.commit()


# ═══════════════════════════════════════════════════════════════════════════════
# TEST AUTONOME
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("TEST — fake_detector.py + process_post()")
    print("=" * 60)

    test_posts = [
        # Cas 1 : Fake évident — sensationnel + source non officielle
        {
            "content": "🚨🚨 URGENT URGENT !!! CATASTROPHE À GABÈS !!! "
                       "Explosion chimique MASSIVE, les MÉDIAS CACHENT LA VÉRITÉ !!! "
                       "Partagez avant que ça disparaisse !!!",
            "source": "Facebook Group Gabès",
            "region": "Gabès",
            "platform": "Facebook",
            "category": "Accident",
            "viral_score": 85,
        },
        # Cas 2 : Fiable — source officielle, ton neutre
        {
            "content": "Le gouvernorat de Sfax annonce la fermeture temporaire "
                       "de l'axe routier RN1 pour travaux de maintenance.",
            "source": "Gouvernorat de Sfax",
            "region": "Sfax",
            "platform": "Page officielle",
            "category": "Politique",
            "viral_score": 30,
        },
        # Cas 3 : Risque moyen — Twitter, vocabulaire modéré
        {
            "content": "😡 Inacceptable ! Encore des coupures d'eau à Tunis. "
                       "Selon des sources, la situation dure depuis longtemps mais "
                       "le gouvernement confirme que tout est réglé.",
            "source": "Twitter",
            "region": "Tunis",
            "platform": "Twitter",
            "category": "Social",
            "viral_score": 55,
        },
        # Cas 4 : Hype TikTok — viral, peu risqué
        {
            "content": "🔥🔥 Ce son est PARTOUT sur TikTok ! Incroyable ce trend, "
                       "tout le monde le fait maintenant ! Bravo à l'artiste !",
            "source": "TikTok",
            "region": "National",
            "platform": "TikTok",
            "category": "Trend viral",
            "viral_score": 92,
        },
        # Cas 5 : Solidarité post catastrophe
        {
            "content": "❤️🙏 Solidarité totale avec les familles des victimes. "
                       "TAP confirme : 12 blessés pris en charge. Donnons ensemble.",
            "source": "TAP - Agence Tunisienne de Presse",
            "region": "National",
            "platform": "TAP",
            "category": "Catastrophe",
            "viral_score": 60,
        },
    ]

    for i, post in enumerate(test_posts, 1):
        result = process_post(post)
        print(f"\n{'─'*55}")
        print(f"[Post {i}] {result['region']} | {result['source']}")
        print(f"  Contenu          : {post['content'][:65]}...")
        print(f"  Émotion          : {result['emotion']} ({result['emotion_score']}/100)")
        print(f"  Fake Score       : {result['fake_score']}/100 → {result['risk_level']}")
        print(f"  Sensationnalisme : {result['sensationalism_score']}/100")
        print(f"  Crédibilité src  : {result['credibility_score']}/100")
        print(f"  Flags            : {result['flags']}")
        print(f"  Viral Score      : {result['viral_score']}/100")
        print(f"  Emojis           : {result['emojis']}")

    # ── Test SQLite ───────────────────────────────────────────
    print(f"\n{'─'*55}")
    print("Test intégration SQLite...")
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE Posts (
            post_id TEXT PRIMARY KEY,
            region TEXT, platform TEXT, source TEXT, content TEXT,
            category TEXT, emotion TEXT, emotion_score INTEGER,
            secondary_emotion TEXT, confidence_index INTEGER,
            viral_score INTEGER, fake_score INTEGER,
            risk_level TEXT, sensationalism_score INTEGER,
            credibility_score INTEGER, contradiction_score INTEGER,
            flags TEXT, timestamp TEXT
        )
    """)
    sample = process_post(test_posts[0])
    save_to_db(sample, conn)
    row = conn.execute("SELECT post_id, emotion, secondary_emotion, confidence_index, fake_score FROM Posts").fetchone()
    print(f"  SQLite row: post_id={row[0][:20]}... | emotion={row[1]} | secondary={row[2]} | confidence={row[3]} | fake_score={row[4]}")
    conn.close()

    print("\n" + "=" * 60)
    print("✅ Tests fake_detector.py + process_post() terminés")
    print("=" * 60)