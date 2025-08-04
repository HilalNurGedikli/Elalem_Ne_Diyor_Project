import os
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv

load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("models/gemini-2.5-flash")

def ask_gemini_with_reviews(site: str, yorumlar: list[str]) -> str:
    prompt = f"""
    Sen bir güvenlik analiz uzmanısın. Aşağıda {site} adlı bir butik e-ticaret sitesi hakkında çeşitli kaynaklardan (Şikayetvar, ETBİS, Twitter, Ekşi Sözlük) toplanmış kullanıcı yorumları ve veriler bulunmaktadır.

    Verileri **kaynak bazında ayrı ayrı değerlendir** ve aşağıdaki kurallara dikkat et:

    1. **Şikayetvar**: 
        - Yorumlar ticari alışveriş deneyimiyle ilgili mi? Değilse atla.
        - Kaç farklı şikayet var, içeriklerinde öne çıkan sorunlar neler?
        - Kullanıcıların mağduriyetleri benzer mi, tekrar eden sorunlar var mı?
        - Yorumların tümü şikayet olduğundan, olumlu veri beklenmemeli, fakat yorumlardaki **haklılık payını ve yoğunluğunu** analiz et.

    2. **ETBİS**: 
       - Site ETBİS sistemine kayıtlı mı? 
       - Kayıtlıysa bu yasal güvenilirlik açısından ne ifade eder?
       - Kayıtlı değilse bu eksikliğin anlamı nedir?

    3. **Twitter**: 
       - Yorum sayısı yeterli mi? Değilse analiz yapmadan geç.
        - Kullanıcılar markadan olumlu mu olumsuz mu bahsediyor?
        - Genelde duygu analizi ne yönde (memnuniyet, öfke, şüphe vb.)?
        - Ticari bağlamı olmayan yorumlar (reklam, şaka, alakasız) varsa dikkate alma.

    4. **Ekşi Sözlük**: 
        - Kaç yorum var ve ne kadar güncel?
        - Yorumların tarihleri çok eskiyse olumsuzlukların düzeltilmiş olabileceğini varsayabilirsin.
        - Yorumlar ticari deneyime dayanıyor mu? Alakasızsa geç.
        - Genel memnuniyet düzeyi ve hangi yönler eleştirilmiş veya övülmüş, değerlendir.

    Tüm bu kaynakları inceledikten sonra:
        - **Sitenin genel güvenilirliğini** değerlendir.
        - **Güçlü ve zayıf yönleri** özetle.
        - Son olarak kısa ve objektif bir sonuç çıkarımı yap. Abartıdan, süslemelerden kaçın.

Veriler:
{chr(10).join(['- (' + yorum.get('kaynak', 'belirsiz') + ') ' + yorum['yorum'] for yorum in yorumlar if "yorum" in yorum])}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[HATA] Gemini isteği başarısız: {str(e)}"
