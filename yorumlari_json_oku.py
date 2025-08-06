import json

def yorumlari_oku(site_adi: str = None) -> list:
    """yorumlar_tarihli_filtreli.json dosyasını oku ve liste olarak döndür"""
    try:
        with open("yorumlar_tarihli_filtreli.json", "r", encoding="utf-8") as json_dosya:
            yorumlar = json.load(json_dosya)
            
            # Eğer site adı belirtilmişse, sadece o siteye ait yorumları filtrele
            if site_adi:
                site_normalized = site_adi.lower().strip().replace(" ", "").replace("-", "")
                filtered_yorumlar = []
                
                for yorum in yorumlar:
                    if isinstance(yorum, dict) and "site" in yorum:
                        yorum_site = yorum["site"].lower().strip().replace(" ", "").replace("-", "")
                        if yorum_site == site_normalized:
                            filtered_yorumlar.append(yorum)
                
                print(f"🔍 FILTERED YORUMLAR: {len(filtered_yorumlar)} yorumlar found for '{site_adi}'")
                return filtered_yorumlar
            
            return yorumlar
    except FileNotFoundError:
        print("yorumlar_tarihli_filtreli.json bulunamadı.")
        return []
    except json.JSONDecodeError:
        print("JSON dosyası bozuk veya okunamıyor.")
        return []
