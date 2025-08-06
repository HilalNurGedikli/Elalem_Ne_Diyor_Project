import os
import time
import threading
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("models/gemini-2.5-flash")

def gemini_with_timeout(prompt: str, timeout_seconds: int = 30):
    """Gemini isteğini timeout ile yapar"""
    result = [None]
    exception = [None]
    
    def make_request():
        try:
            response = model.generate_content(prompt)
            result[0] = response.text
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=make_request)
    thread.daemon = True
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        # Thread hala çalışıyor, timeout oldu
        raise TimeoutError(f"Gemini isteği {timeout_seconds} saniyede tamamlanamadı")
    
    if exception[0]:
        raise exception[0]
    
    return result[0]


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
    
    # Timeout ve retry mekanizması
    max_retries = 3
    timeout_seconds = 20  # Site ismi tahmini kısa sürmeli
    
    for attempt in range(max_retries):
        try:
            print(f"[INFO] Site ismi tahmini başlatılıyor (deneme {attempt + 1}/{max_retries})...")
            
            # Timeout ile request
            response_text = gemini_with_timeout(prompt, timeout_seconds)
            
            print(f"[SUCCESS] Site ismi tahmini tamamlandı: {response_text[:50]}...")
            return response_text
            
        except TimeoutError:
            print(f"[WARNING] Site ismi tahmini timeout! Deneme {attempt + 1} başarısız ({timeout_seconds}s aşıldı)")
            if attempt == max_retries - 1:
                return f"[TIMEOUT] Site ismi tahmini zaman aşımına uğradı"
            time.sleep(2)
            
        except Exception as e:
            print(f"[ERROR] Site ismi tahmini başarısız (deneme {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:
                return f"[HATA] Site ismi tahmini başarısız: {str(e)}"
            time.sleep(2)
    
    return "[FAILED] Site ismi tahmini tüm denemeler başarısız"


# response = get_name_from_url(
#     "https://www.amazon.com.tr/stores/BISSELLT%C3%BCrkiye/page/697B9978-D9D2-453D-8543-749A13FB9B52?lp_asin=B084PSXMQM&ref_=ast_bln"
# )
# print(response)
