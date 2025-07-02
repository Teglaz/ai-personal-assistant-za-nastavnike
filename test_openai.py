import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Najpre pozovi ovo, da povuče iz .env

openai.api_key = os.getenv("OPENAI_API_KEY")
print("API KLJUČ:", openai.api_key)  # Debug linija: prikazuje ključ (ne ostavljaj u realnom radu!)

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
