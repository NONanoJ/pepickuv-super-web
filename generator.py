from google import genai
import json
from datetime import datetime

# --- KONFIGURACE ---
# !!! SEM VLOŽ SVŮJ API KLÍČ !!!
API_KEY = "AIzaSyDCs0QD9mBjsw8HkmoVkxmc7fl-hJ2HiWg" 

client = genai.Client(api_key=API_KEY)

MASTER_PROMPT = """
Jsi šéfredaktor portálu Pepickuv_super_web. Vygeneruj přesně 3 aktuální články (1x AI World, 1x Tech & Innovation, 1x Animal Paradox).
Odpověz VÝHRADNĚ ve formátu JSON. 

Struktura JSONu:
[{"category": "...", "title": "...", "perex": ["...", "...", "..."], "body": "...", "sources": ["..."], "sentiment": 85, "image_query": "futuristic cyberpunk city", "keywords": "..."}]

Pravidla: Jazyk čeština, styl futuristický rok 2050.
"""

def generate_web():
    print("🚀 Startuji generování kostry webu (Gemini 2.5 Flash)...")
    
    try:
        # POUŽÍVÁME TVŮJ OVĚŘENÝ MODEL Z COLABU
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=MASTER_PROMPT
        )
        
        raw_text = response.text
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
        articles = json.loads(raw_text)
        print(f"✅ Úspěšně vygenerováno {len(articles)} článků.")

        # Jednoduchá, ale čistá HTML kostra
        html_content = f"""
        <!DOCTYPE html>
        <html lang="cs">
        <head>
            <meta charset="UTF-8"><title>Pepickuv_super_web - Kostra</title>
            <style>
                body {{ background: #111; color: #eee; font-family: sans-serif; padding: 20px; }}
                .card {{ border: 1px solid #444; padding: 15px; margin-bottom: 20px; border-radius: 8px; }}
                img {{ width: 100%; max-width: 400px; border-radius: 5px; }}
                h2 {{ color: #00f2ff; }}
            </style>
        </head>
        <body>
            <h1>Pepickuv_super_web (Testovací Kostra)</h1>
            <p>Aktualizováno: {datetime.now().strftime('%H:%M:%S')}</p>
        """

        for art in articles:
            query = art['image_query'].replace(' ', '%20')
            img_url = f"https://image.pollinations.ai/prompt/{query}?width=400&height=250&nologo=true"
            
            html_content += f"""
            <div class="card">
                <img src="{img_url}" alt="Ilustrace">
                <p style="color: #b522ff; text-transform: uppercase;">{art['category']}</p>
                <h2>{art['title']}</h2>
                <ul>
                    {"".join([f"<li>{p}</li>" for p in art['perex']])}
                </ul>
                <p>{art['body']}</p>
                <small>Zdroj: <a href="{art['sources'][0]}" style="color: #888;">{art['sources'][0]}</a></small>
            </div>
            """

        html_content += "</body></html>"

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("✨ HOTOVO! Kostra webu je uložena v souboru 'index.html'.")

    except Exception as e:
        print(f"❌ Chyba: {e}")

if __name__ == "__main__":
    generate_web()
