import os
import re


def _local_summary(text: str, max_chars=220) -> str:
    clean = re.sub(r"\s+", " ", text or "").strip()
    if len(clean) <= max_chars:
        return clean
    sentence = re.split(r"(?<=[.!?])\s+", clean)[0]
    if 40 <= len(sentence) <= max_chars:
        return sentence
    return clean[: max_chars - 3].rstrip() + "..."


def summarize_post(post: dict) -> dict:
    content = post.get("content", "")
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")

    if api_key:
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-latest"),
                max_tokens=120,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Resume ce signal tunisien en une phrase courte, "
                            "factuelle, sans inventer d'informations:\n\n"
                            f"{content}"
                        ),
                    }
                ],
            )
            summary = message.content[0].text.strip()
            return {**post, "summary": summary, "summarizer": "claude"}
        except Exception as exc:
            print(f"Claude summarizer fallback used: {exc}")

    return {**post, "summary": _local_summary(content), "summarizer": "local_nlp"}


def summarize_posts(posts):
    return [summarize_post(post) for post in posts]
