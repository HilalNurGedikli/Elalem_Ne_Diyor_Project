import os
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
print("API KEY :", os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("models/gemini-2.5-flash")

def ask_gemini_with_reviews(site: str, yorumlar: list[str]) -> str:
    prompt = f"""
Sen bir güvenilirlik analiz uzmanısın. Aşağıda {site} hakkında Şikayetvar sitesinden alınmış bazı kullanıcı yorumları verilmiştir. Bu yorumlara göre sitenin güvenilirlik düzeyini değerlendir:

Yorumlar:
{chr(10).join(['- ' + yorum for yorum in yorumlar])}

Analiz sonucunda güvenilirlik derecesini belirt.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[HATA] Gemini isteği başarısız: {str(e)}"
