def detect_category(text):
    text = text.lower()

    if any(word in text for word in ["accident", "حادث", "blessés", "grave"]):
        return "Accident"
    if any(word in text for word in ["orage", "pluie", "météo", "chaleur", "inm"]):
        return "Météo"
    if any(word in text for word in ["challenge", "tiktok", "viral", "hashtag"]):
        return "Trend viral"
    if any(word in text for word in ["festival", "culture", "fête"]):
        return "Culture"

    return "News"


def viral_score(engagement, category):
    score = engagement

    if category in ["Accident", "Météo"]:
        score += 60
    elif category == "Trend viral":
        score += 40
    elif category == "Culture":
        score += 10

    return max(0, min(score, 100))


def persona_priority(category, score, persona):
    priority = score

    if persona == "entreprise":
        if category in ["Accident", "Météo"]:
            priority += 30
        elif category == "Trend viral":
            priority -= 10

    elif persona == "influenceur":
        if category == "Trend viral":
            priority += 30
        elif category in ["Accident", "Météo"]:
            priority -= 20

    elif persona == "journaliste":
        if category in ["Accident", "Météo", "News"]:
            priority += 25

    elif persona == "personne_ordinaire":
        if category in ["Accident", "Météo"]:
            priority += 20

    return max(0, min(priority, 100))


def generate_recommendation(category, persona):
    if persona == "entreprise":
        if category in ["Accident", "Météo"]:
            return "⚠️ Éviter les publicités joyeuses dans cette région."
        if category == "Trend viral":
            return "📢 Trend utilisable, mais vérifier le contexte avant campagne."
        return "✅ Communication normale possible."

    if persona == "influenceur":
        if category == "Trend viral":
            return "🔥 Trend prioritaire pour créer du contenu rapidement."
        if category in ["Accident", "Météo"]:
            return "⚠️ Sujet sensible : éviter le contenu humoristique."
        return "✅ Sujet exploitable si adapté à ton audience."

    if persona == "journaliste":
        if category in ["Accident", "Météo"]:
            return "📰 Sujet prioritaire à vérifier et couvrir."
        return "📌 Sujet à surveiller."

    if persona == "personne_ordinaire":
        if category in ["Accident", "Météo"]:
            return "🚨 Alerte importante dans ta région."
        return "ℹ️ Résumé informatif."

    return "Aucune recommandation."


posts = [
    {
        "content": "Accident grave aujourd'hui à Gabès avec plusieurs blessés",
        "engagement": 30,
        "region": "Gabès"
    },
    {
        "content": "Mehrez Ghannouchi alerte : orages violents et pluies intenses attendus en Tunisie",
        "engagement": 35,
        "region": "Tunis"
    },
    {
        "content": "Nouveau challenge TikTok viral à Tunis avec hashtag populaire",
        "engagement": 50,
        "region": "Tunis"
    },
    {
        "content": "Festival culturel à Sousse ce weekend",
        "engagement": 20,
        "region": "Sousse"
    }
]

personas = ["entreprise", "influenceur", "journaliste", "personne_ordinaire"]

print("\n🚀 TEST PIPELINE COMPLET")
print("=" * 60)

for post in posts:
    category = detect_category(post["content"])
    score = viral_score(post["engagement"], category)

    print(f"\n📝 Post: {post['content']}")
    print(f"📍 Région: {post['region']}")
    print(f"🏷️ Catégorie détectée: {category}")
    print(f"📊 Score viral: {score}")

    for persona in personas:
        priority = persona_priority(category, score, persona)
        recommendation = generate_recommendation(category, persona)

        print(f"\n👤 Persona: {persona}")
        print(f"⭐ Priorité finale: {priority}")
        print(f"💡 Recommandation: {recommendation}")

print("\n✅ Pipeline complet validé")