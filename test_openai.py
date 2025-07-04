import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Najpre pozovi ovo, da povuče iz .env

openai.api_key = os.getenv("OPENAI_API_KEY")
# Secure way to verify API key is loaded without exposing it
if openai.api_key:
    print("API KLJUČ: ✅ Uspešno učitan")
else:
    print("API KLJUČ: ❌ Nije pronađen u .env fajlu")

try:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Pozdrav! Da li API radi?"}
        ],
        max_tokens=10
    )
    print("Radi! Odgovor:", response.choices[0].message.content)
except Exception as e:
    print("NE RADI! Greška:", e)
