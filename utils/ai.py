import os
import re
from openai import OpenAI

# OpenRouter Client Setup
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def clean_ai_output(text):
    if not text:
        return ""

    # Remove markdown code blocks
    text = re.sub(r"```html", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Remove markdown separators like ---
    text = re.sub(r"\n?---+\n?", "\n", text)

    # Remove explanation sections
    unwanted_sections = [
        "Key Features",
        "How to Use This Resume",
        "Example Google",
        "Example Keywords",
        "ATS-Friendly Design",
        "Mobile-Responsive"
    ]

    for section in unwanted_sections:
        text = re.split(section, text, flags=re.IGNORECASE)[0]

    # Remove everything before first <h1>
    h1_match = re.search(r"<h1.*?>", text, flags=re.IGNORECASE)
    if h1_match:
        text = text[h1_match.start():]

    # Remove empty "Last Updated"
    text = re.sub(r"Last Updated:.*", "", text, flags=re.IGNORECASE)

    return text.strip()


def generate_resume(user_prompt):

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",   # you can change model here
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate ONLY a clean, professional HTML resume. "
                    "Start directly with HTML content like <h1>. "
                    "Do NOT add explanations, markdown formatting, code blocks, "
                    "or extra text before or after the resume."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.7
    )

    raw_output = response.choices[0].message.content

    cleaned_output = clean_ai_output(raw_output)

    return cleaned_output