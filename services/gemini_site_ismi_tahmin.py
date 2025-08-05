import os
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("models/gemini-2.5-flash")


def get_name_from_url(url: str) -> str:
    prompt = f"""
    Sana url'sini verdiğim siteni mağaza adını ver. Hiçbir ek kelime kullanmadan promptu "Mağaza ismi" formatında yaz. Cevapların alttaki gibi olsun alnızca "Panzer Art" yazan kısmı cevap olarak ver.
    Prompt:"https://www.badebutik.com/" , cevap:"Bade Butik"
    Prompt:"https://chaleipek.com.tr/" , cevap:"Chale İpek"
    Prompt:"https://www.trendyol.com/" , cevap:"Trendyol"
    Prompt:"https://www.shopier.com/PanzerArt" , cevap:"Panzer Art"
    Prompt:"https://www.trendyol.com/magaza/keywest-m-394592" , cevap:"Keywest"
    url:{url} 
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[HATA] Gemini isteği başarısız: {str(e)}"


# response = get_name_from_url(
#     "https://www.amazon.com.tr/stores/BISSELLT%C3%BCrkiye/page/697B9978-D9D2-453D-8543-749A13FB9B52?lp_asin=B084PSXMQM&ref_=ast_bln"
# )
# print(response)
