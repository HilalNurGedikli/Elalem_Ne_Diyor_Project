import os
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("models/gemini-2.5-flash")
    
def ask_gemini_with_reviews(site: str, yorumlar: list[dict]) -> str:
    prompt = f"""
Sen bir güvenlik analiz uzmanısın. Aşağıda {site} isimli bir butik e-ticaret sitesi hakkında farklı kaynaklardan (Şikayetvar, ETBİS, Twitter...) toplanmış kullanıcı yorumları ve veriler bulunmaktadır. Bu verileri kaynaklarına göre ayrı ayrı değerlendir:

1. **Şikayetvar** verilerinde kullanıcıların şikayetlerinin sayısı, yoğunluğu ve haklılık düzeyi hakkında yorum yap.burada maduriyetlerin nereden kaynaklandığı önemli. ve buradan gelen yorumların en nihayetinde şikayetten ibaret olduğunu unutma bu site hakkında olumlu şeyler olmadığı anlamına gelmez.
2. **ETBİS** verisinde site kayıtlı mı, değil mi? Bu durumun güvenilirlik açısından ne anlama geldiğini belirt.
3. **Twitter** yorumlarında genel kullanıcı memnuniyeti,duygu analizi, olumlu ya da olumsuz görüşlerin baskınlığı hakkında çıkarımda bulun.

Tüm bu değerlendirmelerin sonucunda sitenin genel güvenilirliğini, güçlü ve zayıf yönleriyle birlikte analiz et ve kısa bir sonuç çıkarımı yaz.

Veriler:
{chr(10).join(['- (' + yorum.get('kaynak', 'belirsiz') + ') ' + yorum['yorum'] for yorum in yorumlar if "yorum" in yorum])}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[HATA] Gemini isteği başarısız: {str(e)}"
