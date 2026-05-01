def detect_category(text):
    text = text.lower()

    if any(word in text for word in ["accident", "حادث", "blessés", "grave"]):
        return "Accident"
    if any(word in text for word in ["orage", "pluie", "météo", "chaleur", "inm"]):
        return "Météo"
    if any(word in text for word in ["festival", "culture", "fête"]):
        return "Culture"
    if any(word in text for word in ["challenge", "tiktok", "viral", "hashtag"]):
        return "Trend viral"

    return "News"


def viral_score(engagement, category):
    score = engagement

    if category in ["Accident", "Météo"]:
        score += 60
    elif category == "Trend viral":
        score += 40

    return min(score, 100)


tests = [
    "Accident grave aujourd'hui à Gabès avec plusieurs blessés",
    "Mehrez Ghannouchi alerte : orages violents et pluies intenses attendus en Tunisie",
    "Nouveau challenge TikTok viral à Tunis avec hashtag populaire",
    "Festival culturel à Sousse ce weekend"
]

for text in tests:
    category = detect_category(text)
    score = viral_score(30, category)

    print("\nPOST:", text)
    print("Catégorie:", category)
    print("Score viral:", score)