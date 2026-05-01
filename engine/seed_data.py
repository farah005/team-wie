# seed_data.py
from database import create_tables, insert_post

create_tables()

posts_test = [
    ("Sfax", "Facebook", "Page Sfax Actu", "Accident grave sur la route de Sfax",
     "Accident", "Panique", 82, 15),
    ("Tunis", "TikTok", "TikTok TN Trends", "Nouveau son viral #PulseTN challenge",
     "Trend viral", "Hype", 91, 5),
    ("Gabès", "Facebook", "Groupe Gabès Infos", "Incendie signalé dans la zone industrielle",
     "Catastrophe", "Panique", 77, 20),
    ("Tunis", "Google Trends", "Google TN", "Hausse des recherches sur les élections",
     "Politique", "Colère", 65, 40),
    ("Sousse", "Instagram", "Sousse Events", "Festival de musique annulé sans explication",
     "Culture", "Tristesse", 55, 25),
]

for p in posts_test:
    insert_post(*p)

print("✅ Données de test insérées")