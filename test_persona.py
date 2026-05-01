def persona_priority(category, viral_score, persona):
    score = viral_score

    if persona == "entreprise":
        if category in ["Accident", "Météo"]:
            score += 30
        elif category == "Trend viral":
            score -= 10

    elif persona == "influenceur":
        if category == "Trend viral":
            score += 30
        elif category in ["Accident", "Météo"]:
            score -= 20

    elif persona == "journaliste":
        if category in ["Accident", "Météo", "News"]:
            score += 25

    return max(0, min(score, 100))


tests = [
    ("Accident", 90),
    ("Météo", 90),
    ("Trend viral", 70),
    ("Culture", 30)
]

personas = ["entreprise", "influenceur", "journaliste"]

for persona in personas:
    print(f"\n👤 Persona: {persona}")

    for category, score in tests:
        final_score = persona_priority(category, score, persona)
        print(f"- {category}: {score} → priorité {final_score}")