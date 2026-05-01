# persona_engine.py — Décisions personnalisées par persona
from database import get_posts, get_stats

EMOTION_EMOJI = {"Panique":"😨","Colère":"😡","Hype":"🔥","Humour":"😂","Tristesse":"😢","Solidarité":"❤️","Neutre":"😐"}

REGION_COORDS = {
    "Tunis":{"x":68,"y":22},"Ariana":{"x":70,"y":20},"Ben Arous":{"x":70,"y":24},
    "Manouba":{"x":66,"y":21},"Nabeul":{"x":76,"y":30},"Zaghouan":{"x":70,"y":30},
    "Bizerte":{"x":64,"y":14},"Béja":{"x":56,"y":20},"Jendouba":{"x":48,"y":18},
    "Kef":{"x":50,"y":26},"Siliana":{"x":58,"y":28},"Sousse":{"x":72,"y":38},
    "Monastir":{"x":72,"y":42},"Mahdia":{"x":74,"y":48},"Sfax":{"x":68,"y":56},
    "Kairouan":{"x":64,"y":42},"Kasserine":{"x":54,"y":42},"Sidi Bouzid":{"x":60,"y":50},
    "Gabès":{"x":66,"y":66},"Médenine":{"x":72,"y":74},"Tataouine":{"x":66,"y":82},
    "Gafsa":{"x":52,"y":58},"Tozeur":{"x":44,"y":64},"Kébili":{"x":56,"y":70},
}

def get_region_color(posts_in_region):
    if not posts_in_region:
        return {"color":"#2a2a2a","label":"Neutre","score":0}
    emotions = [p.get("emotion","Neutre") for p in posts_in_region]
    scores   = [p.get("viral_score",0) for p in posts_in_region]
    avg_vs   = sum(scores)/len(scores) if scores else 0
    panic    = emotions.count("Panique") + emotions.count("Colère")
    hype     = emotions.count("Hype") + emotions.count("Humour")
    sad      = emotions.count("Tristesse") + emotions.count("Solidarité")
    if panic > 0 and avg_vs > 60:
        return {"color":"#e60e0f","label":"🔴 Crise","score":int(avg_vs)}
    elif hype > 0 and avg_vs > 65:
        return {"color":"#22c55e","label":"🟢 Opportunité","score":int(avg_vs)}
    elif sad > 0:
        return {"color":"#f59e0b","label":"🟡 Sensible","score":int(avg_vs)}
    else:
        return {"color":"#3a3a3a","label":"⚪ Neutre","score":int(avg_vs)}

def get_persona_dashboard(persona, posts):
    stats = get_stats(posts)
    p = persona.lower()

    if p == "entreprise":
        region_data = {}
        for region in REGION_COORDS:
            rp = [x for x in posts if x.get("region")==region]
            region_data[region] = {**get_region_color(rp),"posts":rp,"count":len(rp)}
        crises_posts = [x for x in posts if x.get("emotion") in ["Panique","Colère"] and x.get("viral_score",0)>65]
        oppos_posts  = [x for x in posts if x.get("emotion")=="Hype" and x.get("viral_score",0)>70]
        return {"type":"entreprise","stats":stats,"region_data":region_data,"crises":crises_posts,"opportunities":oppos_posts}

    elif p == "journalisme":
        urgent   = sorted([x for x in posts if x.get("viral_score",0)>75], key=lambda x:-x.get("viral_score",0))
        fake_sus = [x for x in posts if x.get("fake_score",0)>40]
        return {"type":"journalisme","stats":stats,"urgent":urgent[:8],"fake_suspicious":fake_sus}

    elif p in ["influenceur","sport","mode"]:
        trends  = sorted([x for x in posts if x.get("emotion")=="Hype"], key=lambda x:-x.get("viral_score",0))
        avoid   = [x for x in posts if x.get("emotion") in ["Panique","Colère"] and x.get("viral_score",0)>65]
        return {"type":"influenceur","persona_label":persona,"stats":stats,"trends":trends[:8],"avoid":avoid}

    else:  # citoyen, personne ordinaire
        alerts = [x for x in posts if x.get("emotion") in ["Panique","Colère"]]
        local  = sorted(posts, key=lambda x:-x.get("viral_score",0))[:10]
        return {"type":"citoyen","stats":stats,"alerts":alerts,"local":local}
