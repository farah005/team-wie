def get_dashboard(persona, posts):
    dashboard = []

    for post in posts:
        content = post.get("content", "")
        category = post.get("category", "News")
        viral_score = post.get("viral_score", 50)

        priority = viral_score

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

        dashboard.append({
            "content": content,
            "category": category,
            "viral_score": viral_score,
            "priority_score": max(0, min(priority, 100)),
            "region": post.get("region", "Autre"),
            "source": post.get("source", "Unknown")
        })

    dashboard.sort(key=lambda x: x["priority_score"], reverse=True)

    return dashboard