from analysis.fake_detector import process_post

post = {
    "content": "🚨 URGENT !!! Explosion à Gabès, les médias cachent la vérité !!!",
    "source": "Facebook Group Gabès",
    "region": "Gabès",
    "platform": "Facebook",
    "category": "Accident",
    "viral_score": 85
}

result = process_post(post)

print("\n=== TEST FINAL MEMBRE 3 ===")
for key, value in result.items():
    print(f"{key}: {value}")