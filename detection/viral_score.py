def normalize(value, max_value):
    try:
        value = float(value)
        max_value = float(max_value)
    except (ValueError, TypeError):
        return 0

    if max_value <= 0:
        return 0

    return min((value / max_value) * 100, 100)


def calculate_viral_score(post, max_values):
    volume_score = normalize(post.get("volume", 0), max_values.get("volume", 1))
    engagement_score = normalize(post.get("engagement", 0), max_values.get("engagement", 1))
    growth_score = normalize(post.get("growth", 0), max_values.get("growth", 1))
    multiplatform_score = normalize(post.get("platform_count", 1), max_values.get("platform_count", 1))

    viral_score = (
        volume_score +
        engagement_score +
        growth_score +
        multiplatform_score
    ) / 4

    return round(viral_score, 2)